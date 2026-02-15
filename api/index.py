import sys
import os
import shutil
import tempfile
import logging
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Add the packages directory to the system path
sys.path.append(str(Path(__file__).parent / "packages"))

from report_automation.plugins import get_plugin, list_plugins
from report_automation.domain.models import ProcessedData

app = FastAPI()

# Configure CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/api/reports")
def get_reports():
    """List available report types."""
    return {"reports": list_plugins()}

@app.get("/api/reports/{report_type}/config")
def get_report_config(report_type: str):
    """Get configuration for a specific report type."""
    plugin_class = get_plugin(report_type)
    if not plugin_class:
        raise HTTPException(status_code=404, detail=f"Report type '{report_type}' not found")
    
    plugin = plugin_class()
    return plugin.get_config()

@app.post("/api/validate")
async def validate_data(
    report_type: str = Form(...),
    files: List[UploadFile] = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """Analyze data before report generation."""
    temp_dir = Path(tempfile.mkdtemp())
    try:
        input_paths = []
        for file in files:
            file_path = temp_dir / file.filename
            with open(file_path, "wb") as f:
                shutil.copyfileobj(file.file, f)
            input_paths.append(file_path)
        
        plugin_class = get_plugin(report_type)
        if not plugin_class:
            raise HTTPException(status_code=400, detail=f"Report type '{report_type}' not found")
        
        plugin = plugin_class()
        summary = plugin.validate_data(input_paths)
        
        # Clean up temp dir in background
        background_tasks.add_task(shutil.rmtree, temp_dir, ignore_errors=True)
        return summary
    except Exception as e:
        shutil.rmtree(temp_dir, ignore_errors=True)
        logger.error(f"Validation error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate")
async def generate_report(
    report_type: str = Form(...),
    files: List[UploadFile] = File(...),
    existing_excel: Optional[UploadFile] = File(None),
    replace_week: Optional[str] = Form(None),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """Generate a report from uploaded CSV files."""
    temp_dir = Path(tempfile.mkdtemp())
    output_path = temp_dir / f"{report_type}_report.xlsx"
    
    try:
        # Save uploaded CSV files
        input_paths = []
        for file in files:
            file_path = temp_dir / file.filename
            with open(file_path, "wb") as f:
                shutil.copyfileobj(file.file, f)
            input_paths.append(file_path)
            
        # Handle existing Excel file if provided
        existing_excel_path = None
        if existing_excel:
            existing_excel_path = temp_dir / existing_excel.filename
            with open(existing_excel_path, "wb") as f:
                shutil.copyfileobj(existing_excel.file, f)

        # Get plugin
        try:
            plugin_class = get_plugin(report_type)
            if not plugin_class:
                raise HTTPException(status_code=400, detail=f"Report type '{report_type}' not found")
            plugin = plugin_class()
        except ImportError as e:
             # Fallback if plugins are not registered correctly due to import issues
             # This might happen if the plugin registration relies on side-effects of imports
             # For now, let's assume standard import works, otherwise we might need to manually register
             logger.error(f"Plugin import error: {e}")
             raise HTTPException(status_code=500, detail=f"Plugin system error: {str(e)}")

        # Execute plugin logic
        try:
            if plugin.supports_multiple_files:
                # Pass list of paths if supported, even if only one file
                plugin.execute(input_paths, output_path, existing_excel_path, replace_week)
            elif len(input_paths) == 1:
                # Only pass single path if multiple not supported
                plugin.execute(input_paths[0], output_path)
            else:
                 raise HTTPException(status_code=400, detail="Multiple files provided but this report type only supports one file.")
                 
        except Exception as e:
            logger.error(f"Error executing plugin: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail=str(e))

        if not output_path.exists():
            raise HTTPException(status_code=500, detail="Report generation failed to create output file")

        # Return file response
        # We use BackgroundTasks to clean up the temp directory after the response is sent
        background_tasks.add_task(shutil.rmtree, temp_dir, ignore_errors=True)
        
        return FileResponse(
            path=output_path, 
            filename=output_path.name, 
            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

    except HTTPException:
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise
    except Exception as e:
        shutil.rmtree(temp_dir, ignore_errors=True)
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
