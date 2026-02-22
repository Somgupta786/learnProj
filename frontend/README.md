# Frontend - Streamlit E-Commerce Application

## Setup

1. Navigate to frontend folder:
```bash
cd frontend
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

4. Create `.env` file in frontend folder:
```
API_URL=http://localhost:8000/api
```

5. Run the Streamlit app:
```bash
streamlit run app.py
```

App runs on: http://localhost:8501

## Project Structure

```
frontend/
├── src/
│   ├── pages/              # Streamlit pages
│   │   ├── 00_Home.py     # Home page (login/register)
│   │   ├── 01_Products.py # Browse products
│   │   ├── 02_Orders.py   # View orders
│   │   └── 03_Admin.py    # Admin panel
│   ├── components/         # Reusable components
│   │   └── product_display.py
│   ├── utils/              # Utility functions
│   │   └── auth.py        # Authentication helpers
│   └── styles/             # CSS/styling
├── services/
│   └── api.py             # API client
├── config.py              # App configuration
├── app.py                 # Main Streamlit app
├── requirements.txt
└── README.md
```

## Pages

### Home (00_Home)
- User login/registration
- Authentication flow

### Products (01_Products)
- Browse all products
- Search functionality
- Filter by category
- Pagination

### Orders (02_Orders)
- View user's orders
- Order status tracking
- Order details

### Admin Panel (03_Admin)
- Product management (CRUD)
- Order management
- Dashboard (future)

## Clean Code Principles

✓ Reusable components - Product display, cart display
✓ Service layer - API client for all backend calls
✓ Auth utilities - Centralized authentication logic
✓ Session management - Streamlit session state
✓ Error handling - User-friendly error messages
✓ Modular pages - Each page has single responsibility
✓ Config management - Centralized configuration

## Features

- User authentication (login/register)
- Product browsing and search
- Shopping cart (session-based)
- Order management
- Order tracking
- Admin product management
- Admin order management
- Responsive UI using Streamlit columns
