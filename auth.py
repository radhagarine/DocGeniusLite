import streamlit as st
import jwt
import datetime
import os
import uuid
from db import get_db_connection

# Secret key for JWT (in production, this would be an environment variable)
JWT_SECRET = os.getenv("JWT_SECRET", "docgenius_lite_secret_key")
JWT_ALGORITHM = "HS256"
SESSION_EXPIRY_DAYS = 7

def generate_jwt_token(user_id, email, subscription="free"):
    """Generate a JWT token for authenticated users"""
    payload = {
        "user_id": user_id,
        "email": email,
        "subscription": subscription,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=SESSION_EXPIRY_DAYS)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

def verify_jwt_token(token):
    """Verify a JWT token"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def check_authentication():
    """Check if the user is authenticated"""
    if 'token' not in st.session_state:
        return False
    
    payload = verify_jwt_token(st.session_state['token'])
    if not payload:
        return False
    
    # Set session variables from token
    st.session_state['user_id'] = payload['user_id']
    st.session_state['email'] = payload['email']
    st.session_state['subscription'] = payload['subscription']
    
    # Get usage info from database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get current month's document count
    current_month = datetime.datetime.now().strftime('%Y-%m')
    cursor.execute(
        """
        SELECT COUNT(*) FROM documents 
        WHERE user_id = %s AND created_at >= %s::date
        """, 
        (st.session_state['user_id'], f"{current_month}-01")
    )
    st.session_state['free_docs_used'] = cursor.fetchone()[0]
    
    # Get total document count
    cursor.execute(
        "SELECT COUNT(*) FROM documents WHERE user_id = %s", 
        (st.session_state['user_id'],)
    )
    st.session_state['total_docs'] = cursor.fetchone()[0]
    
    cursor.close()
    conn.close()
    
    return True

def login_page():
    """Display the login page"""
    st.title("DocGenius Lite")
    st.markdown("### Log in to access document generation")
    
    # Simulated social login (in a real app, this would integrate with Google/Microsoft OAuth)
    with st.expander("Login with Email", expanded=True):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        
        if st.button("Log In"):
            if email and password:  # Basic validation
                # Check if user exists in database
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT id, email, subscription FROM users WHERE email = %s",
                    (email,)
                )
                user = cursor.fetchone()
                
                if not user:
                    # For demo, auto-create the user
                    user_id = str(uuid.uuid4())
                    cursor.execute(
                        """
                        INSERT INTO users (id, email, subscription, created_at) 
                        VALUES (%s, %s, %s, %s)
                        """,
                        (user_id, email, "free", datetime.datetime.now())
                    )
                    conn.commit()
                    
                    # Set the user for the session
                    user = (user_id, email, "free")
                
                cursor.close()
                conn.close()
                
                # Generate token and store in session
                token = generate_jwt_token(user[0], user[1], user[2])
                st.session_state['token'] = token
                
                # Set basic session data
                st.session_state['user_id'] = user[0]
                st.session_state['email'] = user[1]
                st.session_state['subscription'] = user[2]
                st.session_state['free_docs_used'] = 0  # Will be updated on page reload
                st.session_state['total_docs'] = 0  # Will be updated on page reload
                
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Please enter email and password")
    
    # Simulated social login buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login with Google", key="google_login"):
            st.info("Google login would be implemented here")
    with col2:
        if st.button("Login with Microsoft", key="ms_login"):
            st.info("Microsoft login would be implemented here")
    
    # Sign up option
    st.markdown("---")
    st.markdown("Don't have an account? Sign up with email or social login")

def logout():
    """Log out the user by clearing the session state"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
