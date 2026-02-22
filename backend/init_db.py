#!/usr/bin/env python
"""Initialize the Render PostgreSQL database with schema"""

import psycopg2
from config.settings import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT

# Read the schema file
with open('SCHEMA.sql', 'r') as f:
    schema_sql = f.read()

print('[INFO] Connecting to Render PostgreSQL database...')
try:
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT,
        connect_timeout=15
    )
    cursor = conn.cursor()
    
    print('[INFO] Running schema SQL...')
    cursor.execute(schema_sql)
    conn.commit()
    
    print('[OK] Schema created successfully!')
    
    # Verify tables were created
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name
    """)
    tables = cursor.fetchall()
    print(f'[OK] Created {len(tables)} tables:')
    for table in tables:
        print(f'     - {table[0]}')
    
    cursor.close()
    conn.close()
    print('[OK] Database initialization complete!')
    
except Exception as e:
    print(f'[ERROR] {str(e)}')
    import traceback
    traceback.print_exc()
