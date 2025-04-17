import streamlit as st
import sys
import os
from auth import check_authentication, login_page, logout
from db import init_db, upgrade_db
from utils.styles import apply_custom_css, render_clickable_logo
from utils.sidebar import create_sidebar

def ensure_database():
    """Ensure database is properly initialized and upgraded"""
    try:
        init_db()
        upgrade_db()
    except Exception as e:
        st.error(f"Database initialization failed: {str(e)}")
        st.stop()

# Initialize and upgrade database before anything else
ensure_database()

# Page configuration
st.set_page_config(
    page_title="DocGenius | AI-Powered Document Management",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply the custom CSS
apply_custom_css()

def main():
    # Set current page for sidebar highlighting
    st.session_state['current_page'] = __file__
    
    # Create sidebar
    create_sidebar()
    
    if not check_authentication():
        # Show landing page by redirecting to the new landing page
        st.switch_page("pages/landing.py")
    else:
        # Redirect to dashboard
        st.switch_page("pages/0_Dashboard.py")

if __name__ == "__main__":
    main()
    # Use: streamlit run app.py --server.port=8501
