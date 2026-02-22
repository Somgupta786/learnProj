# GitHub Setup for Cloud Deployment

## Step 1: Create GitHub Repository

### 1.1 Go to GitHub
1. Visit https://github.com/new
2. Create new repository
3. Enter repository name: `ecommerce-app` (or your choice)
4. Add description: "E-Commerce Application with FastAPI and Streamlit"
5. Choose Public (recommended for cloud deployment)
6. Click "Create repository"

### 1.2 Initialize Git Locally
```powershell
# Navigate to your project root
cd C:\Users\Som\Downloads\HCLAgain

# Initialize git
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: E-commerce app with FastAPI backend and Streamlit frontend"

# Add remote repository (replace with your GitHub URL)
git remote add origin https://github.com/YOUR_USERNAME/ecommerce-app.git

# Push to GitHub
git branch -M main
git push -u origin main
```

---

## Step 2: Create .gitignore

Create `.gitignore` in project root to prevent committing sensitive files:

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
*.egg-info/
dist/
build/

# Environment variables
.env
.env.local
.env.production
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# Streamlit
.streamlit/secrets.toml
.streamlit/cache/

# OS
.DS_Store
Thumbs.db

# Database
*.db
*.sqlite
*.sqlite3

# Cache
.cache/
*.cache
```

Then:
```powershell
git add .gitignore
git commit -m "Add .gitignore"
git push
```

---

## Step 3: Prepare for Render Deployment

### 3.1 Verify Procfile Exists
- File: `backend/Procfile`
- Content:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

### 3.2 Verify requirements.txt
- File: `backend/requirements.txt`
- Should include all dependencies

### 3.3 Create runtime.txt (Optional for Python version)
Create `backend/runtime.txt`:
```
python-3.12.1
```

---

## Step 4: Prepare for Streamlit Cloud Deployment

### 4.1 Ensure Directory Structure
```
ecommerce-app/
├── backend/
├── frontend/
│   ├── app.py
│   ├── config.py
│   ├── requirements.txt
│   ├── pages/
│   └── .streamlit/
│       ├── config.toml
│       └── secrets.toml (don't commit - add via dashboard)
├── README.md
└── PRODUCTION_DEPLOYMENT.md
```

### 4.2 Create/Update frontend/.streamlit/config.toml
Already done - verify it exists

### 4.3 Verify frontend/requirements.txt
Should have:
```
streamlit==1.28.1
requests==2.31.0
python-dotenv==1.0.0
```

---

## Step 5: Documentation

### 5.1 Create README.md
```markdown
# E-Commerce Application

A full-stack e-commerce application built with FastAPI (backend) and Streamlit (frontend).

## Features
- User authentication with JWT
- Product browsing and search
- Order management  
- Admin dashboard
- Shopping cart functionality

## Tech Stack
- **Backend**: FastAPI, Uvicorn, MySQL
- **Frontend**: Streamlit
- **Authentication**: JWT, bcrypt
- **Hosting**: Render (backend), Streamlit Cloud (frontend)

## Local Development
See DEVELOPMENT.md

## Production Deployment
See PRODUCTION_DEPLOYMENT.md

## API Documentation
Once backend is deployed, visit: `https://your-api.onrender.com/docs`
```

Save as `README.md` in project root

---

## Step 6: Push Everything to GitHub

```powershell
# From project root
git add .
git commit -m "Prepare for production deployment: Add Procfile, config files, and documentation"
git push origin main
```

---

## Step 7: Deploy Backend on Render

1. Go to https://render.com
2. Click "New +" → "Web Service"
3. Connect GitHub (authorize if needed)
4. Select your repository
5. Configure:
   - **Name**: `ecommerce-api`
   - **Environment**: `Python`
   - **Build Command**: `cd backend && pip install -r requirements.txt`
   - **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Root Directory**: `.` (or leave blank)
   - **Branch**: `main`

6. Go to "Environment" tab
7. Add all environment variables:
   ```
   DB_HOST=your-mysql-host
   DB_USER=your_user
   DB_PASSWORD=your_password
   DB_NAME=ecommerce_db
   DB_PORT=3306
   NODE_ENV=production
   JWT_SECRET=your_very_secret_key_here
   FRONTEND_URL=https://your-app.streamlit.app
   ```

8. Click "Create Web Service"
9. Wait for deployment (3-5 minutes)
10. Copy your API URL from Render dashboard

---

## Step 8: Deploy Frontend on Streamlit Cloud

1. Go to https://share.streamlit.io
2. Click "New app"
3. Choose repository: `ecommerce-app`
4. Set main file path: `frontend/app.py`
5. Click "Deploy"
6. Wait for deployment (1-2 minutes)

Once deployed:
1. Click settings (⚙️ at top right)
2. Go to "Secrets"
3. Add:
   ```toml
   API_URL = "https://your-ecommerce-api.onrender.com/api"
   ```
4. Save - app will redeploy

Your Streamlit URL will be: `https://your-username-ecommerce-app-xxx.streamlit.app`

---

## Step 9: Test Production

### Test Backend API
```powershell
curl https://your-api.onrender.com/api/health
```

Should return:
```json
{"status":"Server is running","environment":"production"}
```

### Test Frontend
1. Go to your Streamlit URL
2. Log in with: `admin@example.com` / `admin123`
3. Browse products
4. Test all features

---

## Step 10: Make Updates

Any changes pushed to GitHub will automatically redeploy:

```powershell
# Make code changes
# ...

# Commit and push
git add .
git commit -m "Your commit message"
git push origin main

# Render and Streamlit Cloud will automatically redeploy
```

---

## Troubleshooting

### Backend Not Deploying
1. Check Render logs
2. Verify environment variables
3. Check Procfile syntax
4. Ensure requirements.txt has all dependencies

### Frontend Not Starting
1. Check Streamlit Cloud logs
2. Verify `frontend/app.py` exists
3. Ensure `API_URL` secret is set
4. Check requirements.txt

### Cannot Connect Frontend to Backend
1. Verify API_URL is correct in Streamlit secrets
2. Check backend is running (test health endpoint)
3. Verify CORS is configured (FRONTEND_URL on backend)
4. Check for HTTPS (both should use HTTPS)

---

## References
- GitHub Docs: https://docs.github.com
- Render Docs: https://render.com/docs
- Streamlit Cloud Docs: https://docs.streamlit.io/deploy/streamlit-cloud
