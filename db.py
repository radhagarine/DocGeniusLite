import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Database connection parameters from environment variables
DB_HOST = os.getenv("PGHOST", "localhost")
DB_NAME = os.getenv("PGDATABASE", "docgenius")
DB_USER = os.getenv("PGUSER", "postgres")
DB_PASSWORD = os.getenv("PGPASSWORD", "postgres")
DB_PORT = os.getenv("PGPORT", "5432")

def get_db_connection():
    """Create a connection to the PostgreSQL database"""
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )
    return conn

def init_db():
    """Initialize the database tables if they don't exist"""
    conn = get_db_connection()
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    
    # Create tables if they don't exist
    create_tables_query = """
    -- Users table
    CREATE TABLE IF NOT EXISTS users (
        id VARCHAR(36) PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        subscription VARCHAR(20) DEFAULT 'free',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Documents table
    CREATE TABLE IF NOT EXISTS documents (
        id VARCHAR(36) PRIMARY KEY,
        user_id VARCHAR(36) REFERENCES users(id),
        doc_type VARCHAR(50) NOT NULL,
        title VARCHAR(255) NOT NULL,
        content TEXT,
        parameters JSONB,
        rai_score FLOAT,
        rai_flags JSONB,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Payments table
    CREATE TABLE IF NOT EXISTS payments (
        id VARCHAR(36) PRIMARY KEY,
        user_id VARCHAR(36) REFERENCES users(id),
        amount DECIMAL(10, 2) NOT NULL,
        currency VARCHAR(3) DEFAULT 'USD',
        payment_type VARCHAR(20) NOT NULL,
        document_id VARCHAR(36) REFERENCES documents(id),
        status VARCHAR(20) DEFAULT 'pending',
        stripe_payment_id VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Document templates table (admin only)
    CREATE TABLE IF NOT EXISTS templates (
        id VARCHAR(36) PRIMARY KEY,
        doc_type VARCHAR(50) UNIQUE NOT NULL,
        name VARCHAR(255) NOT NULL,
        template TEXT NOT NULL,
        parameters JSONB NOT NULL,
        version INTEGER DEFAULT 1,
        is_active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Feedback table
    CREATE TABLE IF NOT EXISTS feedback (
        id VARCHAR(36) PRIMARY KEY,
        user_id VARCHAR(36) REFERENCES users(id),
        document_id VARCHAR(36) REFERENCES documents(id),
        rating INTEGER NOT NULL,
        comments TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    cursor.execute(create_tables_query)
    
    # Check if we need to insert default templates
    cursor.execute("SELECT COUNT(*) FROM templates")
    template_count = cursor.fetchone()[0]
    
    if template_count == 0:
        # Insert default templates (will be populated later with actual templates)
        doc_types = [
            "nda", 
            "invoice", 
            "letter_of_intent", 
            "proposal", 
            "scope_of_work"
        ]
        
        template_names = [
            "Non-Disclosure Agreement", 
            "Invoice", 
            "Letter of Intent", 
            "Business Proposal", 
            "Scope of Work"
        ]
        
        for i, doc_type in enumerate(doc_types):
            cursor.execute(
                """
                INSERT INTO templates (id, doc_type, name, template, parameters, version)
                VALUES (gen_random_uuid(), %s, %s, %s, %s, 1)
                """,
                (
                    doc_type, 
                    template_names[i], 
                    f"Default template for {template_names[i]}", 
                    '{}'  # Empty JSON for now
                )
            )
    
    cursor.close()
    conn.close()

def get_document_templates():
    """Get all active document templates"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, doc_type, name, parameters FROM templates WHERE is_active = TRUE"
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
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
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
        WHERE user_id = %s AND created_at >= CURRENT_DATE - INTERVAL %s DAY
        ORDER BY created_at DESC
        """,
        (user_id, retention_days)
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
        WHERE id = %s AND user_id = %s
        """,
        (doc_id, user_id)
    )
    
    document = cursor.fetchone()
    cursor.close()
    conn.close()
    return document

# Import uuid here for generating IDs
import uuid
