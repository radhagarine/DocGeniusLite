import streamlit as st

def apply_custom_css():
    """Apply custom CSS styling to the Streamlit app."""
    st.markdown("""
        <style>
        /* Global styles */
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            color: #f4f9f7;
            background: linear-gradient(135deg, #0a2817 0%, #164430 100%);
        }
        
        /* Card styles */
        .card {
            background: rgba(22, 68, 48, 0.3);
            /* backdrop-filter: blur(10px); */
            /* -webkit-backdrop-filter: blur(10px); */
            border-radius: 16px;
            padding: 1.5rem;
            border: 1px solid rgba(63, 215, 165, 0.2);
            box-shadow: 
                0 10px 30px rgba(0, 0, 0, 0.1),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
            margin: 1rem 0;
        }
        
        /* Profile styles */
        .profile-avatar {
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, #3fd7a5 0%, #26856c 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            color: white;
            box-shadow: 0 4px 12px rgba(63, 215, 165, 0.2);
        }
        
        .subscription-badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            background: linear-gradient(135deg, #3fd7a5 0%, #26856c 100%);
            border-radius: 20px;
            font-size: 0.8rem;
            color: white;
            margin-top: 0.5rem;
        }
        
        /* Stats styles */
        .stat-card {
            background: rgba(10, 40, 23, 0.3);
            border-radius: 12px;
            padding: 1.25rem;
            border: 1px solid rgba(63, 215, 165, 0.1);
            transition: transform 0.3s ease;
        }
        
        .stat-card:hover {
            transform: translateY(-2px);
        }
        
        .stat-value {
            font-size: 2rem;
            font-weight: 600;
            color: #3fd7a5;
            margin: 0.5rem 0;
        }
        
        /* Progress bar */
        .progress-bar {
            background: rgba(10, 40, 23, 0.5);
            border-radius: 10px;
            height: 8px;
            overflow: hidden;
            margin-top: 0.5rem;
        }
        
        .progress-bar-fill {
            background: linear-gradient(90deg, #3fd7a5 0%, #26856c 100%);
            height: 100%;
            transition: width 0.3s ease;
        }
        
        /* Button styles */
        .button-primary {
            background: linear-gradient(135deg, #3fd7a5 0%, #26856c 100%);
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 500;
        }
        
        .button-primary:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(63, 215, 165, 0.2);
        }
        
        /* Streamlit overrides */
        .stApp {
            background: transparent !important;
        }
        
        .stButton button {
            background: rgba(63, 215, 165, 0.1);
            border: 1px solid rgba(63, 215, 165, 0.2);
            color: #f4f9f7;
            transition: all 0.3s ease;
        }
        
        .stButton button:hover {
            border-color: #3fd7a5;
            background: rgba(63, 215, 165, 0.2);
            transform: translateY(-1px);
        }
        
        .stTextInput input,
        .stNumberInput input,
        .stSelectbox select {
            background: rgba(10, 40, 23, 0.3) !important;
            border: 1px solid rgba(63, 215, 165, 0.2) !important;
            color: #f4f9f7 !important;
        }
        
        .stTextInput input:focus,
        .stNumberInput input:focus,
        .stSelectbox select:focus {
            border-color: #3fd7a5 !important;
            box-shadow: 0 0 0 1px #3fd7a5 !important;
        }
        
        /* Hide default Streamlit elements */
        #MainMenu, footer {
            visibility: hidden !important;
            display: none !important;
        }
        
        /* Hide default Streamlit sidebar navigation items */
        [data-testid="stSidebarNavItems"] {
            visibility: hidden !important;
            display: none !important;
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
        }
        
        /* Custom sidebar styling */
        .sidebar-menu-item {
            background: rgba(10, 40, 23, 0.3);
            border: 1px solid rgba(63, 215, 165, 0.2);
            border-radius: 8px;
            margin-bottom: 0.5rem;
            transition: all 0.2s ease;
        }
        
        .sidebar-menu-item:hover {
            background: rgba(63, 215, 165, 0.1);
            transform: translateY(-2px);
        }
        
        /* Fix for sidebar content */
        [data-testid="stSidebar"] > div:first-child {
            padding-top: 2rem;
            background: rgba(10, 40, 23, 0.5);
        }
        
        /* Dark theme optimizations */
        @media (prefers-color-scheme: dark) {
            .stApp {
                background: linear-gradient(135deg, #0a2817 0%, #164430 100%) !important;
            }
        }
        </style>
    """, unsafe_allow_html=True)

def get_color_scheme():
    """Return the application's color scheme."""
    return {
        'primary': '#3fd7a5',
        'primary_dark': '#26856c',
        'background': '#0a2817',
        'background_light': '#164430',
        'text': '#f4f9f7',
        'text_muted': 'rgba(244, 249, 247, 0.7)',
        'border': 'rgba(63, 215, 165, 0.2)',
    }

def add_home_button():
    """Add a home button to the top of the page"""
    col1, col2, col3 = st.columns([1, 10, 1])
    with col1:
        if st.button("🏠 Home"):
            st.switch_page("app.py")
            
def render_clickable_logo(size="medium", center=True):
    """
    Render a clickable DocGenius logo that redirects to the home page
    
    Parameters:
    -----------
    size : str
        Size of the logo: "small", "medium", or "large"
    center : bool
        Whether to center the logo
    """
    # Define sizes for different logo variants
    sizes = {
        "small": {"d_g": "2rem", "oc_enius": "1.5rem", "margin": "-3px"},
        "medium": {"d_g": "2.5rem", "oc_enius": "1.8rem", "margin": "-3px"},
        "large": {"d_g": "3.5rem", "oc_enius": "2.5rem", "margin": "-5px"}
    }
    
    # Use medium as default if invalid size provided
    if size not in sizes:
        size = "medium"
    
    # Get the appropriate sizes
    s = sizes[size]
    
    # Create the alignment style
    align_style = "text-align: center;" if center else ""
    
    # Render the logo
    st.markdown(f"""
        <div style="{align_style} margin-bottom: 20px;">
            <a href="javascript:void(0);" onclick="window.parent.location.href='/';" style="text-decoration: none; cursor: pointer;">
                <span style="font-size: {s['d_g']}; font-weight: bold; background: linear-gradient(135deg, #3fd7a5 0%, #26856c 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">D</span>
                <span style="font-size: {s['oc_enius']}; font-weight: bold; margin-left: {s['margin']}; color: #f4f9f7;">oc</span>
                <span style="font-size: {s['d_g']}; font-weight: bold; background: linear-gradient(135deg, #3fd7a5 0%, #26856c 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">G</span>
                <span style="font-size: {s['oc_enius']}; font-weight: bold; margin-left: {s['margin']}; color: #f4f9f7;">enius</span>
            </a>
        </div>
    """, unsafe_allow_html=True)