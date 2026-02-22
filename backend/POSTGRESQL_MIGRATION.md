# PostgreSQL Migration Guide

## Migration Overview
Your e-commerce application has been successfully migrated from MySQL to PostgreSQL. All necessary code changes, configuration updates, and database schema modifications have been completed.

---

## 🔄 Changes Made

### 1. **Dependencies** ([backend/requirements.txt](backend/requirements.txt))
- ❌ Removed: `mysql-connector-python==8.2.0`
- ✅ Added: `psycopg2-binary==2.9.6` (already present)
- ✅ Added: `sqlalchemy==2.0.23` (already present)

### 2. **Database Configuration** ([backend/config/database.py](backend/config/database.py))
- Replaced `mysql.connector` with `psycopg2`
- Implemented connection pooling using `psycopg2.pool.SimpleConnectionPool`
- Added `initialize_connection_pool()` function for startup
- Changed connection parameters format for PostgreSQL
- Pool size: 1-20 connections (configurable)

### 3. **Settings** ([backend/config/settings.py](backend/config/settings.py))
- Database host: same (localhost)
- Database user: `root` → `postgres` (PostgreSQL default)
- **Database port: 3306 → 5432** (PostgreSQL default port)
- Connection string format: `postgresql://user:pass@host:port/db` (from `mysql+pymysql://...`)

### 4. **Database Operations** (All files in [backend/db/](backend/db/))

#### [backend/db/user_db.py](backend/db/user_db.py)
- Import: `import psycopg2.extras`
- Cursor type: `RealDictCursor` for dict-like row access
- Insert: Changed from `cursor.lastrowid` to `RETURNING id` clause
- Example: `INSERT INTO users (...) VALUES (...) RETURNING id`

#### [backend/db/product_db.py](backend/db/product_db.py)
- Same cursor and INSERT changes as user_db
- Search function: `LIKE` → `ILIKE` (PostgreSQL case-insensitive search)
- All `cursor.lastrowid` replaced with `RETURNING id`

#### [backend/db/order_db.py](backend/db/order_db.py)
- Same cursor and INSERT changes as above
- Connection management compatible with psycopg2 pooling

### 5. **Database Schema** ([backend/SCHEMA.sql](backend/SCHEMA.sql))
PostgreSQL-specific changes:
- `INT AUTO_INCREMENT` → `SERIAL` (auto-incrementing)
- `TIMESTAMP ON UPDATE CURRENT_TIMESTAMP` → `TIMESTAMP DEFAULT CURRENT_TIMESTAMP`
- `INDEX idx_name (column)` → `CREATE INDEX IF NOT EXISTS idx_name ON table(column)`
- All indexes moved outside table definitions (PostgreSQL syntax)

### 6. **Main Application** ([backend/main.py](backend/main.py))
- Added startup event: `@app.on_event("startup")`
- Automatically calls `initialize_connection_pool()` when app starts
- Ensures connection pool is ready before handling requests

### 7. **Environment Configuration**
- [backend/.env](backend/.env): Updated with PostgreSQL defaults
- [backend/.env.example](backend/.env.example): Created comprehensive template file

### 8. **Dummy Data** ([backend/DUMMY_DATA.sql](backend/DUMMY_DATA.sql))
- `DATE_SUB(NOW(), INTERVAL 30 DAY)` → `NOW() - INTERVAL '30 days'` (PostgreSQL syntax)
- Clear data: `DELETE` → `TRUNCATE ... CASCADE`
- All date calculations updated for PostgreSQL

---

## 📋 Setup Instructions

