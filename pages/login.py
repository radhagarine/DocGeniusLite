import streamlit as st
import sys
import os
import re
from time import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auth import login_user, register_user, check_authentication
from utils.styles import apply_custom_css, render_clickable_logo

st.set_page_config(
    page_title="Login | DocGenius",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def is_valid_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_strong_password(password):
    """Check password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r"\d", password):
        return False, "Password must contain at least one number"
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character"
    return True, ""

def render_auth_form():
    apply_custom_css()
    
    # Initialize attempt tracking in session state
    if 'login_attempts' not in st.session_state:
        st.session_state.login_attempts = 0
    if 'last_attempt_time' not in st.session_state:
        st.session_state.last_attempt_time = 0
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Add logo at the top of the login form
        render_clickable_logo(size="medium", center=True)
        
        st.markdown("""
            <div class="auth-container">
                <h1>{}</h1>
            </div>
        """.format("Create Account" if st.session_state.get('auth_mode') == 'register' else "Welcome Back"), 
        unsafe_allow_html=True)
        
        # Check if user is temporarily blocked
        current_time = time()
        if st.session_state.login_attempts >= 5 and current_time - st.session_state.last_attempt_time < 300:
            remaining_time = int(300 - (current_time - st.session_state.last_attempt_time))
            st.error(f"Too many login attempts. Please try again in {remaining_time} seconds.")
            return

        with st.form("auth_form"):
            email = st.text_input("Email", key="form_email")
            password = st.text_input("Password", type="password")
            
            if st.session_state.get('auth_mode') == 'register':
                name = st.text_input("Name", key="form_name")
                confirm_password = st.text_input("Confirm Password", type="password")
            
            submit_text = "Create Account" if st.session_state.get('auth_mode') == 'register' else "Login"
            
            if st.form_submit_button(submit_text, use_container_width=True):
                if not email or not password:
                    st.error("Please fill in all required fields")
                elif not is_valid_email(email):
                    st.error("Please enter a valid email address")
                else:
                    if st.session_state.get('auth_mode') == 'register':
                        if password != confirm_password:
                            st.error("Passwords do not match")
                        else:
                            is_strong, msg = is_strong_password(password)
                            if not is_strong:
                                st.error(msg)
                            else:
                                success, message = register_user(email, password, st.session_state.form_name)
                                if success:
                                    st.success(message)
                                    st.switch_page("pages/onboarding.py")
                                else:
                                    st.error(message)
                    else:
                        st.session_state.login_attempts += 1
                        st.session_state.last_attempt_time = current_time
                        
                        success, message = login_user(email, password)
                        if success:
                            st.session_state.login_attempts = 0
                            st.success(message)
                            st.switch_page("pages/0_Dashboard.py")
                        else:
                            st.error(message)
        
        # Toggle between login and register
        if st.session_state.get('auth_mode') == 'register':
            st.markdown("""
                <div style="text-align: center; margin-top: 1rem;">
                    Already have an account? 
                    <a href="?auth_mode=login" 
                       style="color: #3fd7a5; text-decoration: none;">Login</a>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style="text-align: center; margin-top: 1rem;">
                    Don't have an account? 
                    <a href="?auth_mode=register" 
                       style="color: #3fd7a5; text-decoration: none;">Create one</a>
                </div>
            """, unsafe_allow_html=True)

def main():
    # Set current page for sidebar highlighting
    st.session_state['current_page'] = __file__
    
    # Hide the sidebar for login/signup pages
    st.markdown("""
        <style>
        [data-testid="stSidebar"] {
            display: none;
        }
        section[data-testid="stSidebarUserContent"] {
            display: none;
        }
        </style>
    """, unsafe_allow_html=True)
    
    if 'auth_mode' not in st.session_state:
        st.session_state.auth_mode = 'login'
    
    if 'auth_mode' in st.query_params:
        st.session_state.auth_mode = st.query_params['auth_mode']
    
    if check_authentication():
        st.switch_page("pages/0_Dashboard.py")
    else:
        render_auth_form()

if __name__ == "__main__":
    main()