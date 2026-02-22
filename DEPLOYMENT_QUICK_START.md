# Quick Start - Production Deployment Checklist

## 📋 Pre-Deployment Checklist

### Backend Preparation
- [ ] Code is clean and working locally
- [ ] All dependencies are in `backend/requirements.txt`
- [ ] `Procfile` exists with: `web: uvicorn main:app --host 0.0.0.0 --port $PORT`
- [ ] `.env.production` is created (for reference only)
- [ ] No sensitive data is hardcoded
- [ ] `.gitignore` excludes `.env` and `__pycache__`

### Frontend Preparation
- [ ] Code is clean and working locally
- [ ] `frontend/requirements.txt` exists with all dependencies
- [ ] `.streamlit/config.toml` is created
- [ ] `.streamlit/secrets.toml` is created (template)
- [ ] `config.py` reads from Streamlit secrets
- [ ] No hardcoded API URLs

### GitHub Preparation
- [ ] GitHub account created
- [ ] Repository created
- [ ] `.gitignore` is in place
- [ ] Project pushed to GitHub main branch
- [ ] All files are committed

### Database Preparation
- [ ] MySQL database created (Render, Planetscale, or AWS RDS)
- [ ] Schema imported
- [ ] Sample data populated
- [ ] Connection credentials noted (but not in code)

---

## 🚀 Deployment Steps

### Step 1: GitHub Setup (5 minutes)
```bash
cd C:\Users\Som\Downloads\HCLAgain

# Initialize git
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/ecommerce-app.git
git branch -M main
git push -u origin main
```

✅ **Completion**: Code is on GitHub

---

### Step 2: Database Setup (10 minutes)
1. **Choose provider**:
   - Render MySQL: https://render.com/
   - Planetscale: https://planetscale.com/
   - AWS RDS: https://aws.amazon.com/rds/

2. **Create database**
   - Database name: `ecommerce_db`
   - Note credentials

3. **Import schema**:
   - Run `SCHEMA.sql`
   - Run `setup_db.py` or import `DUMMY_DATA.sql`

4. **Test connection**:
   ```
   Connection string example:
   mysql://user:password@host:3306/ecommerce_db
   ```

✅ **Completion**: Database is set up with data

---

### Step 3: Backend Deployment on Render (10 minutes)

1. **Create Render Account**
   - https://render.com
   - Sign in with GitHub

2. **Create Web Service**
   - Dashboard → New Web Service
   - Connect your GitHub repository
   - Select ecommerce-app repo

3. **Configure Service**
   - Name: `ecommerce-api`
   - Environment: Python
   - Build Command: `cd backend && pip install -r requirements.txt`
   - Start Command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`

4. **Set Environment Variables**
   - Go to "Environment" tab
   - Add each variable:
     ```
     DB_HOST = your-db-host
     DB_USER = your-db-user
     DB_PASSWORD = your-db-password
     DB_NAME = ecommerce_db
     DB_PORT = 3306
     NODE_ENV = production
     JWT_SECRET = your_super_secret_key_change_me_now
     FRONTEND_URL = https://your-app-name.streamlit.app
     ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (3-5 minutes)
   - Copy API URL from dashboard

✅ **Completion**: Backend is running at `https://your-api.onrender.com`

**Test**: 
```
curl https://your-api.onrender.com/api/health
```

---

### Step 4: Frontend Deployment on Streamlit Cloud (5 minutes)

1. **Create Account**
   - https://streamlit.io/cloud
   - Sign in with GitHub

2. **Deploy App**
   - Click "New app"
   - Repository: your-ecommerce-app
   - Branch: main
   - Main file path: `frontend/app.py`
   - Click "Deploy"
   - Wait for deployment (1-2 minutes)

3. **Add Secrets**
   - Once deployed, click ⚙️ (settings) at top right
   - Click "Secrets"
   - Paste:
     ```toml
     API_URL = "https://your-api.onrender.com/api"
     ```
   - Save (app will redeploy)

✅ **Completion**: Frontend is running at `https://your-username-ecommerce-app-xxx.streamlit.app`

---

### Step 5: Verification (5 minutes)

**Test Backend**:
```bash
# In PowerShell
curl https://your-api.onrender.com/api/health
curl https://your-api.onrender.com/api/products?page=1&limit=2
```

**Test Frontend**:
1. Open: https://your-app-name.streamlit.app
2. Go to Home page
3. Login with:
   - Email: `admin@example.com`
   - Password: `admin123`
4. Click Products
5. Verify products load

✅ **Everything is deployed!**

---

## 📊 Environment Variables by Service

### Render Backend Environment
```
DB_HOST=your-mysql-host.region.db.com
DB_USER=your_db_user
DB_PASSWORD=your_strong_password_here
DB_NAME=ecommerce_db
DB_PORT=3306
NODE_ENV=production
JWT_SECRET=change_this_to_very_random_secret_key_at_least_32_chars
FRONTEND_URL=https://your-app-name.streamlit.app
```

### Streamlit Cloud Secrets
```toml
API_URL = "https://your-ecommerce-api.onrender.com/api"
```

---

## 🔐 Security Reminders

- ✅ Change `JWT_SECRET` to a unique, strong value
- ✅ Use strong database password
- ✅ Don't commit `.env` files
- ✅ Both frontend and backend should use HTTPS
- ✅ CORS is restricted to frontend URL only
- ✅ No hardcoded credentials in code

---

## 🆘 Troubleshooting

### Backend not starting
1. Check Render logs: go to service → Logs
2. Verify environment variables are set
3. Check Procfile syntax
4. Verify DB credentials

### Frontend shows "Failed to fetch products"
1. Check API_URL in Streamlit secrets
2. Check backend is running (test health endpoint)
3. Check browser console for CORS errors
4. Verify FRONTEND_URL on backend matches your Streamlit URL

### Database connection fails
1. Verify DB_HOST, DB_USER, DB_PASSWORD
2. Check database is running
3. Verify database is accessible from Render (IP whitelist if needed)
4. Test connection manually with MySQL client

---

## 🆙 Making Updates

After deployment, to make code changes:

```bash
# Make your code changes
# ...

# Commit and push
git add .
git commit -m "Your update message"
git push origin main

# Services will auto-redeploy within 1-2 minutes
```

---

## 📞 Resources

| Component | Documentation | Status Page |
|-----------|---|---|
| **Render** | https://render.com/docs | https://status.render.com |
| **Streamlit Cloud** | https://docs.streamlit.io/deploy/streamlit-cloud | https://share.streamlit.io |
| **GitHub** | https://docs.github.com | https://www.githubstatus.com |

---

## ✨ After Deployment

1. **Test all features** in production
2. **Change default password** for test users
3. **Monitor logs** regularly
4. **Set up alerting** (if available on Render)
5. **Plan backup strategy** for database
6. **Document your setup** for team

---

## 🎯 You're Done!

Your e-commerce application is now live in production:
- Backend: `https://your-api.onrender.com`
- Frontend: `https://your-app-name.streamlit.app`

Congratulations! 🎉
