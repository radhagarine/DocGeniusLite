import streamlit as st
from auth import logout, check_authentication
from utils.styles import render_clickable_logo

def create_sidebar():
    """Create a sidebar menu for the application"""
    with st.sidebar:
        # Apply custom CSS to hide default sidebar nav items
        st.markdown("""
        <style>
        [data-testid="stSidebarNavItems"] {
            display: none !important;
            visibility: hidden !important;
            height: 0 !important;
            position: absolute !important;
            top: 0 !important;
            left: 0 !important;
            width: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            overflow: hidden !important;
            opacity: 0 !important;
            pointer-events: none !important;
            z-index: -1 !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Logo with clickable link to home
        render_clickable_logo(size="medium", center=True)
        
        st.markdown("<hr style='margin: 1rem 0; opacity: 0.3;'>", unsafe_allow_html=True)
        
        # Menu items
        if check_authentication():
            # Create menu items with custom styling
            menu_items = [
                {"icon": "🏠", "label": "Home", "page": "pages/0_Dashboard.py"},
                {"icon": "📄", "label": "Generate Document", "page": "pages/1_Generate_Document.py"},
                {"icon": "📚", "label": "Document History", "page": "pages/2_Document_History.py"},
                {"icon": "👤", "label": "Profile", "page": "pages/3_Account.py"},
                {"icon": "❓", "label": "Help & Support", "page": "pages/4_Help_&_Support.py"}
            ]
            
            # Determine current page to highlight active menu item
            current_page = st.session_state.get('current_page', '')
            
            # Render menu items
            for item in menu_items:
                # Check if this is the active page
                is_active = current_page.endswith(item["page"])
                
                # Create custom styled button
                if st.button(
                    f"{item['icon']} {item['label']}", 
                    key=f"menu_{item['label']}",
                    use_container_width=True,
                    type="primary" if is_active else "secondary"
                ):
                    st.switch_page(item["page"])
            
            st.markdown("<hr style='margin: 1rem 0; opacity: 0.3;'>", unsafe_allow_html=True)
            
            # Logout button
            if st.button("🚪 Logout", use_container_width=True, key="menu_logout"):
                logout()
                st.rerun()
        else:
            # Login and signup buttons for unauthenticated users
            if st.button("🔑 Login", use_container_width=True, key="menu_login"):
                st.switch_page("pages/login.py")
                
            if st.button("✏️ Sign Up", use_container_width=True, key="menu_signup", type="primary"):
                st.session_state.auth_mode = 'register'
                st.switch_page("pages/login.py")