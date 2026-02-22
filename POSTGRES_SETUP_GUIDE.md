# PostgreSQL Setup Instructions for Windows

## Step 1: Download PostgreSQL

1. Go to [PostgreSQL Official Download Page](https://www.postgresql.org/download/windows/)
2. Download PostgreSQL 14 or higher for Windows
3. Run the installer (postgresql-15.x-windows-x64.exe or similar)

## Step 2: PostgreSQL Installation

During installation:
- **Installation Directory:** `C:\Program Files\PostgreSQL\15` (or default)
- **Port:** `5432` (default)
- **Password:** Set it to `Sh@250704` (or your preferred password)
- **Locale:** Default (English, United States)
- **Data Directory:** Default location

## Step 3: Start PostgreSQL Service

PostgreSQL service should start automatically after installation. Verify it's running:

```powershell
Get-Service | Select-String -Pattern "postgres"
```

If not running, start it:
```powershell
net start "postgresql-x64-15"
```

## Step 4: Create Database and Import Schema

Once PostgreSQL is installed and running, execute the setup script:

```powershell
cd "C:\Users\Sharad Pandey\learnProj\backend"
venv\Scripts\activate
python setup_postgres_db.py
```

This will:
- ✅ Create the `ecommerce_db` database
- ✅ Create all tables (users, products, orders, order_items)
- ✅ Insert 20 sample products
- ✅ Insert 5 sample users
- ✅ Insert 6 sample orders with 21 order items

## Step 5: Verify Database

Check the database in pgAdmin or psql:

```powershell
psql -U postgres -d ecommerce_db
```

Then run:
```sql
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM products;
SELECT COUNT(*) FROM orders;
SELECT COUNT(*) FROM order_items;
```

## Alternative: Using SQL Files

If you prefer manual setup, use the SQL files:

```powershell
psql -U postgres -c "CREATE DATABASE ecommerce_db"
psql -U postgres -d ecommerce_db -f POSTGRES_SCHEMA.sql
psql -U postgres -d ecommerce_db -f POSTGRES_DUMMY_DATA.sql
```

## Configuration

The .env file is already configured for PostgreSQL:
- **DB_HOST:** localhost
- **DB_USER:** postgres
- **DB_PASSWORD:** Sh@250704 (change if you set a different password)
- **DB_NAME:** ecommerce_db
- **DB_PORT:** 5432

## Files Created

- `POSTGRES_SCHEMA.sql` - PostgreSQL database schema
- `POSTGRES_DUMMY_DATA.sql` - Sample data
- `setup_postgres_db.py` - Automated setup script
- `config/database.py` - Updated for PostgreSQL (psycopg2)
- `config/settings.py` - Updated PostgreSQL connection string
- `requirements.txt` - Updated with psycopg2

## Run the Application

After database setup:

```powershell
# Terminal 1 - Backend
cd "C:\Users\Sharad Pandey\learnProj\backend"
venv\Scripts\activate
python main.py

# Terminal 2 - Frontend
cd "C:\Users\Sharad Pandey\learnProj\frontend"
venv\Scripts\activate
streamlit run app.py
```

## Test Accounts

- **admin@example.com** (Admin)
- **jane@example.com**
- **robert@example.com**
- **sarah@example.com**
- **michael@example.com**
- **Password:** admin123 for all accounts

## Troubleshooting

If you get connection errors:
1. Verify PostgreSQL is running: `Get-Service | grep postgres`
2. Check password is correct in .env file
3. Ensure port 5432 is accessible
4. Restart PostgreSQL service

## Uninstall MySQL (Optional)

If you want to remove MySQL:
```powershell
Get-WmiObject Win32_Product | Where-Object { $_.Name -match "mysql" } | ForEach-Object { $_.Uninstall() }
```
