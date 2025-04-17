import streamlit as st
import base64
import os
import uuid
from datetime import datetime, timedelta
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db import get_db_connection

def format_date(date_obj):
    """Format a date object as a readable string"""
    if not date_obj:
        return ""
    return date_obj.strftime("%B %d, %Y")

def can_create_document():
    """Check if the user can create a new document based on their plan and usage"""
    # Pro users can always create documents
    if st.session_state.get('subscription') == 'pro':
        return True, None
    
    # Free users get 3 free documents per month
    free_docs_used = st.session_state.get('free_docs_used', 0)
    if free_docs_used < 3:
        return True, None
    
    return False, "You've reached your free document limit for this month. Purchase this document or upgrade to Pro."

def get_document_display_name(doc_type):
    """Convert document type to display name"""
    display_names = {
        "nda": "Non-Disclosure Agreement",
        "invoice": "Invoice",
        "letter_of_intent": "Letter of Intent",
        "proposal": "Business Proposal",
        "scope_of_work": "Scope of Work"
    }
    return display_names.get(doc_type, doc_type.replace("_", " ").title())

def get_document_description(doc_type):
    """Get a description for a document type"""
    descriptions = {
        "nda": "A legal contract that establishes a confidential relationship between parties. Used when sensitive information needs to be shared but protected from others.",
        "invoice": "A commercial document issued by a seller to a buyer, indicating the products, quantities, and agreed prices for products or services provided.",
        "letter_of_intent": "A document outlining the understanding between parties that wish to enter into a contract. It sets forth the main terms of a deal.",
        "proposal": "A document that offers a solution to a client's problem. Often used in business to suggest services or products to meet specific needs.",
        "scope_of_work": "A document that defines project-specific activities, deliverables, and timelines for a vendor providing services to a client."
    }
    return descriptions.get(doc_type, "")

def create_download_link(file_path, link_text):
    """Create a download link for a file"""
    with open(file_path, "rb") as f:
        file_bytes = f.read()
    
    b64 = base64.b64encode(file_bytes).decode()
    filename = os.path.basename(file_path)
    
    return f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">{link_text}</a>'

def display_rai_indicator(score, flags=None):
    """Display a Responsible AI indicator with the given score"""
    # Determine color based on score
    if score >= 0.8:
        color = "green"
        label = "High Trust"
    elif score >= 0.6:
        color = "orange"
        label = "Medium Trust"
    else:
        color = "red"
        label = "Low Trust"
    
    # Create the indicator
    st.markdown(f"""
    <div style="display: inline-block; padding: 0.3em 0.6em; border-radius: 0.25em; 
                background-color: {color}; color: white; font-weight: bold;">
        {label} ({score:.2f})
    </div>
    """, unsafe_allow_html=True)
    
    # Display flags if provided
    if flags:
        with st.expander("View RAI Details"):
            st.markdown("### Responsible AI Analysis")
            
            # Bias indicator
            bias_level = flags.get("bias", {}).get("level", "low")
            bias_score = flags.get("bias", {}).get("score", 0)
            
            st.markdown(f"**Bias Detection:** {bias_level.title()} ({bias_score:.2f})")
            if bias_level == "high":
                st.warning("The document may contain language that shows strong preferences or prejudices.")
            elif bias_level == "medium":
                st.info("Some language in the document may show subtle preferences.")
            else:
                st.success("The document appears to use neutral language.")
            
            # Hallucination indicator
            hallucination = flags.get("hallucination", "low")
            st.markdown(f"**Hallucination Risk:** {hallucination.title()}")
            if hallucination == "high":
                st.warning("The document may contain unverifiable claims or assertions.")
            elif hallucination == "medium":
                st.info("Some claims in the document may benefit from verification.")
            else:
                st.success("The document appears to contain verifiable information.")
            
            # Security indicator
            security = flags.get("security", "low")
            st.markdown(f"**Security Risk:** {security.title()}")
            if security == "high":
                st.warning("The document may contain sensitive information that requires protection.")
            elif security == "medium":
                st.info("The document contains some information that should be handled with care.")
            else:
                st.success("The document appears to contain minimal sensitive information.")

def get_user_credits(user_id):
    """Get user's current credit balance"""
    if not user_id:
        return 0
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT ai_credits, subscription FROM users WHERE id = ?",
        (user_id,)
    )
    result = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if result:
        credits, subscription = result
        return float('inf') if subscription == 'pro' else credits
    return 0