### 1. Install PostgreSQL
**Windows**: Download from [postgresql.org](https://www.postgresql.org/download/windows/)

**Linux**:
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
```

**macOS**:
```bash
brew install postgresql
```

### 2. Create Database and User
```sql
-- Connect to PostgreSQL as superuser
psql -U postgres

-- Create database
CREATE DATABASE ecommerce_db;

-- Create user (if not using default postgres)
CREATE USER your_user WITH PASSWORD 'your_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE ecommerce_db TO your_user;
ALTER ROLE your_user SUPERUSER;
```

### 3. Run Database Schema
```bash
# Navigate to backend directory
cd backend

# Create tables (as postgres user or your configured user)
psql -U postgres -d ecommerce_db -f SCHEMA.sql

# Insert dummy data
psql -U postgres -d ecommerce_db -f DUMMY_DATA.sql
```

### 4. Configure Environment
Update [backend/.env](backend/.env):
```env
DB_HOST=localhost
DB_USER=postgres                    # or your_user
DB_PASSWORD=Som@7866               # your password
DB_NAME=ecommerce_db
DB_PORT=5432                        # PostgreSQL default
```

### 5. Reinstall Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 6. Start the Application
```bash
# Development
python main.py

# Or with uvicorn
uvicorn main:app --reload
```

---

## 🔍 Verification Queries

After setup, verify your data with these queries:

```sql
-- Check users
SELECT COUNT(*) as total_users FROM users;

-- Check products by category
SELECT category, COUNT(*) FROM products GROUP BY category;

-- Check orders
SELECT status, COUNT(*) FROM orders GROUP BY status;

-- Check order items
SELECT COUNT(*) as total_order_items FROM order_items;

-- Sample product search
SELECT * FROM products WHERE name ILIKE '%headphones%' LIMIT 5;
```

---

## 🚀 Deployment Notes

### For Render Backend Deployment

1. **Create PostgreSQL database on Render**:
   - Create a Postgres database service
   - Note the internal database URL

2. **Update environment variables** in Render:
   ```
   DB_HOST=<your-database-host>
   DB_USER=<your-database-user>
   DB_PASSWORD=<your-database-password>
   DB_NAME=<your-database-name>
   DB_PORT=5432
   ```

3. **Run migrations on Render**:
   - Connect to your Render database via psql
   - Run SCHEMA.sql and DUMMY_DATA.sql

### For Local Development

- Use the provided [.env.example](backend/.env.example) as a template
- Keep [.env](backend/.env) updated with your local PostgreSQL credentials
- PostgreSQL runs on port 5432 by default

---

## ⚠️ Important Notes

1. **Port Change**: PostgreSQL uses port **5432** instead of MySQL's 3306
2. **Case Sensitivity**: PostgreSQL treats unquoted identifiers as lowercase
3. **Connection Pooling**: 
   - Automatically initialized on app startup
   - Pool size: 1-20 connections
   - Returns connections to pool (not closed)
4. **RETURNING Clause**: All INSERT operations now use RETURNING for ID retrieval
5. **Dictionary Cursors**: All queries return dict-like objects for easier data handling

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| `psycopg2.OperationalError: could not translate host name` | Check DB_HOST in .env, ensure PostgreSQL is running |
| `FATAL: password authentication failed` | Verify DB_USER and DB_PASSWORD in .env |
| `database "ecommerce_db" does not exist` | Run SCHEMA.sql to create the database |
| `connection pool is not initialized` | Check that startup event runs (look for ✓ log message) |
| `42P01: relation "users" does not exist` | Ensure SCHEMA.sql was executed in correct database |

---

## 📚 PostgreSQL Documentation
- [psycopg2 Documentation](https://www.psycopg.org/)
- [PostgreSQL Official Docs](https://www.postgresql.org/docs/)
- [Connection Pooling Guide](https://www.psycopg.org/psycopg3/basic/index.html#connection-pools)

---

## ✅ Migration Checklist

- [x] Requirements updated
- [x] Database configuration switched to psycopg2
- [x] All database operations updated for PostgreSQL
- [x] Schema converted to PostgreSQL syntax
- [x] Connection pooling implemented
- [x] Environment configuration prepared
- [x] Dummy data updated for PostgreSQL
- [x] Changes committed to git
- [ ] PostgreSQL installed locally/on server
- [ ] Database created on PostgreSQL
- [ ] SCHEMA.sql executed
- [ ] DUMMY_DATA.sql loaded (optional)
- [ ] .env configured with PostgreSQL credentials
- [ ] Application tested with PostgreSQL

---

## 📞 Support

For issues or questions about the migration:
1. Check PostgreSQL logs: `sudo tail -f /var/log/postgresql/postgresql.log`
2. Test connection: `psql -U postgres -h localhost -d ecommerce_db -c "SELECT 1"`
3. Verify app can connect: Check terminal output for "✓ Connection pool initialized"
