# Deployment Setup Guide for Render

This guide will help you deploy the backend to Render.

## Prerequisites

1. **Render Account**: Create an account at [render.com](https://render.com)
2. **PostgreSQL Database**: Set up a PostgreSQL instance on Render
3. **GitHub Repository**: Push your code to GitHub

## Step 1: Create PostgreSQL Database on Render

1. Go to Render Dashboard
2. Click "New +" → "PostgreSQL"
3. Fill in the details:
   - **Name**: `ecommerce-db` (or your choice)
   - **Database**: `ecommerce_db`
   - **User**: `postgres` or custom user
   - **Region**: Select closest region
   - **PostgreSQL Version**: 15 or higher

4. **Note**: After creation, save these credentials:
   - Host (e.g., `dpg-xxxx.render.com`)
   - User
   - Password
   - Database name
   - Port (usually 5432)

## Step 2: Create Web Service on Render

1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Select the repository and branch
4. Fill in the details:
   - **Name**: `ecommerce-api` (or your choice)
   - **Region**: Same as database
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free or Starter (choose based on needs)

## Step 3: Set Environment Variables

In Render Dashboard for your web service:

1. Click "Environment" tab
2. Add the following environment variables:

```
DB_HOST=your-postgres-host.render.com
DB_USER=your_db_user
DB_PASSWORD=your_secure_password
DB_NAME=ecommerce_db
DB_PORT=5432
NODE_ENV=production
PORT=8000
HOST=0.0.0.0
JWT_SECRET=<generate-a-secure-random-secret>
FRONTEND_URL=https://your-frontend-url.com
```

### Generate JWT_SECRET

Run this command locally to generate a secure secret:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Step 4: Verify Requirements.txt

Ensure your `backend/requirements.txt` has all dependencies:

```
fastapi==0.104.1
uvicorn==0.24.0
python-dotenv==1.0.0
psycopg2-binary==2.9.6
sqlalchemy==2.0.23
pydantic==2.5.0
bcrypt==4.1.1
python-jose==3.3.0
passlib==1.7.4
PyJWT==2.11.0
email-validator==2.1.0
```

## Step 5: Setup Database Schema

After deploying, you have two options:

### Option A: Automatic Schema Setup (Recommended)

1. Create a setup script the first time only
2. Run it once via Render shell

### Option B: Manual Setup

1. Connect to PostgreSQL database (using pgAdmin or psql)
2. Run the SQL from `SCHEMA.sql` to create tables

## Step 6: Test Your Deployment

1. Visit your deployed service URL
2. Check the health endpoint: `https://your-service-url.render.com/api/health`
3. API Docs: `https://your-service-url.render.com/docs`

## Troubleshooting

### Build Fails with "No module named main"

**Solution**: Ensure the working directory is correct:
- Procfile should be in `backend/` directory
- OR use `cd backend && uvicorn main:app...` in start command

### Database Connection Error

**Solution**: 
- Verify all DB environment variables are set correctly
- Check firewall rules on Render PostgreSQL (should allow all IPs for simplicity)
- Test connection locally first

### JWT_SECRET Missing Error

**Solution**: 
- Generate a new secret using the command above
- Add to Render environment variables
- Redeploy

### Service Starting But No Response

**Solution**:
- Check logs: `Logs` tab in Render Dashboard
- Verify database is accessible
- Check if PORT and HOST are correctly set

## Important Security Notes

⚠️ **NEVER** commit `.env` file to GitHub
⚠️ **ALWAYS** use strong JWT_SECRET in production
⚠️ **NEVER** expose database credentials in code
✅ **Use** Render's environment variables feature
✅ **Enable** HTTPS (Render provides free SSL)
✅ **Set** proper CORS for your frontend URL

## Production Checklist

- [ ] JWT_SECRET is strong and unique
- [ ] NODE_ENV is set to `production`
- [ ] Database credentials are secure
- [ ] FRONTEND_URL points to your frontend domain
- [ ] `.env` is in `.gitignore`
- [ ] All environment variables are set in Render
- [ ] Database is backing up regularly
- [ ] Health endpoint responds successfully
- [ ] API documentation loads at `/docs`

## Rolling Back

If something goes wrong:

1. Check the logs in Render Dashboard
2. You can view previous deployments
3. Click "Deployments" and select a previous version
4. Click three dots → "Redeploy"

## Additional Resources

- [Render Documentation](https://render.com/docs)
- [PostgreSQL on Render](https://render.com/docs/databases)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Uvicorn Configuration](https://www.uvicorn.org/deployment/)
