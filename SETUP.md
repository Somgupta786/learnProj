# E-Commerce Application - Setup Instructions

## Quick Start Guide

### Prerequisites
- Python 3.9+
- MySQL Server
- pip (Python package manager)

---

## 📁 Project Structure

```
HCLAgain/
├── backend/                  # FastAPI Backend Server
│   ├── config/              # Configuration files
│   ├── db/                  # Database operations
│   ├── models/              # Pydantic schemas
│   ├── routes/              # API endpoints
│   ├── middleware/          # Authentication
│   ├── utils/               # Validators and helpers
│   ├── main.py              # FastAPI entry point
│   ├── requirements.txt
│   ├── .env.example
│   └── DATABASE_SCHEMA.sql
│
└── frontend/                # Streamlit Frontend
    ├── src/
    │   ├── pages/           # Application pages
    │   ├── components/      # Reusable components
    │   └── utils/           # Helper functions
    ├── services/
    │   └── api.py           # API client
    ├── config.py
    ├── requirements.txt
    └── README.md
```

---

## 🗄️ Step 1: Setup MySQL Database

1. **Create database:**
```sql
CREATE DATABASE ecommerce_db;
```

2. **Import schema:**
```bash
mysql -u root -p ecommerce_db < backend/DATABASE_SCHEMA.sql
```

---

## 🔧 Step 2: Setup Backend (FastAPI)

1. **Navigate to backend:**
```bash
cd backend
```

2. **Create virtual environment:**
```bash
python -m venv venv
# Activate on Windows:
venv\Scripts\activate
# Activate on macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment:**
```bash
cp .env.example .env
# Edit .env with your MySQL credentials
# DB_HOST=localhost
# DB_USER=root
# DB_PASSWORD=your_password
# DB_NAME=ecommerce_db
```

5. **Run backend:**
```bash
python main.py
```

✅ Backend runs on: **http://localhost:8000**
- API Docs: http://localhost:8000/docs

---

## 🎨 Step 3: Setup Frontend (Streamlit)

1. **Open new terminal, navigate to frontend:**
```bash
cd frontend
```

2. **Create virtual environment:**
```bash
python -m venv venv
# Activate on Windows:
venv\Scripts\activate
# Activate on macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Create .env file:**
```bash
echo API_URL=http://localhost:8000/api > .env
```

5. **Run frontend:**
```bash
streamlit run src/pages/00_Home.py
```

✅ Frontend runs on: **http://localhost:8501**

---

## 🚀 Deployment Guide

### Backend Deployment

#### Docker (Recommended)
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Deploy on AWS/GCP/Azure
- Build image and push to container registry
- Deploy as Cloud Run, App Engine, or EC2

#### Environment Variables
```
DB_HOST=your-db-host
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_NAME=ecommerce_db
JWT_SECRET=your-secret-key
FRONTEND_URL=https://your-frontend-url
```

### Frontend Deployment

#### Streamlit Cloud (Easiest)
1. Push code to GitHub
2. Connect repo to Streamlit Cloud
3. Deploy automatically

#### Docker Deployment
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY frontend/requirements.txt .
RUN pip install -r requirements.txt

COPY frontend/ .

CMD ["streamlit", "run", "src/pages/00_Home.py", "--server.port=8501"]
```

#### Environment Variables
```
API_URL=https://your-backend-api-url/api
```

---

## 📚 Tech Stack

### Backend
- **Framework:** FastAPI
- **Database:** MySQL
- **Authentication:** JWT
- **Validation:** Pydantic
- **Server:** Uvicorn

### Frontend
- **Framework:** Streamlit
- **HTTP Client:** Requests
- **State Management:** Streamlit Session State

---

## 🔐 Security Notes

1. **Change JWT secret** in production:
```
JWT_SECRET=your-very-secure-change-this-key
```

2. **Use HTTPS** in production

3. **Database credentials** - Use environment variables (never commit .env)

4. **CORS** - Configure allowed origins in backend

5. **Password hashing** - Using bcrypt

---

## 🧪 Testing

### Backend API Testing
```bash
# Using curl
curl http://localhost:8000/api/health

# Using Python requests
python -c "import requests; print(requests.get('http://localhost:8000/api/health').json())"
```

### Frontend Testing
- Navigate to http://localhost:8501
- Test login/register
- Browse products
- Place orders

---

## 📝 Code Quality

✅ **Modular Structure** - Separation of concerns
✅ **Clean Code** - Well-organized, readable
✅ **Error Handling** - Consistent error responses
✅ **Validation** - Input validation on both ends
✅ **Type Hints** - Full type annotations
✅ **Documentation** - Clear comments

---

## 📞 Support

For issues or questions:
1. Check README files in each folder
2. Review API documentation at /docs (backend)
3. Check error logs in terminal output

---

## 📄 License

This project is open source and available under the MIT License.
