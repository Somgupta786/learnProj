# Importing Dummy Data into the Database

## Method 1: Using PowerShell (Recommended)

Run this command in PowerShell from the backend folder:

```powershell
mysql -h localhost -u root -pSom@7866 ecommerce_db < DUMMY_DATA.sql
```

## Method 2: Using MySQL CLI Directly

1. Open MySQL Command Line Client
2. Connect to your database:
```sql
USE ecommerce_db;
```

3. Import the SQL file:
```sql
SOURCE DUMMY_DATA.sql;
```

## Method 3: Using MySQL Workbench

1. Open MySQL Workbench
2. Open the `DUMMY_DATA.sql` file
3. Click the execute button (⚡ icon) or press `Ctrl+Enter`

## Method 4: Execute in Python Script

Create a file `import_data.py` in the backend folder:

```python
import mysql.connector
from config.settings import DATABASE_URL

try:
    # Parse database URL
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'Som@7866',
        'database': 'ecommerce_db'
    }
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    # Read and execute SQL file
    with open('DUMMY_DATA.sql', 'r') as sql_file:
        sql_script = sql_file.read()
        
    # Split by semicolon and execute each statement
    statements = sql_script.split(';')
    for statement in statements:
        statement = statement.strip()
        if statement and not statement.startswith('--'):
            cursor.execute(statement)
            print(f"✓ Executed: {statement[:50]}...")
    
    conn.commit()
    print("\n✅ All dummy data imported successfully!")
    
except Exception as e:
    print(f"❌ Error importing data: {e}")
finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
```

Then run: `python import_data.py`

## Data Summary

The `DUMMY_DATA.sql` file includes:

### Users (5 total)
- ✅ 1 Admin account
- ✅ 4 Regular user accounts
- All emails: `admin@example.com`, `jane@example.com`, `robert@example.com`, `sarah@example.com`, `michael@example.com`
- Default password for all: `admin123` (bcrypt hashed)

### Products (20 total)
- ✅ 5 Electronics (Headphones, Cable, Power Bank, Speaker, Hub)
- ✅ 5 Clothing items (T-Shirt, Jeans, Shoes, Jacket, Socks)
- ✅ 5 Books (Python, Web Dev, Data Science, Cloud, AI)
- ✅ 5 Home items (Lamp, Cushions, Clock, Mat, Organizer)
- Price range: $14.99 - $149.99
- All with stock and descriptions

### Orders (6 total)
- ✅ Various statuses: delivered, shipped, processing, pending
- ✅ Realistic dates (30-60 days ago for older orders)
- ✅ Different users placed orders
- Total values: $89.98 - $349.97

### Order Items (19 total)
- ✅ Multiple items per order
- ✅ Realistic quantities and pricing
- ✅ Historical order data for testing

## Testing the Import

After importing, verify the data:

```sql
-- Check total records
SELECT COUNT(*) as total_users FROM users;
SELECT COUNT(*) as total_products FROM products;
SELECT COUNT(*) as total_orders FROM orders;
SELECT COUNT(*) as total_order_items FROM order_items;

-- View sample data
SELECT * FROM users LIMIT 5;
SELECT * FROM products LIMIT 5;
SELECT * FROM orders LIMIT 3;
```

## Testing the Application

### 1. Login with Admin Account
- Email: `admin@example.com`
- Password: `admin123`
- Access admin panel to manage products and orders

### 2. Login with Regular User
- Email: `jane@example.com`
- Password: `admin123`
- View existing orders and browse products

### 3. Test Features
- ✅ Browse products by category
- ✅ Search for products
- ✅ View order history
- ✅ Admin: Add new products
- ✅ Admin: Update order status
- ✅ Admin: View all orders

## Important Notes

⚠️ **Passwords**: All accounts use the same hashed password `admin123` for easy testing. For production, use different strong passwords.

⚠️ **Image URLs**: Products use placeholder images from `https://via.placeholder.com/`. Replace with actual images for production.

⚠️ **Data Reset**: If you want to clear and re-import:
```sql
DELETE FROM order_items;
DELETE FROM orders;
DELETE FROM products;
DELETE FROM users;
```

Then re-run the import.

---

If you encounter any issues, check:
1. MySQL is running
2. Database `ecommerce_db` exists
3. Tables are created (run `DATABASE_SCHEMA.sql` first if not)
4. User has correct credentials: `root` / `Som@7866`
