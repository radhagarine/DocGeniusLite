import streamlit as st
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.auth import check_authentication, logout
from app import apply_custom_css

def display_dashboard():
    st.markdown("""
        <div class="dashboard-container">
            <div class="dashboard-header">
                <h1>Welcome to DocGenius</h1>
                <div class="user-info">
                    <span>👤 {}</span>
                    <div class="subscription-badge">{}</div>
                </div>
            </div>
            
            <div class="stats-container">
                <div class="stat-card">
                    <div class="stat-circle">
                        <div class="stat-number">{}</div>
                    </div>
                    <h3>Documents Created</h3>
                    <p>Total documents generated</p>
                </div>
                
                <div class="stat-card">
                    <div class="stat-circle">
                        <div class="stat-number">{}%</div>
                    </div>
                    <h3>Monthly Usage</h3>
                    <p>{}/{} documents used this month</p>
                </div>
                
                <div class="stat-card">
                    <div class="stat-circle">
                        <div class="stat-number">{}</div>
                    </div>
                    <h3>Subscription Status</h3>
                    <p>{}</p>
                </div>
            </div>
            
            <h2>Quick Actions</h2>
            <div class="quick-actions">
                <div class="action-card" onclick="window.location.href='1_Generate_Document'">
                    <h3>Create New Document</h3>
                    <p>Generate a new professional document from our template library</p>
                </div>
                
                <div class="action-card" onclick="window.location.href='2_Document_History'">
                    <h3>View Document History</h3>
                    <p>Access, view, and download your previously created documents</p>
                </div>
            </div>
            
            <h2>Available Templates</h2>
            <div class="template-grid">
                {}
            </div>
            
            {}
        </div>
    """.format(
        st.session_state.get('email', 'User'),
        st.session_state.get('subscription', 'FREE').upper(),
        st.session_state.get('total_docs', 0),
        min(int((st.session_state.get('free_docs_used', 0) / 3) * 100), 100),
        st.session_state.get('free_docs_used', 0),
        3,
        st.session_state.get('subscription', 'FREE').upper(),
        "PRO Plan Active" if st.session_state.get('subscription') == 'pro' else "FREE Plan Active",
        '\n'.join([f"""
            <div class="template-card" onclick="window.location.href='1_Generate_Document'">
                <div class="template-icon">{template['icon']}</div>
                <h3>{template['name']}</h3>
                <p>{template['description']}</p>
            </div>
        """ for template in [
            {"name": "Non-Disclosure Agreement", "icon": "🔒", "description": "Create a secure NDA document"},
            {"name": "Invoice", "icon": "📊", "description": "Generate professional invoices"},
            {"name": "Letter of Intent", "icon": "📝", "description": "Draft a formal letter of intent"},
            {"name": "Business Proposal", "icon": "💼", "description": "Create compelling business proposals"},
            {"name": "Scope of Work", "icon": "🔨", "description": "Define project scope and deliverables"}
        ]]),
        """
        <div class="pro-features" style="display: {};">
            <h2>Upgrade to PRO</h2>
            <p>Unlock premium features and create unlimited documents</p>
            <ul>
                <li>Unlimited document generation</li>
                <li>Advanced customization options</li>
                <li>Enhanced AI validation</li>
                <li>Priority support</li>
                <li>Document storage for 1 year</li>
            </ul>
            <button class="shadcn-button" onclick="window.location.href='3_Account'">
                Upgrade Now
            </button>
        </div>
        """.format('block' if st.session_state.get('subscription') != 'pro' else 'none')
    ), unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="Dashboard | DocGenius",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    apply_custom_css()
    
    if not check_authentication():
        st.switch_page("app.py")
    else:
        # Add logout button to header
        col1, col2 = st.columns([6,1])
        with col2:
            if st.button("Logout", type="primary"):
                logout()
                st.rerun()
        display_dashboard()

if __name__ == "__main__":
    main() 