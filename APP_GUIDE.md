# 🛍️ E-Commerce Application - User Guide

## ✅ What's Working

### 1. **Authentication** ✅
- Login/Register on Home page
- JWT token-based authentication
- Session management

### 2. **Products** ✅
- Browse all products with images (placeholder images from placeholder.com)
- Search products
- Filter by category
- Pagination support

### 3. **Database** ✅
- Remote PostgreSQL on Render.com
- 5 test users ready to use
- 20+ products with prices and stock

### 4. **Orders** ✅
- Backend supports order creation
- Track your orders
- Admin can manage orders

---

## 🔑 Test Credentials

All test users have password: **`admin123`**

### Admin Account (Access Admin Panel):
```
Email: admin@example.com
Password: admin123
```

### Regular User Accounts:
- jane@example.com
- robert@example.com
- sarah@example.com
- michael@example.com

---

## 🖼️ Product Images

**Status**: ✅ Working (Placeholder images)

Products display placeholder images from `https://via.placeholder.com/`. These are temporary placeholder images. To use real images:

1. Update product image URLs in admin panel
2. Or manually update in database:
```sql
UPDATE products SET image_url = 'your_image_url' WHERE id = 1;
```

---

## ⚙️ Admin Panel Access

**How to Access:**
1. Go to Home page (🏠)
2. Login with: `admin@example.com` / `admin123`
3. Go to Admin page (⚙️)
4. You can now:
   - View all products
   - Create new products
   - Edit existing products
   - Delete products
   - Manage orders
   - View dashboard

---

## 📦 Placing Orders

**Note**: Order UI is available in the backend API but not fully integrated in the frontend yet.

**To place an order** (via API):
```bash
POST http://localhost:8000/api/orders/
Authorization: Bearer {your_jwt_token}

{
  "items": [
    {"product_id": 61, "quantity": 1},
    {"product_id": 62, "quantity": 2}
  ],
  "total_amount": 160.97,
  "shipping_address": "123 Main St, City, State 12345"
}
```

**To view your orders:**
- Go to Orders page (📦)
- Must be logged in
- Shows all your orders with status and details

---

## 🔗 Important URLs

| Component | URL | Status |
|-----------|-----|--------|
| Frontend | http://localhost:8501 | ✅ Running |
| Backend API | http://localhost:8000 | ✅ Running |
| Database | Render PostgreSQL | ✅ Connected |

---

## 📝 Next Steps to Complete

To add ordering UI to frontend:
1. Add "Buy Now" button on products page
2. Create cart functionality for multiple items
3. Checkout form with shipping address
4. Order confirmation page

Frontend file to update: `frontend/pages/02_🛍️_Products.py`

---

## ❓ Troubleshooting

### Images not showing?
- Reload the page (F5)
- Check browser console for CORS errors
- Placeholder images should load from internet

### Can't access admin panel?
- Make sure you're logged in first
- Use admin@example.com account
- Check that role is "admin" in database

### Orders page shows error?
- Make sure you're logged in
- Backend must be running
- Check network tab in browser console

---

**Last Updated**: February 22, 2026
**Backend**: FastAPI + PostgreSQL
**Frontend**: Streamlit
