# E-Commerce Application - Production Deployment Guide

## Overview
This guide covers deploying the E-Commerce application to production:
- **Backend**: FastAPI on Render
- **Frontend**: Streamlit on Streamlit Cloud
- **Database**: MySQL (managed service)

---

## Part 1: Database Setup (MySQL Hosting)

### Option A: Using Render MySQL (Recommended)
1. Go to https://render.com
2. Create a new MySQL database
3. Copy connection details:
   - Host
   - Username
   - Password
   - Database name
   - Port (usually 3306)

### Option B: Using Planetscale (Free tier available)
1. Go to https://planetscale.com
2. Create new database
3. Get connection string

### Option C: Using AWS RDS
1. Create RDS MySQL instance
2. Get endpoint and credentials
3. Configure security groups

**After creating database:**
1. Run your schema: Import `SCHEMA.sql` into the database
2. Run setup script: Import `setup_db.py` data or use `setup_db.py`

---

## Part 2: Backend Deployment (Render)

### Step 1: Prepare Repository
```bash
# Initialize git (if not already done)
cd backend
git init

# Create .gitignore
echo "__pycache__/" > .gitignore
echo "*.pyc" >> .gitignore
echo ".env" >> .gitignore
echo "*.egg-info/" >> .gitignore
echo ".venv/" >> .gitignore
```

### Step 2: Verify Requirements
Ensure `requirements.txt` has all dependencies:
```
fastapi==0.104.1
uvicorn==0.24.0
python-dotenv==1.0.0
mysql-connector-python==8.2.1
PyJWT==2.11.0
bcrypt==4.1.1
email-validator==2.1.0
```

### Step 3: Create Render Account
1. Go to https://render.com
2. Sign up with GitHub account
3. Connect your GitHub repository

### Step 4: Deploy Backend on Render
1. Create new Web Service
2. Connect your GitHub repo (backend folder)
3. Configure:
   - **Name**: `ecommerce-api`
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free (or your preferred tier)

### Step 5: Set Environment Variables on Render
Go to Service Settings > Environment Variables and add:

```
DB_HOST=your-mysql-host.com
DB_USER=your_username
DB_PASSWORD=your_strong_password
DB_NAME=ecommerce_db
DB_PORT=3306
NODE_ENV=production
JWT_SECRET=your_super_secret_jwt_key_change_this_very_important
FRONTEND_URL=https://your-app-name.streamlit.app
```

### Step 6: Deploy
1. Click "Deploy"
2. Monitor logs for errors
3. Once deployed, you'll get a URL like: `https://ecommerce-api.onrender.com`

### Step 7: Test Backend
```bash
curl https://your-backend-url.onrender.com/api/health
# Should return: {"status":"Server is running","environment":"production"}
```

---

## Part 3: Frontend Deployment (Streamlit Cloud)

### Step 1: Prepare Repository Layout
Your GitHub repo should look like:
```
your-repo/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── Procfile
│   ├── .env.production
│   └── ... (other backend files)
├── frontend/
│   ├── app.py
│   ├── config.py
│   ├── requirements.txt
│   ├── pages/
│   │   ├── 01_🏠_Home.py
│   │   ├── 02_🛍️_Products.py
│   │   ├── 03_📦_Orders.py
│   │   └── 04_⚙️_Admin.py
│   └── .streamlit/
│       ├── config.toml
│       └── secrets.toml
└── README.md
```

### Step 2: Update Frontend Requirements
Ensure `frontend/requirements.txt` exists with:
```
streamlit==1.28.1
requests==2.31.0
python-dotenv==1.0.0
```

### Step 3: Create Streamlit Cloud Account
1. Go to https://streamlit.io/cloud
2. Sign in with GitHub
3. Authorize access to your repositories

### Step 4: Deploy Frontend
1. Click "New app"
2. Select repository (choose `frontend` folder if option available, otherwise `frontend/app.py`)
3. Configure:
   - **Repository**: your-github-repo
   - **Branch**: main
   - **Main file path**: `frontend/app.py`

### Step 5: Add Secrets to Streamlit Cloud
1. After deployment, go to app settings (⚙️ at top right)
2. Click "Secrets"
3. Add:
```toml
API_URL = "https://your-backend-api.onrender.com/api"
```

4. Save - the app will redeploy automatically

### Step 6: Test Frontend
1. Your app will be at: `https://your-app-name.streamlit.app`
2. Test login with:
   - Email: `admin@example.com`
   - Password: `admin123`
