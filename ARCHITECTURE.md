# Production Architecture & Deployment Diagram

## 🏗️ Production Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      END USER / BROWSER                          │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
                    ▼                         ▼
    ┌──────────────────────────┐   ┌──────────────────────────┐
    │   Streamlit Cloud        │   │    HTTPS                 │
    │  https://app.streamlit   │◄──┤  (Encrypted)             │
    │      .app                │   └──────────────────────────┘
    │                          │
    │  Frontend Application    │
    │  - React-like UI         │
    │  - Login/Auth            │
    │  - Product Browse        │
    │  - Order Management      │
    │                          │
    └────────────┬─────────────┘
                 │
        ┌────────┴──────────┐
        │ API_URL Secret    │
        │ (Stored in Cloud) │
        └────────┬──────────┘
                 │
        ┌────────▼──────────┐
        │ https://api       │
        │ .onrender.com/api │
        └────────┬──────────┘
                 │
                 ▼
    ┌──────────────────────────┐
    │   Render (Backend)       │
    │  https://api.onrender    │   
    │      .com                │
    │                          │
    │ FastAPI Application      │
    │ - /api/auth              │
    │ - /api/products          │
    │ - /api/orders            │
    │ - JWT Authentication     │
    │                          │
    └────────────┬─────────────┘
                 │
        ┌────────▼──────────┐
        │ Environment Vars  │
        │ (Stored in Cloud) │
        └────────┬──────────┘
                 │
                 ▼
    ┌──────────────────────────┐
    │    MySQL Database        │
    │  (Render/Planetscale/    │
    │   AWS RDS)               │
    │                          │
    │ Tables:                  │
    │ - users                  │
    │ - products               │
    │ - orders                 │
    │ - order_items            │
    │                          │
    └──────────────────────────┘
```

---

## 📊 Data Flow Diagram

### User Login Flow
```
User enters credentials
        │
        ▼
[Frontend] POST /api/auth/login
        │
        ▼
[Backend] Hash password & verify
        │
        ├─ Valid? ──YES──> Generate JWT token
        │                        │
        └─ Invalid? ─YES─> Return 401 Error
                                 │
        ┌────────────────────────┘
        │
        ▼
Return JWT in response
        │
        ▼
Frontend stores JWT in session
        │
        ▼
Include JWT in future API requests
```

### Product Fetch Flow
```
User clicks "Products" page
        │
        ▼
[Frontend] GET /api/products?page=1&limit=10
           (Include JWT in Authorization header)
        │
        ▼
[Backend] Verify JWT token
        │
        ├─ Valid? ──YES──> Query database
        │                        │
        └─ Invalid?── YES──> Return 401 Unauthorized
                            │
        ┌──────────────────┘
        │
        ▼
Fetch products from MySQL
        │
        ▼
Return JSON with products list
        │
        ▼
Frontend receives & displays products
```

---

## 🔄 Deployment Flow

### Local Development → Production

```
┌─────────────────────┐
│  Your Local Machine │
│                     │
│  • Write code       │
│  • Test locally     │
│  • Commit changes   │
└──────────┬──────────┘
           │
           │ git push origin main
           │
           ▼
┌─────────────────────┐
│  GitHub Repository  │
│                     │
│  • Stores code      │
│  • Version control  │
│  • Webhook triggers │
└──┬─────────────────┬┘
   │                 │
   │ (Webhook fired) │
   │                 │
   ▼                 ▼
┌─────────────────────────┐  ┌──────────────────────┐
│  Render (Backend)       │  │ Streamlit Cloud      │
│                         │  │ (Frontend)           │
│ • Pulls latest code     │  │                      │
│ • Installs dependencies │  │ • Pulls latest code  │
│ • Runs build command    │  │ • Installs packages  │
│ • Starts server         │  │ • Deploys app        │
│ (3-5 minutes)          │  │ (1-2 minutes)        │
└──────────┬──────────────┘  └──────────┬───────────┘
           │                           │
           ▼                           ▼
        Live!                       Live!
```

---

## 🔐 Security Architecture

```
┌─────────────────────────────────────────────────────────┐
│              HTTPS/SSL Encryption Layer                 │
│   (All communication between user & backend encrypted)  │
└──────────────┬──────────────────────┬──────────────────┘
               │                      │
        Frontend                   Backend
        (Streamlit Cloud)          (Render)
               │                      │
          Secrets:                Environment:
          • API_URL                • DB_HOST
                                   • DB_USER
                                   • DB_PASSWORD
                                   • JWT_SECRET (32+ chars)
                                   • FRONTEND_URL (CORS)
                                   • NODE_ENV=production

               │                      │
               │   REQUEST: GET /api/products
               │   Header: Authorization: Bearer <JWT_TOKEN>
               ├─────────────────────>│
               │                      │
               │   ✓ JWT verified     │
               │   ✓ Query database   │
               │   ✓ Return products  │
               │   RESPONSE: 200 OK   │
               │<─────────────────────┤
               │                      │
