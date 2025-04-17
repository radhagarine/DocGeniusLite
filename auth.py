import streamlit as st
import bcrypt
import jwt
from datetime import datetime, timedelta
import uuid
from db import get_db_connection

# JWT configuration
JWT_SECRET = "your-secret-key"  # In production, use environment variable
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24

def init_user_db():
    """Initialize the user database if it doesn't exist"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create users table if it doesn't exist (moved to db.py init_db())
    cursor.close()
    conn.close()

def hash_password(password):
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed):
    """Verify a password against its hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_jwt_token(user_id, email):
    """Create a JWT token for a user"""
    expiration = datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
    return jwt.encode(
        {
            "user_id": user_id,
            "email": email,
            "exp": expiration
        },
        JWT_SECRET,
        algorithm=JWT_ALGORITHM
    )

def verify_jwt_token(token):
    """Verify a JWT token"""
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except:
        return None

def register_user(email, password, name):
    """Register a new user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if user exists
        cursor.execute("SELECT email FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            return False, "Email already registered"
        
        # Create new user with default credits
        user_id = str(uuid.uuid4())
        hashed_password = hash_password(password)
        
        cursor.execute(
            """
            INSERT INTO users (id, email, name, password_hash, subscription, ai_credits, total_credits_used)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (user_id, email, name, hashed_password, 'free', 50, 0)
        )
        
        conn.commit()
        
        # Create and store session
        token = create_jwt_token(user_id, email)
        st.session_state["token"] = token
        st.session_state["authenticated"] = True
        st.session_state["user_id"] = user_id
        st.session_state["email"] = email
        st.session_state["name"] = name
        st.session_state["subscription"] = "free"
        st.session_state["ai_credits"] = 50
        st.session_state["total_credits_used"] = 0
        
        return True, "Registration successful"
        
    except Exception as e:
        return False, str(e)
    finally:
        cursor.close()
        conn.close()

def login_user(email, password):
    """Login a user with improved error handling"""
    if not email or not password:
        return False, "Email and password are required"
        
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        
        if not user:
            return False, "Email not found"
            
        if not verify_password(password, user['password_hash']):
            return False, "Invalid password"
            
        # Set session state with all user data with all user data
        st.session_state.user_id = user['id']
        st.session_state.user_email = user['email']
        st.session_state.email = user['email']  # Add both versions for compatibilityemail = user['email']  # Add both versions for compatibility
        st.session_state.user_name = user['name']
        st.session_state.name = user['name']  # Add both versions for compatibility
        st.session_state.credits = user['ai_credits']
        st.session_state.ai_credits = user['ai_credits']
        st.session_state.subscription = user['subscription']
        st.session_state.total_credits_used = user['total_credits_used']
        st.session_state.onboarding_completed = bool(user['onboarding_completed'])
        st.session_state.authenticated = True
        
        # Load all onboarding data into session state
        for field in ['industry', 'business_type', 'company_description', 'company_name',
                     'team_size', 'doc_types', 'company_logo', 'business_address',
                     'business_phone', 'business_email']:
            if field in user and user[field]:
                st.session_state[field] = user[field]
        st.session_state.user_name = user['name']
        st.session_state.name = user['name']  # Add both versions for compatibility
        st.session_state.credits = user['ai_credits']
        st.session_state.ai_credits = user['ai_credits']
        st.session_state.subscription = user['subscription']
        st.session_state.total_credits_used = user['total_credits_used']
        st.session_state.onboarding_completed = bool(user['onboarding_completed'])
        st.session_state.authenticated = True
        
        # Load all onboarding data into session state
        for field in ['industry', 'business_type', 'company_description', 'company_name',
                     'team_size', 'doc_types', 'company_logo', 'business_address',
                     'business_phone', 'business_email']:
            if field in user and user[field]:
                st.session_state[field] = user[field]
        
        # Create and set JWT token
        token = create_jwt_token(user['id'], user['email'])
        st.session_state.token = token
        
        return True, "Login successful"
    except Exception as e:
        return False, f"Login error: {str(e)}"
    finally:
        cursor.close()
        conn.close()

