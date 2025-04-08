import streamlit as st
import os
from auth import check_authentication, login_page, logout
from db import init_db

# Page configuration
st.set_page_config(
    page_title="DocGenius Lite",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database on first run
init_db()

# App title and description
def main():
    # Check if user is authenticated
    if not check_authentication():
        login_page()
        return
    
    # Main page content (shown after login)
    st.title("DocGenius Lite")
    st.markdown("""
    ### Fast, reliable generation of professional business documents
    
    Welcome to DocGenius Lite - your document assistant for creating legally sound 
    and professional-looking business documents without technical knowledge or legal teams.
    
    **Get started by selecting an option from the sidebar →**
    """)
    
    # Display features in columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📝 Generate Documents")
        st.markdown("""
        - NDAs
        - Invoices
        - Letters of Intent
        - Proposals
        - Scope of Work
        """)
        st.button("Create New Document", type="primary", key="create_new_doc", 
                  on_click=lambda: st.switch_page("pages/1_Generate_Document.py"))
    
    with col2:
        st.markdown("### 📊 Your Document Stats")
        
        # Mock document stats (will be replaced with real data from database)
        free_docs_used = st.session_state.get('free_docs_used', 0)
        free_docs_limit = 3
        
        st.metric("Documents Created", st.session_state.get('total_docs', 0))
        st.progress(free_docs_used/free_docs_limit, 
                    f"Free documents this month: {free_docs_used}/{free_docs_limit}")
        
        if st.session_state.get('subscription') == 'pro':
            st.success("PRO Plan Active")
        else:
            st.info("Free Plan Active")
            if st.button("Upgrade to Pro", key="upgrade_btn"):
                st.switch_page("pages/3_Account.py")
    
    # Footer
    st.markdown("---")
    st.markdown("Need help? Check our [Help & Support](#) section")
    
    # Logout button in sidebar
    if st.sidebar.button("Logout"):
        logout()
        st.rerun()

if __name__ == "__main__":
    main()
