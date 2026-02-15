"""Main CLI entry point."""

import click
import logging
from pathlib import Path
from typing import List

from ..infrastructure.excel import SimpleExcelGenerator
from ..domain.models import ProcessedData
from ..plugins import get_plugin, list_plugins as get_plugin_list


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@click.group()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
def cli(verbose: bool):
    """Report Automation CLI - Generate Excel reports from CSV data."""
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Verbose logging enabled")


@cli.command()
@click.argument('input_csv', type=str)
@click.argument('output_excel', type=click.Path(path_type=Path))
@click.option('--report-type', '-t', default='a-b-report', 
              help='Type of report to generate (default: a-b-report)')
@click.option('--simple', is_flag=True, help='Generate simple test report')
@click.option('--existing-excel', type=click.Path(exists=True, path_type=Path),
              help='Existing Excel file to update (wp-chains-2-partial only)')
@click.option('--replace-week', type=str,
              help='Week number to replace (e.g., 01, 02, 03, 04)')
def generate(input_csv: str, output_excel: Path, report_type: str, simple: bool,
             existing_excel: Path, replace_week: str):
    """Generate Excel report from CSV data."""
    logger.info(f"Generating {report_type} report from {input_csv}")
    
    try:
        if simple:
            # Create simple test report
            test_data = ProcessedData(
                report_type=report_type,
                time_periods=['10m', '1h', '1d'],
                weekly_data={},
                totals={
                    '10m': {'sent': 100, 'delivered': 95, 'opened': 50, 'clicked': 10, 'converted': 2},
                    '1h': {'sent': 200, 'delivered': 190, 'opened': 80, 'clicked': 15, 'converted': 3},
                    '1d': {'sent': 150, 'delivered': 140, 'opened': 60, 'clicked': 12, 'converted': 4}
                },
                percentages={
                    '10m': {'% Delivered': 95.0, '% Open': 52.6, '% Click': 20.0, '% CR': 4.0},
                    '1h': {'% Delivered': 95.0, '% Open': 42.1, '% Click': 18.8, '% CR': 3.8},
                    '1d': {'% Delivered': 93.3, '% Open': 42.9, '% Click': 20.0, '% CR': 6.7}
                }
            )
            
            generator = SimpleExcelGenerator()
            generator.create_simple_report(test_data, output_excel)
            
            click.echo(f"✅ Simple test report generated: {output_excel}")
        else:
            # Get plugin
            plugin_class = get_plugin(report_type)
            if not plugin_class:
                available = get_plugin_list()
                click.echo(f"❌ Report type '{report_type}' not found")
                click.echo(f"Available: {', '.join(available)}")
                return
            
            plugin = plugin_class()
            
            # Parse input files
            if ',' in input_csv:
                input_paths = [Path(f.strip()) for f in input_csv.split(',')]
            else:
                input_paths = [Path(input_csv)]
            
            # Validate files exist
            for path in input_paths:
                if not path.exists():
                    click.echo(f"❌ File not found: {path}")
                    return
            
            # Ensure output directory exists
            output_excel.parent.mkdir(parents=True, exist_ok=True)
            
            # Execute plugin
            if plugin.supports_multiple_files and len(input_paths) > 1:
                plugin.execute(input_paths, output_excel, existing_excel, replace_week)
            else:
                plugin.execute(input_paths[0], output_excel)
            
            click.echo(f"✅ {report_type} report generated: {output_excel}")
        
    except Exception as e:
        logger.error(f"Error generating report: {e}")
        click.echo(f"❌ Error: {e}", err=True)
        raise click.Abort()


@cli.command()
def list_reports():
    """List available report types."""
    from ..plugins import list_plugins as get_plugin_list
    
    plugins = get_plugin_list()
    
    click.echo("Available report types:")
    if plugins:
        for plugin_name in plugins:
            click.echo(f"  • {plugin_name}")
    else:
        click.echo("  No plugins registered")


@cli.command()
@click.argument('output_path', type=click.Path(path_type=Path))
def test(output_path: Path):
    """Create a basic test Excel file."""
    logger.info(f"Creating test Excel file: {output_path}")
    
    try:
        generator = SimpleExcelGenerator()
        generator.create_basic_workbook(output_path)
        
        click.echo(f"✅ Test Excel file created: {output_path}")
        
    except Exception as e:
        logger.error(f"Error creating test file: {e}")
        click.echo(f"❌ Error: {e}", err=True)
        raise click.Abort()


def main():
    """Main entry point for the CLI."""
    cli()


if __name__ == '__main__':
    main()