def logout():
    """Log out the user by clearing the session state"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]

def check_authentication():
    """Check if a user is authenticated"""
    if not st.session_state.get("authenticated"):
        return False
    
    token = st.session_state.get("token")
    if not token:
        return False
    
    claims = verify_jwt_token(token)
    if not claims:
        logout()
        return False
    
    return True

def get_user_info():
    """Get current user's information"""
    if not check_authentication():
        return None
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            """
            SELECT id, email, name, subscription, ai_credits, total_credits_used,
                   industry, business_type, company_description, company_name,
                   team_size, doc_types, company_logo, business_address,
                   business_phone, business_email, onboarding_completed
            FROM users WHERE id = ?
            """,
            (st.session_state["user_id"],)
        )
        user = cursor.fetchone()
        
        if not user:
            return None
            
        # Return all user fields
        user_data = {}
        for key in user.keys():
            user_data[key] = user[key]
        return user_data
    finally:
        cursor.close()
        conn.close()

def get_user_stats():
    """Get current user's statistics"""
    if not check_authentication():
        return None
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            """
            SELECT email, name, subscription, ai_credits, total_credits_used
            FROM users WHERE id = ?
            """,
            (st.session_state["user_id"],)
        )
        user = cursor.fetchone()
        
        if not user:
            return None
        
        # Get document count
        cursor.execute(
            """
            SELECT COUNT(*) as doc_count
            FROM documents 
            WHERE user_id = ? AND created_at >= DATE('now', '-30 days')
            """,
            (st.session_state["user_id"],)
        )
        doc_count = cursor.fetchone()['doc_count']
        
        return {
            "email": user['email'],
            "name": user['name'],
            "subscription": user['subscription'],
            "ai_credits": user['ai_credits'],
            "total_credits_used": user['total_credits_used'],
            "total_docs": doc_count
        }
    finally:
        cursor.close()
        conn.close()

def update_user_stats(user_id, stats):
    """Update user statistics"""
    if not user_id:
        return False
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Start transaction
        cursor.execute("BEGIN")
        
        # Build update query dynamically based on provided stats
        valid_fields = {
            "subscription", "ai_credits", "total_credits_used"
        }
        
        updates = []
        params = []
        for key, value in stats.items():
            if key in valid_fields:
                updates.append(f"{key} = ?")
                params.append(value)
        
        if not updates:
            return False
            
        # Add user_id to params
        params.append(user_id)
        
        # Execute update
        cursor.execute(
            f"""
            UPDATE users 
            SET {', '.join(updates)}
            WHERE id = ?
            """,
            params
        )
        
        # Update session state
        for key, value in stats.items():
            if key in valid_fields:
                st.session_state[key] = value
        
        cursor.execute("COMMIT")
        return True
        
    except Exception as e:
        cursor.execute("ROLLBACK")
        return False
    finally:
        cursor.close()
        conn.close()

def update_user_info(user_id, data):
    """Update user information"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Build the update query dynamically based on provided fields
        update_fields = []
        values = []
        
        valid_fields = [
            'name', 'subscription', 'ai_credits', 'total_credits_used',
            'industry', 'business_type', 'company_description',
            'company_name', 'team_size', 'doc_types', 'company_logo',
            'business_address', 'business_phone', 'business_email',
            'onboarding_completed'
        ]
        
        for field in valid_fields:
            if field in data:
                update_fields.append(f"{field} = ?")
                values.append(data[field])
        
        if not update_fields:
            return False
            
        # Add user_id to values
        values.append(user_id)
        
        # Execute update
        cursor.execute(
            f"""
            UPDATE users 
            SET {', '.join(update_fields)}
            WHERE id = ?
            """,
            tuple(values)
        )
        
        conn.commit()
        return True
        
    except Exception as e:
        print(f"Error updating user info: {str(e)}")
        return False
    finally:
        cursor.close()
        conn.close()

def delete_user(user_id):
    """Delete a user account and all associated data"""
    if not user_id:
        return False, "Invalid user ID"
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Start transaction
        cursor.execute("BEGIN")
        
        # Delete credit transactions
        cursor.execute(
            "DELETE FROM credit_transactions WHERE user_id = ?",
            (user_id,)
        )
        
        # Delete documents
        cursor.execute(
            "DELETE FROM documents WHERE user_id = ?",
            (user_id,)
        )
        
        # Delete industry profile if exists
        cursor.execute(
            "DELETE FROM industry_profiles WHERE user_id = ?",
            (user_id,)
        )
        
        # Finally, delete the user
        cursor.execute(
            "DELETE FROM users WHERE id = ?",
            (user_id,)
        )
        
        # Commit all changes
        cursor.execute("COMMIT")
        return True, "Account successfully deleted"
        
    except Exception as e:
        cursor.execute("ROLLBACK")
        return False, f"Error deleting account: {str(e)}"
    finally:
        cursor.close()
        conn.close()

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
            success, message = login_user(email, password)
            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)
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
