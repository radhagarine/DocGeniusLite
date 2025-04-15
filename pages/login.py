import streamlit as st
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.auth import login_user, register_user
from app import apply_custom_css

def render_login_form():
    st.markdown("""
        <div class="auth-header">
            <div class="logo-text">
                <span class="gradient-text">D</span>oc<span class="gradient-text">G</span>enius
            </div>
            <h2>Welcome Back</h2>
            <p>Enter your credentials to access your account</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("login_form", clear_on_submit=True):
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            remember_me = st.checkbox("Remember me")
        with col2:
            st.markdown('<div style="text-align: right"><a href="#" class="forgot-password">Forgot password?</a></div>', unsafe_allow_html=True)
        
        submit_button = st.form_submit_button("Sign In", use_container_width=True)
        
        if submit_button:
            if login_user(email, password):
                st.success("Login successful!")
                st.switch_page("pages/0_Dashboard.py")
            else:
                st.error("Invalid email or password")
    
    st.markdown("""
        <div class="social-login">
            <p>Or continue with</p>
            <div class="social-buttons">
                <button class="social-button google">
                    <img src="https://www.svgrepo.com/show/475656/google-color.svg" alt="Google">
                    Google
                </button>
                <button class="social-button microsoft">
                    <img src="https://www.svgrepo.com/show/452091/microsoft.svg" alt="Microsoft">
                    Microsoft
                </button>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Don't have an account? Create one", use_container_width=True):
            st.session_state.show_register = True
            st.rerun()

def render_register_form():
    st.markdown("""
        <div class="auth-header">
            <div class="logo-text">
                <span class="gradient-text">D</span>oc<span class="gradient-text">G</span>enius
            </div>
            <h2>Create Account</h2>
            <p>Get started with your free account</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("register_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name", placeholder="Enter your first name")
        with col2:
            last_name = st.text_input("Last Name", placeholder="Enter your last name")
            
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", type="password", placeholder="Create a password")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            terms = st.checkbox("I agree to the Terms of Service and Privacy Policy")
        
        submit_button = st.form_submit_button("Create Account", use_container_width=True)
        
        if submit_button:
            if not first_name or not last_name:
                st.error("Please enter your full name")
            elif not email:
                st.error("Please enter your email")
            elif not password:
                st.error("Please enter a password")
            elif password != confirm_password:
                st.error("Passwords do not match")
            elif not terms:
                st.error("Please accept the Terms of Service and Privacy Policy")
            else:
                full_name = f"{first_name} {last_name}"
                if register_user(email, password, full_name):
                    st.success("Account created successfully! Please sign in.")
                    st.session_state.show_register = False
                    # Clear URL parameters
                    st.experimental_set_query_params()
                    st.rerun()
                else:
                    st.error("Failed to create account. Email might already be registered.")
    
    st.markdown("""
        <div class="social-login">
            <p>Or sign up with</p>
            <div class="social-buttons">
                <button class="social-button google">
                    <img src="https://www.svgrepo.com/show/475656/google-color.svg" alt="Google">
                    Google
                </button>
                <button class="social-button microsoft">
                    <img src="https://www.svgrepo.com/show/452091/microsoft.svg" alt="Microsoft">
                    Microsoft
                </button>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Already have an account? Sign in", use_container_width=True):
            st.session_state.show_register = False
            # Clear URL parameters
            st.experimental_set_query_params()
            st.rerun()

def main():
    st.set_page_config(
        page_title="Sign In | DocGenius",
        page_icon="🔐",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    apply_custom_css()
    
    # Add authentication-specific styles
    st.markdown("""
        <style>
        /* Auth Container */
        .auth-container {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 2rem;
        }
        
        .auth-box {
            background: rgba(22, 68, 48, 0.3);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-radius: 24px;
            border: 1px solid rgba(63, 215, 165, 0.1);
            padding: 2.5rem;
            width: 100%;
            max-width: 480px;
            box-shadow: 
                0 10px 30px rgba(0, 0, 0, 0.1),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
        }
        
        /* Center the form on the page */
        [data-testid="stForm"] {
            max-width: 480px !important;
            margin: 2rem auto !important;
            padding: 2rem !important;
            background: rgba(22, 68, 48, 0.3) !important;
            backdrop-filter: blur(10px) !important;
            -webkit-backdrop-filter: blur(10px) !important;
            border-radius: 24px !important;
            border: 1px solid rgba(63, 215, 165, 0.1) !important;
            box-shadow: 
                0 10px 30px rgba(0, 0, 0, 0.1),
                inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
        }
        
        /* Style form inputs */
        [data-testid="stTextInput"] input {
            background: rgba(10, 40, 23, 0.3) !important;
            border: 1px solid rgba(63, 215, 165, 0.2) !important;
            color: #f4f9f7 !important;
        }
        
        [data-testid="stTextInput"] input:focus {
            border-color: #3fd7a5 !important;
            box-shadow: 0 0 0 1px #3fd7a5 !important;
        }
        
        /* Style buttons */
        .stButton button {
            background: linear-gradient(135deg, #3fd7a5 0%, #26856c 100%) !important;
            color: #f4f9f7 !important;
            border: none !important;
            transition: all 0.3s ease !important;
            transform-style: preserve-3d !important;
        }
        
        .stButton button:hover {
            transform: translateY(-2px) translateZ(10px) !important;
            box-shadow: 
                0 8px 25px rgba(63, 215, 165, 0.3),
                inset 0 2px 5px rgba(255, 255, 255, 0.3) !important;
        }
        
        /* Header styles */
        .auth-header {
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .logo-text {
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 1.5rem;
        }
        
        .gradient-text {
            background: linear-gradient(135deg, #3fd7a5 0%, #26856c 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .auth-header h2 {
            font-size: 1.8rem;
            margin-bottom: 0.5rem;
            color: #f4f9f7;
        }
        
        .auth-header p {
            color: rgba(244, 249, 247, 0.7);
            font-size: 1rem;
        }
        
        /* Social login styles */
        .social-login {
            text-align: center;
            margin: 2rem 0;
        }
        
        .social-buttons {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
            max-width: 480px;
            margin: 1rem auto;
        }
        
        .social-button {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
            padding: 0.75rem;
            background: rgba(10, 40, 23, 0.3);
            border: 1px solid rgba(63, 215, 165, 0.2);
            border-radius: 8px;
            color: #f4f9f7;
            font-size: 0.9rem;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .social-button:hover {
            transform: translateY(-2px);
            border-color: rgba(63, 215, 165, 0.4);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }
        
        .social-button img {
            width: 20px;
            height: 20px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'show_register' not in st.session_state:
        st.session_state.show_register = False
    
    # Add a button in the top right to switch to register
    col1, col2, col3 = st.columns([6, 2, 2])
    with col3:
        if not st.session_state.show_register:
            if st.button("Create Account", use_container_width=True):
                st.session_state.show_register = True
                st.rerun()
        else:
            if st.button("Sign In", use_container_width=True):
                st.session_state.show_register = False
                st.rerun()
    
    # Render appropriate form
    if st.session_state.show_register:
        render_register_form()
    else:
        render_login_form()

if __name__ == "__main__":
    main() 