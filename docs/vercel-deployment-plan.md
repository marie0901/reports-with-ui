# Vercel Deployment Plan

## Overview

Deploy Next.js frontend + FastAPI backend on Vercel with file handling for CSV/Excel uploads and report generation.

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│ Vercel Edge Network                                     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Frontend (Next.js)          Backend (Python)           │
│  ┌──────────────────┐       ┌──────────────────┐       │
│  │ Static Pages     │       │ FastAPI          │       │
│  │ React Components │◄─────►│ Serverless Funcs │       │
│  │ /builder UI      │       │ /api/*           │       │
│  └──────────────────┘       └──────────────────┘       │
│                                      │                   │
│                                      ▼                   │
│                              ┌──────────────────┐       │
│                              │ /tmp (ephemeral) │       │
│                              │ - CSV uploads    │       │
│                              │ - Excel files    │       │
│                              │ - Generated xlsx │       │
│                              └──────────────────┘       │
└─────────────────────────────────────────────────────────┘
```

---

## File Handling Strategy

### How It Works (Direct Upload)

1. **Frontend uploads** CSV/Excel files via multipart/form-data
2. **Backend receives** files in FastAPI endpoint
3. **Save to /tmp** directory (ephemeral, 512 MB limit)
4. **Process** files using pandas/openpyxl
5. **Generate** Excel report in /tmp
6. **Return** file via FileResponse
7. **Auto-cleanup** /tmp cleared after function execution

### Limits
- Request body: **10 MB** (Hobby/Pro), **50 MB** (Enterprise)
- /tmp storage: **512 MB**
- Function timeout: **10s** (Hobby), **60s** (Pro)
- No persistent filesystem

### Current Implementation
Your app already uses this approach - no changes needed for deployment!

---

## Deployment Configuration

### Current vercel.json
```json
{
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    },
    {
      "src": "package.json",
      "use": "@vercel/next"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "api/index.py"
    },
    {
      "src": "/(.*)",
      "dest": "/$1"
    }
  ]
}
```

### Required Updates

**1. Add function configuration for larger payloads:**
```json
{
  "functions": {
    "api/index.py": {
      "maxDuration": 60,
      "memory": 1024
    }
  }
}
```

**2. Add environment variables:**
```json
{
  "env": {
    "PYTHON_VERSION": "3.11",
    "STORAGE_TYPE": "local"
  }
}
```

---

## Development & Deployment Workflow

### Setup

**Development Computer (Current)**
```bash
# Git already initialized ✓
# Just commit and push to GitHub

git add .
git commit -m "Prepare for deployment"

# Add your GitHub repo
git remote add origin https://github.com/marie0901/reports-with-ui.git
git push -u origin main
```

**Deployment Computer (New)**
```bash
# 1. Clone repo
git clone https://github.com/marie0901/reports-with-ui.git
cd reports-with-ui/with-UI

# 2. Install Vercel CLI
npm i -g vercel

# 3. Login to Vercel
vercel login

# 4. Deploy
vercel --prod
```

### Daily Workflow

**On Development Computer:**
```bash
# 1. Make changes
# 2. Test locally
npm run dev  # or ./start.sh

# 3. Commit and push
git add .
git commit -m "Add feature X"
git push
```

**On Deployment Computer:**
```bash
# 1. Pull latest changes
git pull

# 2. Deploy to Vercel
vercel --prod
```

### Auto-Deploy (Recommended)

Connect GitHub to Vercel for automatic deployments:

1. Go to [vercel.com](https://vercel.com)
2. Click "Add New Project"
3. Import your GitHub repo
4. Vercel auto-deploys on every `git push`

**Then you only need:**
```bash
# On development computer
git push  # Auto-deploys to Vercel ✨
```

---

## Step-by-Step Deployment

### 1. Pre-Deployment Checklist

- [ ] Verify vercel.json configuration
- [ ] Add .vercelignore file
- [ ] Test build locally
- [ ] Configure environment variables
- [ ] Set up domain (optional)

### 2. Create .vercelignore

```
# Python
api/venv/
api/__pycache__/
*.pyc
*.pyo
*.pyd
.Python

# Node
node_modules/
.next/
.turbopack/

# Development
.kiro/
docs/
*.log
.DS_Store

# Storage (will be empty on Vercel)
api/storage/uploads/
api/storage/outputs/
```

### 3. Install Vercel CLI (on deployment computer)

```bash
npm i -g vercel
```

### 4. Login to Vercel

```bash
vercel login
```

### 5. Deploy to Preview

```bash
vercel
```

This creates a preview deployment for testing.

### 6. Deploy to Production

```bash
vercel --prod
```

### 7. Configure Environment Variables (via Vercel Dashboard)

Go to: Project Settings → Environment Variables

Add:
- `PYTHON_VERSION`: `3.11`
- `STORAGE_TYPE`: `local`

---

## File Size Limits

### Vercel Limits
- Request body: **10 MB** (Hobby/Pro)
- Response body: **5 MB**
- /tmp storage: **512 MB**
- Function timeout: **10s** (Hobby), **60s** (Pro)

### If Files Exceed 10 MB
Add frontend validation:
```typescript
if (file.size > 10 * 1024 * 1024) {
  alert('File too large. Max 10 MB');
  return;
}
```

---

## Backend - No Changes Needed

Your current code already works with Vercel:
- Uses /tmp for temporary storage ✓
- Returns files via FileResponse ✓
- Cleans up with BackgroundTasks ✓

Vercel automatically:
- Clears /tmp after function execution
- Handles file streaming
- Manages memory

---

## Testing Deployment

### 1. Test API Endpoints

```bash
# Get reports
curl https://your-app.vercel.app/api/reports

# Upload and generate (small file)
curl -X POST https://your-app.vercel.app/api/generate \
  -F "report_type=slot" \
  -F "files=@test.csv" \
  -o output.xlsx
```

### 2. Test Frontend

Visit: `https://your-app.vercel.app`

- Upload CSV files
- Generate report
- Download Excel

### 3. Monitor Logs

```bash
vercel logs
```

Or via Vercel Dashboard → Deployments → View Logs

---

## Cost Estimation

### Vercel Pricing

**Hobby (Free)**
- 100 GB bandwidth/month
- 100 GB-hours function execution
- 10s max function duration
- Good for: Testing

**Pro ($20/month)**
- 1 TB bandwidth
- 1,000 GB-hours function execution
- 60s max function duration
- Good for: Production

### Estimated Cost

1,000 reports/month:
- Compute: 8 GB-hours (well within limit)
- Bandwidth: 7 GB (well within limit)

**Total: $20/month (Pro plan)**

---

## Monitoring & Debugging

### 1. Enable Logging

```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/api/generate")
async def generate_report(...):
    logger.info(f"Processing {len(files)} files for {report_type}")
    # ... processing
    logger.info(f"Generated report: {output_path}")
```

### 2. Add Health Check

```python
@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "storage_type": STORAGE_TYPE,
        "tmp_available": os.path.exists("/tmp")
    }
```

### 3. Monitor via Vercel Dashboard

- Real-time logs
- Function invocations
- Error rates
- Response times

---

## Rollback Strategy

### If Deployment Fails

**1. Instant Rollback:**
```bash
vercel rollback
```

**2. Redeploy Previous Version:**
```bash
vercel --prod --force
```

**3. Via Dashboard:**
- Go to Deployments
- Find previous working deployment
- Click "Promote to Production"

---

## Production Checklist

- [ ] Add .vercelignore file
- [ ] Set environment variables in Vercel dashboard
- [ ] Test with sample files
- [ ] Add file size validation (10 MB limit)
- [ ] Configure custom domain (optional)
- [ ] Enable Vercel Analytics (optional)

---

## Alternative Deployment (If Needed)

If files consistently exceed 10 MB:

**Railway / Render**
- No file size limits
- Persistent storage
- $5-10/month
- Deploy: `git push`

---

## Quick Start

### Option 1: Manual Deploy
```bash
# On deployment computer
git clone https://github.com/marie0901/reports-with-ui.git
cd reports-with-ui/with-UI
npm i -g vercel
vercel login
vercel --prod
```

### Option 2: Auto-Deploy (Recommended)
1. Push code to GitHub
2. Connect repo to Vercel dashboard
3. Every `git push` auto-deploys ✨

### Test
```bash
curl https://your-app.vercel.app/api/health
```

Done! 🚀
