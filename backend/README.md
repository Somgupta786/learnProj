# Backend - FastAPI E-Commerce API

## Setup

1. Navigate to backend folder:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Setup MySQL Database:
- Create database: `ecommerce_db`
- Run the SQL script from `DATABASE_SCHEMA.sql`

5. Configure environment:
- Copy `.env.example` to `.env`
- Update database credentials and other settings

6. Run the server:
```bash
python main.py
```

Server runs on: http://localhost:8000
API docs: http://localhost:8000/docs

## Project Structure

```
backend/
├── config/              # Configuration files
│   ├── settings.py     # App settings
│   └── database.py     # Database connection
├── db/                 # Database operations
│   ├── user_db.py
│   ├── product_db.py
│   └── order_db.py
├── models/             # Pydantic models (schemas)
│   ├── user.py
│   ├── product.py
│   └── order.py
├── routes/             # API endpoints
│   ├── auth.py
│   ├── products.py
│   └── orders.py
├── middleware/         # Middleware
│   └── auth.py        # JWT authentication
├── utils/              # Utility functions
│   ├── validators.py
│   └── helpers.py
├── main.py            # FastAPI app entry point
├── requirements.txt
├── .env.example
└── DATABASE_SCHEMA.sql
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user

### Products
- `GET /api/products` - Get all products
- `GET /api/products/search` - Search products
- `GET /api/products/{id}` - Get product by ID
- `POST /api/products` - Create product (admin)
- `PUT /api/products/{id}` - Update product (admin)
- `DELETE /api/products/{id}` - Delete product (admin)

### Orders
- `POST /api/orders` - Create order
- `GET /api/orders` - Get user orders
- `GET /api/orders/{id}` - Get order by ID
- `GET /api/orders/admin/all` - Get all orders (admin)
- `PUT /api/orders/{id}/status` - Update order status (admin)
- `DELETE /api/orders/{id}` - Delete order (admin)

## Clean Code Principles

✓ Separation of concerns - Config, DB, Routes, Models
✓ Database abstraction - DB classes handle all queries
✓ Validation - Input validation in utils/validators.py
✓ Error handling - Consistent error responses
✓ Modular structure - Easy to extend and maintain
✓ JWT authentication - Secure token-based auth
✓ Type hints - Full Pydantic validation
