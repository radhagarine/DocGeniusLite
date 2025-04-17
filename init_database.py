import sqlite3
import os

def init_db():
    # Create database directory if it doesn't exist
    db_path = 'docgenius.db'
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        email TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        password_hash TEXT NOT NULL,
        subscription TEXT DEFAULT 'free',
        ai_credits INTEGER DEFAULT 50,
        total_credits_used INTEGER DEFAULT 0,
        onboarding_completed BOOLEAN DEFAULT FALSE,
        industry TEXT,
        company_description TEXT,
        business_type TEXT,
        company_name TEXT,
        team_size TEXT,
        doc_types TEXT,
        company_logo TEXT,
        business_address TEXT,
        business_phone TEXT,
        business_email TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Add missing columns if they don't exist
    cursor.execute("PRAGMA table_info(users)")
    columns = [column[1] for column in cursor.fetchall()]
    
    # Check and add each column if it doesn't exist
    for field, default in [
        ('onboarding_completed', 'BOOLEAN DEFAULT 0'),
        ('industry', 'TEXT'),
        ('business_type', 'TEXT'),
        ('company_description', 'TEXT'),
        ('company_name', 'TEXT'),
        ('team_size', 'TEXT'),
        ('doc_types', 'TEXT'),
        ('company_logo', 'TEXT'),
        ('business_address', 'TEXT'),
        ('business_phone', 'TEXT'),
        ('business_email', 'TEXT'),
        ('updated_at', 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
    ]:
        if field not in columns:
            cursor.execute(f"ALTER TABLE users ADD COLUMN {field} {default}")
    
    # Create documents table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        type TEXT NOT NULL,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        parameters TEXT,
        credits_used INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)
    
    # Create credit_history table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS credit_history (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        document_id TEXT,
        credits INTEGER NOT NULL,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (document_id) REFERENCES documents (id)
    )
    """)
    
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    init_db()