```

---

## 📈 System Components

### Frontend (Streamlit Cloud)
```
Frontend/
├── Entry: app.py
├── Config: config.py (reads Streamlit secrets)
├── Pages:
│   ├── Home (Login/Register)
│   ├── Products (Browse & Search)
│   ├── Orders (View Orders)
│   └── Admin (Manage Products)
└── Secrets:
    └── API_URL = "https://your-api.onrender.com/api"
```

### Backend (Render)
```
Backend/
├── Entry: main.py
├── Routes:
│   ├── /auth (login, register)
│   ├── /products (CRUD + search)
│   └── /orders (CRUD with auth)
├── Database Layer (db/)
│   ├── user_db.py
│   ├── product_db.py
│   └── order_db.py
├── Models (models/)
│   ├── user.py
│   ├── product.py
│   └── order.py
└── Environment:
    ├── DB_HOST, DB_USER, DB_PASSWORD
    ├── JWT_SECRET
    ├── FRONTEND_URL (CORS)
    └── NODE_ENV=production
```

### Database (MySQL)
```
ecommerce_db/
├── users
│   ├── id (PK)
│   ├── email (UNIQUE)
│   ├── password (bcrypt hashed)
│   ├── role (user/admin)
│   └── timestamps
├── products
│   ├── id (PK)
│   ├── name
│   ├── price, stock, category
│   └── timestamps
├── orders
│   ├── id (PK)
│   ├── user_id (FK → users)
│   ├── total_amount, status
│   └── timestamps
└── order_items
    ├── id (PK)
    ├── order_id (FK → orders)
    ├── product_id (FK → products)
    └── quantity, price
```

---

## 🔑 Environment Variables

### On Render Dashboard
```
DB_HOST = your-db-host.com
DB_USER = your_db_user
DB_PASSWORD = your_strong_password_32_chars
DB_NAME = ecommerce_db
DB_PORT = 3306
NODE_ENV = production
JWT_SECRET = your_unique_secret_key_at_least_32_chars
FRONTEND_URL = https://your-app-abc123.streamlit.app
```

### On Streamlit Cloud Dashboard (Secrets)
```toml
API_URL = "https://your-ecommerce-api.onrender.com/api"
```

---

## 🚀 Deployment Timeline

**Phase 1: Preparation** (30 min)
- Create GitHub account & repository
- Create MySQL database
- Set up credentials

**Phase 2: Backend Deployment** (10 min active, 3-5 min build)
- Create Render account
- Set environment variables
- Deploy (build + start)
- Test health endpoint

**Phase 3: Frontend Deployment** (5 min active, 1-2 min build)
- Create Streamlit account
- Connect GitHub
- Add API_URL secret
- Deploy

**Phase 4: Testing** (15 min)
- Test backend API
- Test frontend UI
- Test authentication
- Test all features

**Total Time: ~2 hours** (including deployment waits)

---

## 📊 Traffic Flow Example

### API Request Sequence
```
1. User @ Browser
   └─ Types admin@example.com, password "admin123"

2. Frontend sends POST request
   POST https://api.onrender.com/api/auth/login
   {
     "email": "admin@example.com",
     "password": "admin123"
   }

3. Backend receives request
   └─ Hashes password with bcrypt
   └─ Compares with DB stored hash
   └─ If match: Generate JWT token

4. Backend returns response
   {
     "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
     "user": {
       "id": 1,
       "email": "admin@example.com",
       "role": "admin"
     }
   }

5. Frontend stores token
   └─ Saves in Streamlit session_state

6. Future requests include token
   GET https://api.onrender.com/api/products
   Headers: {
     "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
   }

7. Backend verifies token
   └─ Checks signature with JWT_SECRET
   └─ Extracts user info

8. Backend returns data
   {
     "products": [...],
     "pagination": {...}
   }

9. Frontend displays results
```

---

## ✅ Health Checks

### Backend Health
```
GET https://your-api.onrender.com/api/health

Response:
{
  "status": "Server is running",
  "environment": "production"
}
```

### Database Health
Check from backend logs - if database connection works, DB is healthy

### Frontend Health
- Page loads in browser
- Can reach https://your-app.streamlit.app
- Can see login page

---

## 🔄 Update Cycle

```
Day 1: Deploy
  └─ Backend live
  └─ Frontend live
  └─ Database populated

Day 2+: Updates
  └─ Make code changes locally
  └─ Push to GitHub
     ├─ Render auto-rebuilds (3-5 min)
     └─ Streamlit auto-redeploys (1-2 min)
  └─ No downtime! (blue-green deployment)
```

---

## 🎯 Scaling Considerations

### If You Need More Power
- **Render Backend**: Upgrade plan (free → pro → business)
- **Streamlit Cloud**: Auto-scales with usage
- **Database**: Add replicas for read scaling

### If You Need More Storage
- **Database**: Upgrade storage tier
- **Backups**: Enable automated backups

### If You Need Better Performance
- **CDN**: Add CloudFlare for frontend
- **Caching**: Add Redis layer (future)
- **Database Optimization**: Add indexes

---

## 🎉 Architecture Complete!

Your e-commerce application with:
- ✅ Secure HTTPS communication
- ✅ JWT token-based authentication
- ✅ Auto-deployments from GitHub
- ✅ Scalable microservices architecture
- ✅ Professional production deployment

**Ready to go live!** 🚀
