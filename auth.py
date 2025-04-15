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
    st.markdown("""
        <style>
        /* Navigation Links Override */
        .nav-container .nav-links a,
        .nav-link,
        .hero-cta,
        .launch-button,
        div.nav-links > a {
            color: #f4f9f7 !important;
            text-decoration: none !important;
            transition: all 0.3s ease;
        }
        
        .nav-container .nav-links a:hover,
        .nav-link:hover,
        .hero-cta:hover {
            color: #3fd7a5 !important;
            transform: translateY(-1px);
        }
        
        /* Streamlit Element Overrides */
        .stMarkdown a,
        .streamlit-expanderHeader,
        [data-testid="stMarkdownContainer"] a,
        .element-container a,
        div[data-testid="stMarkdownContainer"] p a,
        .stMarkdown p a {
            color: #f4f9f7 !important;
            text-decoration: none !important;
            transition: all 0.3s ease;
        }
        
        /* Header Link Override */
        h1 a, h2 a, h3 a, h4 a, h5 a, h6 a,
        [data-testid="stHeaderLink"] {
            color: #f4f9f7 !important;
            text-decoration: none !important;
        }
        
        /* Form Elements Override */
        .stTextInput label,
        .stCheckbox label,
        .stButton label,
        div[data-testid="stForm"] label {
            color: #f4f9f7 !important;
        }
        
        /* Link Hover Effects */
        a:hover,
        .stMarkdown a:hover,
        .element-container a:hover {
            color: #3fd7a5 !important;
            text-decoration: none !important;
        }
        
        /* 3D Container Effect */
        .login-container {
            max-width: 400px;
            margin: 4rem auto;
            padding: 2.5rem;
            background: rgba(22, 68, 48, 0.3);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-radius: 16px;
            border: 1px solid rgba(63, 215, 165, 0.1);
            box-shadow: 
                0 10px 20px rgba(0, 0, 0, 0.2),
                0 5px 15px rgba(63, 215, 165, 0.1),
                inset 0 0 10px rgba(63, 215, 165, 0.05);
            transform-style: preserve-3d;
            perspective: 1000px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        /* Login Header Styles */
        .login-header {
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .login-title {
            color: #f4f9f7;
            font-size: 1.5rem;
            margin-bottom: 0.5rem;
            font-weight: 600;
        }
        
        .login-subtitle {
            color: rgba(244, 249, 247, 0.7);
            font-size: 0.9rem;
        }
        
        /* Social Login Section */
        .social-login {
            margin-top: 2rem;
            text-align: center;
            padding-top: 2rem;
            border-top: 1px solid rgba(63, 215, 165, 0.1);
        }
        
        .social-login-text {
            color: rgba(244, 249, 247, 0.7);
            font-size: 0.9rem;
            margin-bottom: 1rem;
        }
        
        /* Sign Up Prompt */
        .signup-prompt {
            margin-top: 2rem;
            text-align: center;
            color: rgba(244, 249, 247, 0.7) !important;
            font-size: 0.9rem;
        }
        
        /* Success/Error Messages Override */
        .stSuccess,
        .stError {
            color: #f4f9f7 !important;
            background: rgba(22, 68, 48, 0.3) !important;
            border: 1px solid rgba(63, 215, 165, 0.2) !important;
        }
        
        /* Hide Streamlit's Default Elements */
        #MainMenu,
        footer,
        header[data-testid="stHeader"] {
            display: none !important;
        }
        
        /* Override any remaining blue focus rings */
        *:focus {
            outline-color: #3fd7a5 !important;
        }
        
        /* Override default selection color */
        ::selection {
            background: rgba(63, 215, 165, 0.3);
            color: #f4f9f7;
        }
        </style>
    """, unsafe_allow_html=True)

    # Render the login container
    st.markdown("""
        <div class="login-container">
            <div class="login-header">
                <div class="login-logo">DG</div>
                <h1 class="login-title">Welcome back</h1>
                <p class="login-subtitle">Sign in to continue to DocGenius Lite</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Login form
    with st.form("login_form"):
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        # Remember me and Forgot password row
        col1, col2 = st.columns([1, 1])
        with col1:
            remember = st.checkbox("Remember me")
        with col2:
            st.markdown('<div style="text-align: right;"><a href="#" class="helper-link">Forgot password?</a></div>', unsafe_allow_html=True)
        
        submit = st.form_submit_button("Sign in")
        
        if submit and email and password:
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
            st.session_state['free_docs_used'] = 0
            st.session_state['total_docs'] = 0
            
            st.success("Login successful!")
            st.rerun()
        elif submit:
            st.error("Please enter both email and password")

    # Social login section
    st.markdown("""
        <div class="social-login">
            <p class="social-login-text">Or continue with</p>
            <div class="social-buttons">
                <a href="#" class="social-button">
                    <img src="https://www.google.com/favicon.ico" width="18" height="18" alt="Google">
                    Google
                </a>
                <a href="#" class="social-button">
                    <img src="https://www.microsoft.com/favicon.ico" width="18" height="18" alt="Microsoft">
                    Microsoft
                </a>
            </div>
        </div>
        <div class="signup-prompt">
            Don't have an account? <a href="#" class="signup-link">Create a free account</a>
        </div>
    """, unsafe_allow_html=True)

def logout():
    """Log out the user by clearing the session state"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
