import streamlit as st
import os
from auth import check_authentication, login_page, logout
from db import init_db

# Configure page settings
st.set_page_config(
    page_title="DocGenius Lite",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None
)

# Hide streamlit elements using custom CSS
st.markdown("""
    <style>
    #MainMenu {display: none}
    header[data-testid="stHeader"] {display: none}
    .stDeployButton {display: none}
    section[data-testid="stSidebar"] {display: none}
    [data-testid="collapsedControl"] {display: none}
    footer {display: none}
    
    /* Ensure main content is visible */
    .main .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    [data-testid="stAppViewContainer"] {
        padding-top: 0 !important;
    }
    
    /* Hide specific Streamlit Elements */
    #MainMenu, 
    footer, 
    header[data-testid="stHeader"],
    .stDeployButton,
    section[data-testid="stSidebar"],
    [data-testid="collapsedControl"],
    button[kind="headerNoPadding"],
    [data-testid="stDecoration"],
    .decoration,
    /* Hide heading anchor buttons */
    .st-emotion-cache-2cgmpt,
    .st-emotion-cache-gi0tri {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# Custom CSS with modern styling
def apply_custom_css():
    st.markdown("""
        <style>
        /* Reset and base styles */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        /* Hide Streamlit components */
        #MainMenu, footer, header {display: none !important;}
        .stDeployButton {display: none !important;}
        section[data-testid="stSidebar"] {display: none !important;}
        div[data-testid="collapsedControl"] {display: none !important;}
        
        /* Main container styles */
        .stApp {
            background: linear-gradient(135deg, #0a2817 0%, #164430 100%) !important;
            color: #f4f9f7;
            min-height: 100vh;
        }
        
        .main-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        /* Navigation */
        .nav-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 4rem;
            background: rgba(22, 68, 48, 0.3);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 1000;
            box-shadow: 
                0 10px 30px rgba(0, 0, 0, 0.1),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
        }
        
        .logo-box {
            display: flex;
            align-items: center;
            font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            color: #f4f9f7;
            text-decoration: none;
            transform-style: preserve-3d;
            transition: transform 0.3s ease;
        }
        
        .logo-box:hover {
            transform: translateY(-2px) translateZ(10px);
        }
        
        .nav-links {
            display: flex;
            gap: 2.5rem;
            align-items: center;
        }
        
        .nav-link {
            color: #f4f9f7 !important;
            text-decoration: none !important;
            font-size: 1rem;
            font-weight: 500;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            transition: all 0.3s ease;
            position: relative;
            transform-style: preserve-3d;
        }
        
        .nav-link:hover {
            background: rgba(63, 215, 165, 0.1);
            transform: translateY(-2px) translateZ(10px);
        }
        
        .nav-link::after {
            content: '';
            position: absolute;
            bottom: -2px;
            left: 50%;
            transform: translateX(-50%) scaleX(0);
            width: 100%;
            height: 2px;
            background: linear-gradient(135deg, #3fd7a5 0%, #26856c 100%);
            transition: transform 0.3s ease;
        }
        
        .nav-link:hover::after {
            transform: translateX(-50%) scaleX(1);
        }
        
        .shadcn-button {
            background: linear-gradient(135deg, #3fd7a5 0%, #26856c 100%);
            color: #f4f9f7;
            padding: 0.75rem 2rem;
            border-radius: 8px;
            font-weight: 600;
            border: none;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 
                0 4px 15px rgba(63, 215, 165, 0.2),
                inset 0 2px 5px rgba(255, 255, 255, 0.2);
            transform-style: preserve-3d;
        }
        
        .shadcn-button:hover {
            transform: translateY(-2px) translateZ(10px);
            box-shadow: 
                0 8px 25px rgba(63, 215, 165, 0.3),
                inset 0 2px 5px rgba(255, 255, 255, 0.3);
        }
        
        /* Override any remaining blue colors */
        a, a:visited, a:hover, a:active {
            color: #f4f9f7 !important;
            text-decoration: none !important;
        }
        
        .streamlit-expanderHeader {
            color: #f4f9f7 !important;
        }
        
        [data-testid="stMarkdownContainer"] a {
            color: #f4f9f7 !important;
            transition: color 0.3s ease;
        }
        
        [data-testid="stMarkdownContainer"] a:hover {
            color: #3fd7a5 !important;
        }
        
        /* Hero section */
        .hero-section {
            text-align: center;
            padding: 10rem 2rem 6rem 2rem;  /* Increased top padding to account for fixed nav */
            position: relative;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
        }
        
        .hero-section::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 800px;
            height: 800px;
            background: radial-gradient(circle, rgba(63, 215, 165, 0.1) 0%, rgba(63, 215, 165, 0) 70%);
            z-index: 0;
        }
        
        .hero-title {
            font-size: 4rem;
            font-weight: bold;
            margin-bottom: 1.5rem;
            line-height: 1.2;
            position: relative;
            z-index: 1;
            max-width: 800px;
        }
        
        .hero-title span {
            background: linear-gradient(135deg, #3fd7a5 0%, #26856c 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .hero-subtitle {
            font-size: 1.25rem;
            opacity: 0.9;
            max-width: 600px;
            margin: 0 auto 2rem auto;
            line-height: 1.6;
            position: relative;
            z-index: 1;
        }
        
        /* Feature cards */
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
            margin-top: 6rem;
            padding: 0 2rem;
        }
        
        .feature-card {
            background: rgba(22, 68, 48, 0.3);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 2rem;
            border: 1px solid rgba(63, 215, 165, 0.1);
            transition: all 0.3s ease;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
            border-color: rgba(63, 215, 165, 0.3);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
        }
        
        .feature-icon {
            width: 48px;
            height: 48px;
            background: linear-gradient(135deg, #26856c 0%, #3fd7a5 100%);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 1.5rem;
            font-size: 1.5rem;
        }
        
        .feature-card h3 {
            color: #f4f9f7;
            margin-bottom: 1rem;
            font-size: 1.25rem;
        }
        
        .feature-card p {
            opacity: 0.9;
            line-height: 1.6;
            font-size: 0.95rem;
        }
        
        /* Stats section */
        .stats-section {
            margin-top: 8rem;
            text-align: center;
            padding: 4rem 2rem;
            background: rgba(22, 68, 48, 0.3);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-radius: 24px;
            border: 1px solid rgba(63, 215, 165, 0.1);
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 3rem;
            margin-top: 3rem;
        }
        
        .stat-card {
            position: relative;
        }
        
        .stat-card::after {
            content: '';
            position: absolute;
            top: 50%;
            right: -1.5rem;
            transform: translateY(-50%);
            width: 1px;
            height: 60%;
            background: rgba(63, 215, 165, 0.2);
        }
        
        .stat-card:last-child::after {
            display: none;
        }
        
        .stat-number {
            font-size: 3.5rem;
            font-weight: bold;
            background: linear-gradient(135deg, #3fd7a5 0%, #26856c 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
        }
        
        /* Brand section */
        .brand-section {
            margin-top: 6rem;
            padding: 3rem 0;
            border-top: 1px solid rgba(63, 215, 165, 0.1);
        }
        
        .brand-grid {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 4rem;
            flex-wrap: wrap;
            opacity: 0.6;
        }
        
        .brand-logo {
            height: 30px;
            filter: brightness(0) invert(1);
            transition: opacity 0.3s ease;
        }
        
        .brand-logo:hover {
            opacity: 0.8;
        }
        
        /* Form styling */
        .auth-form {
            max-width: 400px;
            margin: 2rem auto;
            padding: 2.5rem;
            background: rgba(22, 68, 48, 0.3);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-radius: 16px;
            border: 1px solid rgba(63, 215, 165, 0.1);
        }
        
        .stTextInput > div > div {
            background: rgba(10, 40, 23, 0.3) !important;
            border: 1px solid rgba(63, 215, 165, 0.2) !important;
            border-radius: 8px !important;
            color: #f4f9f7 !important;
            transition: all 0.3s ease;
        }
        
        .stTextInput > div > div:focus-within {
            border-color: rgba(63, 215, 165, 0.5) !important;
            box-shadow: 0 0 0 2px rgba(63, 215, 165, 0.1) !important;
        }
        
        .stButton > button {
            background: linear-gradient(135deg, #3fd7a5 0%, #26856c 100%) !important;
            color: #fff !important;
            font-weight: 600 !important;
            width: 100% !important;
            border-radius: 8px !important;
            padding: 0.75rem !important;
            transition: all 0.3s ease !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 15px rgba(63, 215, 165, 0.2) !important;
        }

        /* Dashboard Styles */
        .dashboard-container {
            padding: 2rem 4rem;
        }
        
        .dashboard-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2rem;
            background: rgba(22, 68, 48, 0.3);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 1.5rem 2rem;
            border: 1px solid rgba(63, 215, 165, 0.1);
            box-shadow: 
                0 10px 30px rgba(0, 0, 0, 0.1),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
            transform-style: preserve-3d;
            perspective: 1000px;
        }
        
        .user-info {
            display: flex;
            align-items: center;
            gap: 1rem;
            padding: 0.5rem 1rem;
            background: rgba(10, 40, 23, 0.3);
            border-radius: 12px;
            border: 1px solid rgba(63, 215, 165, 0.2);
            transform-style: preserve-3d;
            transition: all 0.3s ease;
        }
        
        .user-info:hover {
            transform: translateY(-2px) translateZ(10px);
            box-shadow: 
                0 8px 25px rgba(63, 215, 165, 0.2),
                inset 0 1px 2px rgba(255, 255, 255, 0.1);
        }
        
        .subscription-badge {
            padding: 0.25rem 0.75rem;
            background: linear-gradient(135deg, #3fd7a5 0%, #26856c 100%);
            border-radius: 8px;
            font-size: 0.8rem;
            font-weight: 600;
            box-shadow: 
                0 2px 8px rgba(63, 215, 165, 0.2),
                inset 0 1px 2px rgba(255, 255, 255, 0.1);
        }
        
        /* Dashboard Stats */
        .stats-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin-bottom: 3rem;
        }
        
        .stat-card {
            background: rgba(22, 68, 48, 0.3);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 2rem;
            border: 1px solid rgba(63, 215, 165, 0.1);
            transform-style: preserve-3d;
            transition: all 0.3s ease;
            box-shadow: 
                0 10px 30px rgba(0, 0, 0, 0.1),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
        }
        
        .stat-card:hover {
            transform: translateY(-5px) translateZ(20px);
            box-shadow: 
                0 15px 35px rgba(0, 0, 0, 0.2),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
        }
        
        .stat-circle {
            width: 80px;
            height: 80px;
            background: rgba(10, 40, 23, 0.3);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 1.5rem;
            border: 2px solid #3fd7a5;
            box-shadow: 
                0 8px 16px rgba(63, 215, 165, 0.2),
                inset 0 2px 4px rgba(255, 255, 255, 0.1);
            transform-style: preserve-3d;
        }
        
        /* Quick Actions */
        .quick-actions {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
            margin-bottom: 3rem;
        }
        
        .action-card {
            background: rgba(22, 68, 48, 0.3);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 2rem;
            border: 1px solid rgba(63, 215, 165, 0.1);
            transform-style: preserve-3d;
            transition: all 0.3s ease;
            cursor: pointer;
            box-shadow: 
                0 10px 30px rgba(0, 0, 0, 0.1),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
        }
        
        .action-card:hover {
            transform: translateY(-5px) translateZ(20px);
            border-color: rgba(63, 215, 165, 0.3);
            box-shadow: 
                0 15px 35px rgba(0, 0, 0, 0.2),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
        }
        
        /* Template Cards */
        .template-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 2rem;
            margin-top: 2rem;
        }
        
        .template-card {
            background: rgba(22, 68, 48, 0.3);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 1.5rem;
            border: 1px solid rgba(63, 215, 165, 0.1);
            transform-style: preserve-3d;
            transition: all 0.3s ease;
            cursor: pointer;
            box-shadow: 
                0 10px 30px rgba(0, 0, 0, 0.1),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
        }
        
        .template-card:hover {
            transform: translateY(-5px) translateZ(20px);
            border-color: rgba(63, 215, 165, 0.3);
            box-shadow: 
                0 15px 35px rgba(0, 0, 0, 0.2),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
        }
        
        .template-icon {
            font-size: 2rem;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, #3fd7a5 0%, #26856c 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        /* Pro Features Section */
        .pro-features {
            background: rgba(22, 68, 48, 0.3);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 2rem;
            border: 1px solid #3fd7a5;
            margin-top: 3rem;
            transform-style: preserve-3d;
            transition: all 0.3s ease;
            box-shadow: 
                0 10px 30px rgba(0, 0, 0, 0.1),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
        }
        
        .pro-features:hover {
            transform: translateY(-5px) translateZ(20px);
            box-shadow: 
                0 15px 35px rgba(0, 0, 0, 0.2),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
        }
        
        .pro-features h2 {
            color: #3fd7a5;
            margin-bottom: 1rem;
        }
        
        .pro-features ul {
            list-style: none;
            padding: 0;
            margin: 1.5rem 0;
        }
        
        .pro-features li {
            margin-bottom: 0.75rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .pro-features li::before {
            content: '✓';
            color: #3fd7a5;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

# Custom navigation
def render_navigation():
    # Add Sign Up button click handler
    if not check_authentication():
        col1, col2, col3 = st.columns([2, 6, 2])
        with col2:
            st.markdown("""
                <nav class="nav-container">
                    <div class="logo-box">
                        <span style="font-size: 2.5rem; font-weight: bold; background: linear-gradient(135deg, #3fd7a5 0%, #26856c 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">D</span>
                        <span style="font-size: 1.8rem; font-weight: bold; margin-left: -5px;">oc</span>
                        <span style="font-size: 2.5rem; font-weight: bold; background: linear-gradient(135deg, #3fd7a5 0%, #26856c 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">G</span>
                        <span style="font-size: 1.8rem; font-weight: bold; margin-left: -5px;">enius</span>
                    </div>
                    <div class="nav-links">
                        <a href="#features" class="nav-link">Features</a>
                        <a href="#pricing" class="nav-link">Pricing</a>
                        <button class="shadcn-button" onclick="window.location.href='pages/login'">Sign Up</button>
                    </div>
                </nav>
            """, unsafe_allow_html=True)
    else:
        col1, col2, col3 = st.columns([2, 6, 2])
        with col2:
            st.markdown("""
                <nav class="nav-container">
                    <div class="logo-box">
                        <span style="font-size: 2.5rem; font-weight: bold; background: linear-gradient(135deg, #3fd7a5 0%, #26856c 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">D</span>
                        <span style="font-size: 1.8rem; font-weight: bold; margin-left: -5px;">oc</span>
                        <span style="font-size: 2.5rem; font-weight: bold; background: linear-gradient(135deg, #3fd7a5 0%, #26856c 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">G</span>
                        <span style="font-size: 1.8rem; font-weight: bold; margin-left: -5px;">enius</span>
                    </div>
                    <div class="nav-links">
                        <a href="pages/0_Dashboard.py" class="nav-link">Dashboard</a>
                        <a href="#" onclick="document.getElementById('logout-form').submit();" class="nav-link">Logout</a>
                    </div>
                </nav>
            """, unsafe_allow_html=True)

# Hero section
def render_hero():
    st.markdown("""
        <div class="hero-section">
            <h1 class="hero-title">Protect your data with<br><span>next-generation AI</span></h1>
            <p class="hero-subtitle">Our AI-powered document system creates and validates business documents in real time, ensuring perfect legal compliance.</p>
            <button class="shadcn-button">Get Started</button>
        </div>

        <div class="feature-grid">
            <div class="feature-card">
                <div class="feature-icon">🔍</div>
                <h3>Intelligent threat detection</h3>
                <p>AI analyzes and detects security threats in real-time, ensuring maximum protection.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🛡️</div>
                <h3>Personalized protection</h3>
                <p>Customized security measures tailored to your specific needs and requirements.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">⚡</div>
                <h3>Real-time response</h3>
                <p>Instant threat mitigation and protection against potential security breaches.</p>
            </div>
        </div>

        <div class="stats-section">
            <h2>All your security tools in one place</h2>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">100%</div>
                    <h3>Security Guarantee</h3>
                    <p>Complete protection for your data</p>
                </div>
                <div class="stat-card">
                    <div class="stat-number">24/7</div>
                    <h3>Real-time monitoring</h3>
                    <p>Continuous security oversight</p>
                </div>
                <div class="stat-card">
                    <div class="stat-number">170+</div>
                    <h3>Threats blocked</h3>
                    <p>Average daily protection</p>
                </div>
            </div>
        </div>

        <div class="brand-section">
            <div class="brand-grid">
                <img src="https://cdn.worldvectorlogo.com/logos/discord-6.svg" class="brand-logo" alt="Discord">
                <img src="https://cdn.worldvectorlogo.com/logos/shopify.svg" class="brand-logo" alt="Shopify">
                <img src="https://cdn.worldvectorlogo.com/logos/atlassian-1.svg" class="brand-logo" alt="Atlassian">
                <img src="https://cdn.worldvectorlogo.com/logos/microsoft-5.svg" class="brand-logo" alt="Microsoft">
                <img src="https://cdn.worldvectorlogo.com/logos/google-1-1.svg" class="brand-logo" alt="Google">
            </div>
        </div>
    """, unsafe_allow_html=True)

def main():
    apply_custom_css()
    
    if not check_authentication():
        render_navigation()
        render_hero()
    else:
        st.switch_page("pages/0_Dashboard.py")

def display_dashboard():
    st.markdown("""
        <div class="dashboard-container">
            <div class="dashboard-header">
                <h1>DocGenius Dashboard</h1>
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
                <div class="action-card" onclick="window.location.href='pages/1_Generate_Document.py'">
                    <h3>Create New Document</h3>
                    <p>Generate a new professional document from our template library</p>
                </div>
                
                <div class="action-card" onclick="window.location.href='pages/2_Document_History.py'">
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
        st.session_state.get('email'),
        st.session_state.get('subscription').upper(),
        st.session_state.get('total_docs', 0),
        min(int((st.session_state.get('free_docs_used', 0) / 3) * 100), 100),
        st.session_state.get('free_docs_used', 0),
        3,
        st.session_state.get('subscription', 'FREE').upper(),
        "PRO Plan Active" if st.session_state.get('subscription') == 'pro' else "FREE Plan Active",
        '\n'.join([f"""
            <div class="template-card" onclick="window.location.href='pages/1_Generate_Document.py'">
                <div class="template-icon">{template['icon']}</div>
                <h3>{template['name']}</h3>
            </div>
        """ for template in [
            {"name": "Non-Disclosure Agreement", "icon": "🔒"},
            {"name": "Invoice", "icon": "📊"},
            {"name": "Letter of Intent", "icon": "📝"},
            {"name": "Business Proposal", "icon": "💼"},
            {"name": "Scope of Work", "icon": "🔨"}
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
            <button class="shadcn-button" onclick="window.location.href='pages/3_Account.py'">
                Upgrade Now
            </button>
        </div>
        """.format('block' if st.session_state.get('subscription') != 'pro' else 'none')
    ), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