def calculate_required_credits(doc_type, word_count=None):
    """Calculate required credits for document generation"""
    base_credits = {
        'nda': 5,
        'invoice': 3,
        'letter_of_intent': 4,
        'proposal': 8,
        'scope_of_work': 10
    }
    
    # Base credit cost for the document type
    required_credits = base_credits.get(doc_type, 5)
    
    # Additional credits based on complexity/length if word count provided
    if word_count:
        required_credits += max(0, (word_count - 500) // 250)
    
    return required_credits

def deduct_credits(user_id, amount, document_id, description):
    """Deduct credits from user's balance and record the transaction"""
    if not user_id:
        return False
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Start transaction
        cursor.execute("BEGIN")
        
        # Update user's credit balance
        cursor.execute(
            """
            UPDATE users 
            SET ai_credits = ai_credits - ?,
                total_credits_used = total_credits_used + ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ? AND subscription != 'pro'
            RETURNING ai_credits
            """,
            (amount, amount, user_id)
        )
        
        result = cursor.fetchone()
        if not result:
            # User is either not found or is on pro plan
            cursor.execute("ROLLBACK")
            return True
        
        new_balance = result[0]
        if new_balance < 0:
            # Insufficient credits
            cursor.execute("ROLLBACK")
            return False
        
        # Record the transaction
        cursor.execute(
            """
            INSERT INTO credit_transactions 
            (id, user_id, amount, transaction_type, document_id, description, created_at)
            VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """,
            (str(uuid.uuid4()), user_id, -amount, 'deduction', document_id, description)
        )
        
        # Update document with credits used if document_id provided
        if document_id:
            cursor.execute(
                """
                UPDATE documents
                SET credits_used = ?
                WHERE id = ?
                """,
                (amount, document_id)
            )
        
        cursor.execute("COMMIT")
        
        # Update session state
        st.session_state["ai_credits"] = new_balance
        st.session_state["total_credits_used"] = st.session_state.get("total_credits_used", 0) + amount
        
        return True
        
    except Exception as e:
        cursor.execute("ROLLBACK")
        raise e
    finally:
        cursor.close()
        conn.close()

def add_credits(user_id, amount, description, transaction_type='purchase'):
    """Add credits to user's balance and record the transaction"""
    if not user_id:
        return False
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("BEGIN")
        
        # Update user's credit balance
        cursor.execute(
            """
            UPDATE users 
            SET ai_credits = ai_credits + ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ? AND subscription != 'pro'
            RETURNING ai_credits
            """,
            (amount, user_id)
        )
        
        result = cursor.fetchone()
        if not result:
            cursor.execute("ROLLBACK")
            return False
            
        new_balance = result[0]
        
        # Record the transaction
        cursor.execute(
            """
            INSERT INTO credit_transactions 
            (id, user_id, amount, transaction_type, description, created_at)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """,
            (str(uuid.uuid4()), user_id, amount, transaction_type, description)
        )
        
        cursor.execute("COMMIT")
        
        # Update session state
        st.session_state["ai_credits"] = new_balance
        
        return True
        
    except Exception as e:
        cursor.execute("ROLLBACK")
        raise e
    finally:
        cursor.close()
        conn.close()

def get_credit_history(user_id, limit=10):
    """Get user's credit transaction history"""
    if not user_id:
        return []
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        """
        SELECT 
            ct.amount,
            ct.transaction_type,
            ct.description,
            ct.created_at,
            d.title as document_title
        FROM credit_transactions ct
        LEFT JOIN documents d ON ct.document_id = d.id
        WHERE ct.user_id = ?
        ORDER BY ct.created_at DESC
        LIMIT ?
        """,
        (user_id, limit)
    )
    
    transactions = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return transactions

def get_document_count(user_id):
    """Get total number of documents generated by a user"""
    if not user_id:
        return 0
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT COUNT(*) FROM documents WHERE user_id = ?",
        (user_id,)
    )
    count = cursor.fetchone()[0]
    
    cursor.close()
    conn.close()
    
    return count

def get_user_storage_used(user_id):
    """Calculate the total storage used by a user's documents in MB"""
    if not user_id:
        return 0
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Get the sum of content lengths (in bytes)
        cursor.execute(
            """
            SELECT SUM(LENGTH(content)) as total_bytes
            FROM documents
            WHERE user_id = ?
            """,
            (user_id,)
        )
        
        result = cursor.fetchone()
        total_bytes = result[0] if result[0] is not None else 0
        
        # Convert bytes to megabytes (1 MB = 1,048,576 bytes)
        storage_mb = total_bytes / 1048576.0
        
        return round(storage_mb, 2)  # Round to 2 decimal places
        
    except Exception as e:
        print(f"Error calculating storage: {str(e)}")
        return 0
    finally:
        cursor.close()
        conn.close()

def get_recent_documents(user_id, limit=5):
    """Get user's most recent documents"""
    if not user_id:
        return []
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        """
        SELECT 
            id,
            title,
            doc_type,
            created_at,
            credits_used,
            status
        FROM documents 
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT ?
        """,
        (user_id, limit)
    )
    
    documents = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return [dict(d) for d in documents]