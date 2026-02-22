# E-Commerce Application (FastAPI + Streamlit)

A modular e-commerce app with a FastAPI backend and Streamlit frontend, designed for independent deployment and a MySQL database.

## Highlights
- Separate backend and frontend for independent deployment
- JWT authentication with role-based access (admin/user)
- Product browsing, search, orders, and admin management
- MySQL schema and seed data included

## Tech Stack
- Backend: FastAPI, Uvicorn, MySQL Connector
- Frontend: Streamlit, Requests
- Auth: JWT + bcrypt

## Project Structure
- backend/  FastAPI app (routes, models, db, middleware)
- frontend/ Streamlit app (app.py + pages/)
- docs and deployment guides in root

## Quick Start (Local)
1) Backend
- cd backend
- pip install -r requirements.txt
- python setup_db.py
- python main.py

2) Frontend
- cd frontend
- pip install -r requirements.txt
- streamlit run app.py

## Default Test Login
- admin@example.com / admin123

## Production Deployment
See:
- PRODUCTION_DEPLOYMENT.md
- DEPLOYMENT_QUICK_START.md

## Notes
- Update backend/.env with your DB credentials
- For production, use Render + Streamlit Cloud
