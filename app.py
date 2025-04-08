import streamlit as st
import os
from auth import check_authentication, login_page, logout
from db import init_db

# Custom CSS to mimic the dark green theme from the screenshot
st.set_page_config(
    page_title="DocGenius Lite",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
def apply_custom_css():
    st.markdown("""
    <style>
    /* Main colors */
    :root {
        --dark-green: #0a2817;
        --medium-green: #164430;
        --light-green: #26856c;
        --accent-green: #3fd7a5;
        --text-white: #f4f9f7;
    }
    
    /* Background and text styles */
    .main {
        background-color: var(--dark-green);
        color: var(--text-white);
    }
    
    h1, h2, h3 {
        color: white !important;
    }
    
    /* Cards */
    .feature-card {
        background-color: var(--medium-green);
        border-radius: 8px;
        padding: 20px;
        margin: 10px 0;
        border-left: 3px solid var(--accent-green);
    }
    
    .stat-card {
        background-color: var(--medium-green);
        border-radius: 12px;
        padding: 25px;
        margin: 15px 0;
        text-align: center;
    }
    
    /* Custom button */
    .launch-btn {
        background-color: var(--accent-green);
        color: var(--dark-green);
        padding: 10px 25px;
        border-radius: 25px;
        font-weight: bold;
        border: none;
        cursor: pointer;
        text-align: center;
        display: inline-block;
        margin: 20px 0;
    }
    
    /* Header navigation */
    .header-nav {
        display: flex;
        justify-content: space-between;
        padding: 15px 0;
        align-items: center;
    }
    
    .logo-container {
        display: flex;
        align-items: center;
    }
    
    .nav-links {
        display: flex;
        gap: 20px;
    }
    
    .nav-link {
        color: var(--text-white);
        text-decoration: none;
        padding: 5px 10px;
    }
    
    /* Hero section */
    .hero-section {
        text-align: center;
        padding: 60px 0 40px 0;
    }
    
    /* Stats circle */
    .stat-circle {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        background-color: var(--medium-green);
        border: 3px solid var(--accent-green);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin: 0 auto;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: bold;
        color: var(--accent-green);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 30px 0;
        margin-top: 50px;
        border-top: 1px solid var(--medium-green);
    }
    
    /* Sidebar override */
    [data-testid="stSidebar"] {
        background-color: var(--medium-green);
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize database on first run
init_db()

# App title and description
def main():
    apply_custom_css()
    
    # Non-authenticated landing page or authenticated dashboard
    if not check_authentication():
        display_landing_page()
    else:
        display_dashboard()

def display_landing_page():
    # Header navigation
    st.markdown("""
    <div class="header-nav">
        <div class="logo-container">
            <div style="width:40px; height:40px; background-color:#26856c; border-radius:8px; display:flex; justify-content:center; align-items:center; margin-right:10px;">
                <span style="color:white; font-weight:bold; font-size:20px;">DG</span>
            </div>
            <span style="font-weight:bold; font-size:18px;">DocGenius</span>
        </div>
        <div class="nav-links">
            <a href="#" class="nav-link">Product</a>
            <a href="#" class="nav-link">Pricing</a>
            <a href="#" class="nav-link">Templates</a>
            <a href="#" class="nav-link">Blog</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Hero section
    st.markdown("""
    <div class="hero-section">
        <h1>Create professional documents with<br>next-generation AI</h1>
        <p style="font-size:1.2rem; margin:20px 0 40px 0;">
            Our AI-powered document system creates and validates<br>
            business documents in real time, ensuring perfect legal compliance.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Login/signup button
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("""
        <div style="text-align:center;">
            <button class="launch-btn" id="login-btn">Launch DocGenius</button>
        </div>
        """, unsafe_allow_html=True)
        
        # Use a regular button that will show the login form when clicked
        if st.button("Sign in / Sign up", key="login_trigger"):
            login_page()
            st.rerun()
    
    # Feature highlights
    st.markdown("<h2 style='text-align:center; margin-top:60px;'>Key Features</h2>", unsafe_allow_html=True)
    
    # Feature cards in a grid
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>Intelligent template selection</h3>
            <p>AI analyzes your needs and recommends the perfect document template based on your specific requirements.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>Customizable parameters</h3>
            <p>Adjust all document aspects to fit your exact needs while maintaining professional standards and legal compliance.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>Real-time validation</h3>
            <p>Track your document's quality score with our Responsible AI system that ensures accuracy, fairness, and compliance.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>Multiple export formats</h3>
            <p>Download your finished documents in PDF, DOCX, or HTML formats, ready for immediate professional use.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Document stats section
    st.markdown("<h2 style='text-align:center; margin-top:60px;'>All your document tools in one place</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-circle">
                <div class="stat-number">5+</div>
            </div>
            <h3>Document Types</h3>
            <p>Create NDAs, proposals, invoices, letters of intent, and more from professional templates</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-circle">
                <div class="stat-number">98%</div>
            </div>
            <h3>Accuracy Rate</h3>
            <p>Our documents maintain high standards of legal compliance and professional quality</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-circle">
                <div class="stat-number">24/7</div>
            </div>
            <h3>Document Access</h3>
            <p>Create and access your documents anytime, from any device, with secure cloud storage</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Why choose us section
    st.markdown("""
    <div style="margin-top:80px; text-align:center;">
        <h2>Why choose DocGenius?</h2>
        <p style="font-size:1.1rem; margin:20px 0 40px 0;">
            The ultimate tool for businesses that value professionalism, compliance, and efficiency.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Customer testimonials
    st.markdown("<h2 style='text-align:center; margin-top:60px;'>What our customers say about us</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background-color:#164430; padding:20px; border-radius:10px; margin-top:20px;">
            <p>"The NDA templates saved me hours of work and worry. I can now generate perfect legal documents in minutes."</p>
            <p style="margin-top:20px; font-style:italic;">- Sarah J., Small Business Owner</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background-color:#164430; padding:20px; border-radius:10px; margin-top:20px;">
            <p>"I've used many document generators, but DocGenius is the only one that gives me confidence about legal compliance."</p>
            <p style="margin-top:20px; font-style:italic;">- Michael R., Consultant</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background-color:#164430; padding:20px; border-radius:10px; margin-top:20px;">
            <p>"The ProAI validation gives me peace of mind that my documents are clear, fair, and likely to be accepted by partners."</p>
            <p style="margin-top:20px; font-style:italic;">- Elena K., Freelancer</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>© 2025 DocGenius Lite | Terms of Service | Privacy Policy</p>
    </div>
    """, unsafe_allow_html=True)

def display_dashboard():
    # Header with user info
    st.markdown(f"""
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:30px;">
        <h1>DocGenius Dashboard</h1>
        <div style="background-color:#164430; padding:8px 15px; border-radius:20px;">
            <span>👤 {st.session_state.get('email')}</span>
            <span style="margin-left:10px; background-color:#26856c; padding:3px 8px; border-radius:10px;">
                {st.session_state.get('subscription').upper()}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Main dashboard stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-circle">
                <div class="stat-number" id="doc-count"></div>
            </div>
            <h3>Documents Created</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Update the count with JavaScript
        st.markdown(f"""
        <script>
            document.getElementById('doc-count').innerText = '{st.session_state.get('total_docs', 0)}';
        </script>
        """, unsafe_allow_html=True)
    
    with col2:
        # Calculate usage percentage
        free_docs_used = st.session_state.get('free_docs_used', 0)
        free_docs_limit = 3
        usage_percent = min(int((free_docs_used / free_docs_limit) * 100), 100)
        
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-circle">
                <div class="stat-number">{usage_percent}%</div>
            </div>
            <h3>Monthly Usage</h3>
            <p>{free_docs_used}/{free_docs_limit} documents used this month</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        subscription = st.session_state.get('subscription', 'free')
        if subscription == 'pro':
            status_text = "PRO Plan Active"
            color = "#3fd7a5"
        else:
            status_text = "FREE Plan Active"
            color = "#f4f9f7"
            
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-circle" style="border-color:{color};">
                <div class="stat-number" style="color:{color};">{subscription.upper()}</div>
            </div>
            <h3>Subscription Status</h3>
            <p>{status_text}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick actions
    st.markdown("<h2 style='margin-top:30px;'>Quick Actions</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Document creation card
        st.markdown("""
        <div style="background-color:#164430; padding:25px; border-radius:10px; margin-top:20px;">
            <h3>Create New Document</h3>
            <p style="margin-bottom:20px;">Generate a new professional document from our template library</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Create Document", type="primary", key="create_doc_btn"):
            st.switch_page("pages/1_Generate_Document.py")
    
    with col2:
        # Document history card
        st.markdown("""
        <div style="background-color:#164430; padding:25px; border-radius:10px; margin-top:20px;">
            <h3>View Document History</h3>
            <p style="margin-bottom:20px;">Access, view, and download your previously created documents</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("View History", key="view_history_btn"):
            st.switch_page("pages/2_Document_History.py")
    
    # Document templates
    st.markdown("<h2 style='margin-top:40px;'>Available Templates</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    templates = [
        {"name": "Non-Disclosure Agreement", "icon": "🔒", "type": "nda"},
        {"name": "Invoice", "icon": "📊", "type": "invoice"},
        {"name": "Letter of Intent", "icon": "📝", "type": "letter_of_intent"},
        {"name": "Business Proposal", "icon": "💼", "type": "proposal"},
        {"name": "Scope of Work", "icon": "🔨", "type": "scope_of_work"}
    ]
    
    for i, template in enumerate(templates):
        with [col1, col2, col3][i % 3]:
            st.markdown(f"""
            <div style="background-color:#164430; padding:15px; border-radius:10px; margin-top:15px;">
                <div style="display:flex; align-items:center;">
                    <div style="font-size:28px; margin-right:10px;">{template['icon']}</div>
                    <div>
                        <h3 style="margin:0;">{template['name']}</h3>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Use Template", key=f"use_{template['type']}"):
                # Store template selection in session state
                st.session_state['selected_template'] = template['type']
                st.switch_page("pages/1_Generate_Document.py")
    
    # Pro features highlight
    if st.session_state.get('subscription') != 'pro':
        st.markdown("""
        <div style="background-color:#164430; padding:25px; border-radius:10px; margin-top:40px; border:1px solid #3fd7a5;">
            <h2 style="color:#3fd7a5;">Upgrade to PRO</h2>
            <p>Unlock premium features and create unlimited documents</p>
            <ul style="margin-top:15px;">
                <li>Unlimited document generation</li>
                <li>Advanced customization options</li>
                <li>Enhanced AI validation</li>
                <li>Priority support</li>
                <li>Document storage for 1 year</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Upgrade Now", type="primary", key="upgrade_pro_btn"):
            st.switch_page("pages/3_Account.py")
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>© 2025 DocGenius Lite | <a href="#" style="color:#3fd7a5;">Help & Support</a></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Logout button in sidebar
    if st.sidebar.button("Logout"):
        logout()
        st.rerun()

if __name__ == "__main__":
    main()