3. Test product browsing

---

## Part 4: Production Checklist

### Backend
- [ ] Database is set up and accessible
- [ ] Environment variables are configured on Render
- [ ] JWT_SECRET is changed to a strong, unique value
- [ ] FRONTEND_URL is set to your Streamlit app URL
- [ ] Database credentials are secure (use managed service)
- [ ] API health check endpoint works
- [ ] Products endpoint works and returns data
- [ ] Authentication endpoints work

### Frontend  
- [ ] Frontend is deployed on Streamlit Cloud
- [ ] API_URL secret is configured correctly
- [ ] Login works with test credentials
- [ ] Products page loads and displays products
- [ ] Search functionality works
- [ ] Admin panel accessible to admin users
- [ ] Orders page shows user's orders

### Security
- [ ] No hardcoded credentials in code
- [ ] Environment variables are used for all secrets
- [ ] CORS is restricted to your frontend domain
- [ ] JWT tokens are set with appropriate expiry
- [ ] Password hashing is implemented (bcrypt)
- [ ] HTTPS is enforced

---

## Part 5: Post-Deployment

### Monitor Your Application
- **Render Dashboard**: https://dashboard.render.com
- **Streamlit Cloud**: https://share.streamlit.io
- Monitor logs for errors
- Check uptime and performance

### Update Your Credentials
Once deployed, create new test users with different passwords:
```python
# Run this script to create a new admin user
from routes.auth import hash_password
from db.user_db import UserDB

# Create new admin (you'll need access to the backend)
new_admin = UserDB.create_user(
    name="Production Admin",
    email="prod-admin@example.com",
    password=hash_password("your_strong_password"),
    phone="1234567890",
    role="admin"
)
```

### Scale Your Application
- **Render**: Upgrade plan for more resources
- **Streamlit Cloud**: Monitor usage and upgrade if needed
- **Database**: Consider managed replication for high availability

### Continuous Deployment
1. Push changes to GitHub
2. Render automatically rebuilds on push
3. Streamlit Cloud automatically redeploys on push

---

## Part 6: Troubleshooting

### Backend Issues
**Error: 502 Bad Gateway**
- Check Render logs: `render.com/dashboard`
- Verify database credentials
- Check FRONTEND_URL is correct

**Error: Cannot connect to database**
- Verify DB credentials in Environment Variables
- Check database is accessible from Render (IP whitelist)
- Ensure database exists

**CORS Error**
- Verify FRONTEND_URL in backend environment variables
- Check frontend is using HTTPS URL

### Frontend Issues
**Error: Cannot fetch products**
- Check API_URL secret is correct
- Verify backend API is running
- Check network tab for CORS errors

**Error: Login fails**
- Verify backend is accessible
- Check JWT_SECRET matches between local and production

### Database Issues
**Connection timeout**
- Add Render's IP to database security group
- Or use managed MySQL that doesn't require IP whitelisting

---

## Part 7: Environment Variables Reference

### Backend (.env on Render)
```
DB_HOST=                   # MySQL host
DB_USER=                   # MySQL username
DB_PASSWORD=               # MySQL password (strong!)
DB_NAME=ecommerce_db       # Database name
DB_PORT=3306               # MySQL port
NODE_ENV=production        # Environment
JWT_SECRET=                # Strong random string
FRONTEND_URL=              # Your Streamlit Cloud URL
```

### Frontend (Secrets in Streamlit Cloud)
```
API_URL=                   # Your Render backend URL + /api
```

---

## Part 8: Rollback & Updates

### Update Backend Code
1. Make changes locally
2. Push to GitHub
3. Render auto-redeploys

### Update Frontend Code
1. Make changes locally
2. Push to GitHub
3. Streamlit Cloud auto-redeploys

### Rollback
- Both services keep deployment history
- Use dashboard to revert to previous version

---

## Support Resources

- **Render Docs**: https://render.com/docs
- **Streamlit Cloud Docs**: https://docs.streamlit.io/deploy/streamlit-cloud
- **FastAPI Docs**: https://fastapi.tiangolo.com/deployment/
- **Streamlit Docs**: https://docs.streamlit.io/

---

## Contact & Support
For issues during deployment, check:
1. Service logs (Render/Streamlit dashboard)
2. Environment variables are set correctly
3. Database is accessible
4. GitHub repository is connected properly
