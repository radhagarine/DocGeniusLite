import os
import sqlite3
from datetime import datetime

# Database file path
DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'docgenius.db')

def get_db_connection():
    """Create a connection to the SQLite database"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def upgrade_db():
    """Upgrade database schema with new columns"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Start transaction
        cursor.execute("BEGIN")
        
        # Check existing columns in users table
        cursor.execute("PRAGMA table_info(users)")
        columns = {column[1] for column in cursor.fetchall()}
        
        # Add name column if it doesn't exist
        if 'name' not in columns:
            cursor.execute("""
                ALTER TABLE users 
                ADD COLUMN name TEXT DEFAULT 'User'
            """)
        
        # Add password_hash column if it doesn't exist
        if 'password_hash' not in columns:
            cursor.execute("""
                ALTER TABLE users 
                ADD COLUMN password_hash TEXT
            """)
        
        # Add ai_credits column if it doesn't exist
        if 'ai_credits' not in columns:
            cursor.execute("""
                ALTER TABLE users 
                ADD COLUMN ai_credits INTEGER DEFAULT 50
            """)
            
            cursor.execute("""
                ALTER TABLE users 
                ADD COLUMN total_credits_used INTEGER DEFAULT 0
            """)
            
            # Update existing users to have default credits
            cursor.execute("""
                UPDATE users 
                SET ai_credits = 50,
                    total_credits_used = 0 
                WHERE ai_credits IS NULL
            """)
            
        # Add onboarding fields if they don't exist
        for field in ['onboarding_completed', 'industry', 'business_type', 'company_description',
                      'company_name', 'team_size', 'doc_types', 'company_logo',
                      'business_address', 'business_phone', 'business_email',
                      'theme_preference', 'default_doc_type', 'notification_preferences']:
            if field not in columns:
                cursor.execute(f"""
                    ALTER TABLE users 
                    ADD COLUMN {field} TEXT
                """)
                
        # Add updated_at column if it doesn't exist
        if 'updated_at' not in columns:
            cursor.execute("""
                ALTER TABLE users 
                ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            """)
        
        # Create credit_transactions table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS credit_transactions (
                id TEXT PRIMARY KEY,
                user_id TEXT REFERENCES users(id),
                amount INTEGER NOT NULL,
                transaction_type TEXT NOT NULL,
                document_id TEXT REFERENCES documents(id),
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Check if credits_used column exists in documents table
        cursor.execute("PRAGMA table_info(documents)")
        columns = {column[1] for column in cursor.fetchall()}
        
        if 'credits_used' not in columns:
            cursor.execute("""
                ALTER TABLE documents 
                ADD COLUMN credits_used INTEGER DEFAULT 0
            """)
        
        cursor.execute("COMMIT")
        
    except Exception as e:
        cursor.execute("ROLLBACK")
        raise e
    finally:
        cursor.close()
        conn.close()

def init_db():
    """Initialize database with required tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Start transaction
        cursor.execute("BEGIN")
        
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
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                onboarding_completed BOOLEAN DEFAULT FALSE,
                industry TEXT,
                business_type TEXT,
                company_description TEXT,
                company_name TEXT,
                team_size TEXT,
                doc_types TEXT,
                company_logo TEXT,
                business_address TEXT,
                business_phone TEXT,
                business_email TEXT,
                theme_preference TEXT DEFAULT 'System',
                default_doc_type TEXT DEFAULT 'nda',
                notification_preferences TEXT
            )
        """)
        
        # Create industry_profiles table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS industry_profiles (
                user_id TEXT PRIMARY KEY REFERENCES users(id),
                industry TEXT NOT NULL,
                company_size TEXT,
                business_type TEXT,
                target_market TEXT,
                company_description TEXT,
                document_preferences TEXT,
                brand_colors TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create documents table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id TEXT PRIMARY KEY,
                user_id TEXT REFERENCES users(id),
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                doc_type TEXT NOT NULL,
                credits_used INTEGER DEFAULT 0,
                status TEXT DEFAULT 'completed',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("COMMIT")
        
    except Exception as e:
        cursor.execute("ROLLBACK")
        raise e
    finally:
        cursor.close()
        conn.close()

def get_document_templates():
    """Get all active document templates"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, doc_type, name, parameters FROM templates WHERE is_active = 1"
    )
    templates = cursor.fetchall()
    cursor.close()
    conn.close()
    return templates

def save_document(user_id, doc_type, title, content, parameters, rai_score, rai_flags):
    """Save a document to the database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    doc_id = str(uuid.uuid4())
    
    cursor.execute(
        """
        INSERT INTO documents 
        (id, user_id, doc_type, title, content, parameters, rai_score, rai_flags)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        RETURNING id
        """,
        (doc_id, user_id, doc_type, title, content, parameters, rai_score, rai_flags)
    )
    
    doc_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return doc_id

def get_user_documents(user_id, limit=30):
    """Get user's documents with retention period limit"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Limiting to documents created in the last 30 days
    retention_days = 30
    cursor.execute(
        """
        SELECT id, doc_type, title, created_at, rai_score
        FROM documents
        WHERE user_id = ? AND created_at >= DATE('now', '-30 days')
        ORDER BY created_at DESC
        """,
        (user_id,)
    )
    
    documents = cursor.fetchall()
    cursor.close()
    conn.close()
    return documents

def get_document_by_id(doc_id, user_id):
    """Get a document by ID for a specific user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        """
        SELECT id, doc_type, title, content, parameters, rai_score, rai_flags, created_at
        FROM documents
        WHERE id = ? AND user_id = ?
        """,
        (doc_id, user_id)
    )
    
    document = cursor.fetchone()
    cursor.close()
    conn.close()
    return document

# Import uuid here for generating IDs
import uuid
