import streamlit as st
import sys
import os
import json
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auth import check_authentication, logout, get_user_info, update_user_info
from utils.styles import apply_custom_css, render_clickable_logo
from utils.document import (
    get_user_credits,
    calculate_required_credits,
    get_document_display_name,
    get_document_count,
    get_recent_documents,
    get_user_storage_used
)
from utils.sidebar import create_sidebar
import time

st.set_page_config(
    page_title="Dashboard | DocGenius",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

def format_date(timestamp):
    dt = datetime.fromisoformat(timestamp)
    return dt.strftime("%B %d, %Y %I:%M %p")

def get_storage_display_values(user_id):
    """
    Calculate storage display values for the dashboard
    
    Returns:
    --------
    tuple: (display_value, unit, progress_percentage)
    """
    # Get storage used in MB
    storage_mb = get_user_storage_used(user_id)
    
    # Set storage limit based on subscription (1GB for free, unlimited for pro)
    storage_limit_mb = float('inf') if st.session_state.get('subscription') == 'pro' else 1024
    
    # Calculate progress percentage (max 100%)
    if storage_limit_mb == float('inf'):
        progress = 50  # Show 50% for unlimited plans
    else:
        progress = min((storage_mb / storage_limit_mb) * 100, 100)
    
    # Format display value and unit
    if storage_mb > 1000:
        display_value = f"{storage_mb/1024:.2f}"
        unit = "GB"
    else:
        display_value = f"{storage_mb:.2f}"
        unit = "MB"
        
    # For unlimited plans, show a different display
    if st.session_state.get('subscription') == 'pro':
        if storage_mb > 1000:
            return f"{storage_mb/1024:.2f}", "GB", 50
        else:
            return f"{storage_mb:.2f}", "MB", 50
    
    return display_value, unit, progress

def save_onboarding_data(data):
    """
    Save onboarding data to the database
    
    Parameters:
    -----------
    data : dict
        Dictionary containing user onboarding information with keys:
        - industry: User's industry
        - business_type: Type of business
        - company_description: Description of the company (optional)
        - doc_types: Types of documents user creates (optional)
        - team_size: Size of the user's team (optional)
        - company_name: Name of the company (optional)
        - company_logo: Path to uploaded company logo (optional)
    
    Returns:
    --------
    bool
        True if update was successful, False otherwise
    """
    # Save all data to the user profile
    update_data = {
        "industry": data.get('industry'),
        "business_type": data.get('business_type'),
        "company_description": data.get('company_description', ''),
        "company_name": data.get('company_name', ''),
        "team_size": data.get('team_size', ''),
        "doc_types": ','.join(data.get('doc_types', [])) if isinstance(data.get('doc_types'), list) else data.get('doc_types', ''),
        "company_logo": data.get('company_logo', ''),
        "business_address": data.get('business_address', ''),
        "business_phone": data.get('business_phone', ''),
        "business_email": data.get('business_email', st.session_state.get('email', '')),
        "onboarding_completed": True
    }
    
    # Also store in session state for immediate use
    for key, value in update_data.items():
        st.session_state[key] = value
        
    return update_user_info(st.session_state.user_id, update_data)

def show_onboarding():
    """
    Display a simplified onboarding process using Streamlit components
    """
    # Initialize onboarding state if not present
    if 'onboarding_step' not in st.session_state:
        st.session_state.onboarding_step = 1
        
    # Get existing user info to pre-fill fields
    user_info = get_user_info() or {}
    
    # Apply custom CSS for onboarding
    st.markdown("""
    <style>
        .onboarding-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
            background: linear-gradient(135deg, rgba(22, 28, 36, 0.95), rgba(22, 28, 36, 0.98));
            border-radius: 16px;
            border: 1px solid rgba(63, 215, 165, 0.2);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        }
        
        .stProgress > div > div {
            background-color: #3fd7a5 !important;
        }
        
        .step-indicator {
            color: #3fd7a5;
            font-size: 0.9rem;
            text-align: right;
            margin-bottom: 1rem;
        }
        
        .onboarding-header {
            color: white;
            margin-bottom: 1.5rem;
        }
        
        .onboarding-subtext {
            color: rgba(255, 255, 255, 0.7);
            margin-bottom: 2rem;
        }
        
        /* Form styling */
        .stButton button {
            border-radius: 8px;
            font-weight: 500;
            transition: all 0.2s;
        }
        
        .stButton button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Create a container with custom styling
    st.markdown('<div class="onboarding-container">', unsafe_allow_html=True)
    onboarding_container = st.container()
    
    with onboarding_container:
        # Add a progress bar to show steps
        progress_value = 0.5 if st.session_state.onboarding_step == 1 else 1.0
        st.progress(progress_value)
        
        # Step indicator
        st.markdown(f'<div class="step-indicator">Step {st.session_state.onboarding_step} of 2</div>', unsafe_allow_html=True)
        
        # Step 1: Basic Information
        if st.session_state.onboarding_step == 1:
            st.markdown('<h2 class="onboarding-header">Welcome to DocGenius! 👋</h2>', unsafe_allow_html=True)
            st.markdown('<p class="onboarding-subtext">Let\'s get you set up with your account. This will only take a minute.</p>', unsafe_allow_html=True)
            
            # Form for step 1
            with st.form(key="onboarding_step1_form"):
                company_name = st.text_input(
                    "Company Name",
                    value=user_info.get('company_name', st.session_state.get('company_name', '')),
                    placeholder="Enter your company name"
                )
                
                industry = st.selectbox(
                    "Industry",
                    ["Technology", "Healthcare", "Finance", "Education", "Other"],
                    index=["Technology", "Healthcare", "Finance", "Education", "Other"].index(user_info.get('industry', st.session_state.get('industry', 'Technology'))) if user_info.get('industry', st.session_state.get('industry', '')) in ["Technology", "Healthcare", "Finance", "Education", "Other"] else 0
                )
                
                business_type = st.selectbox(
                    "Business Type",
                    ["B2B", "B2C", "Non-profit", "Government", "Other"],
                    index=["B2B", "B2C", "Non-profit", "Government", "Other"].index(user_info.get('business_type', st.session_state.get('business_type', 'B2B'))) if user_info.get('business_type', st.session_state.get('business_type', '')) in ["B2B", "B2C", "Non-profit", "Government", "Other"] else 0
                )
                
                # Company logo upload
                st.write("Company Logo (optional)")
                uploaded_logo = st.file_uploader("Upload your company logo", type=["png", "jpg", "jpeg"], key="logo_uploader")
                
                # Display existing logo if available
                existing_logo = user_info.get('company_logo', st.session_state.get('company_logo', ''))
                if existing_logo and not uploaded_logo:
                    st.image(existing_logo, width=150, caption="Current Logo")
                    st.caption("Upload a new logo to replace the current one")
                
                # Form buttons
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.form_submit_button("Skip", on_click=lambda: complete_onboarding(), type="secondary")
                with col2:
                    submit = st.form_submit_button("Next →", type="primary")
                    if submit and company_name and industry:
                        # Process logo if uploaded
                        logo_path = ''
                        if uploaded_logo:
                            # Create directory if it doesn't exist
                            import os
                            logo_dir = os.path.join(os.getcwd(), "attached_assets", "logos")
                            os.makedirs(logo_dir, exist_ok=True)
                            
                            # Save the file
                            file_extension = uploaded_logo.name.split('.')[-1]
                            logo_filename = f"logo_{st.session_state.user_id}.{file_extension}"
                            logo_path = os.path.join(logo_dir, logo_filename)
                            
                            with open(logo_path, "wb") as f:
                                f.write(uploaded_logo.getbuffer())
                        
                        # Save data to session state
                        st.session_state.company_name = company_name
                        st.session_state.industry = industry
                        st.session_state.business_type = business_type
                        if logo_path:
                            st.session_state.company_logo = logo_path
                        
                        # Move to next step
                        st.session_state.onboarding_step = 2
                        st.rerun()
        
        # Step 2: Document Preferences
        else:
            st.markdown('<h2 class="onboarding-header">Almost there! 🎯</h2>', unsafe_allow_html=True)
            st.markdown('<p class="onboarding-subtext">Tell us a bit more about your document needs.</p>', unsafe_allow_html=True)
            
            # Form for step 2
            with st.form(key="onboarding_step2_form"):
                # Get existing doc types from user info
                existing_doc_types = []
                if user_info.get('doc_types'):
                    existing_doc_types = user_info.get('doc_types').split(',')
                elif st.session_state.get('doc_types') and isinstance(st.session_state.get('doc_types'), list):
                    existing_doc_types = st.session_state.get('doc_types')
                elif st.session_state.get('doc_types') and isinstance(st.session_state.get('doc_types'), str):
                    existing_doc_types = st.session_state.get('doc_types').split(',')
                
                doc_types = st.multiselect(
                    "What types of documents do you create most often?",
                    ["Proposals", "Invoices", "NDAs", "Letters of Intent", "Scope of Work"],
                    default=existing_doc_types
                )
                
                # Get existing team size
                team_size_options = ["1-10", "11-50", "51-200", "201-500", "500+"]
                default_team_size = user_info.get('team_size', st.session_state.get('team_size', '1-10'))
                default_index = team_size_options.index(default_team_size) if default_team_size in team_size_options else 0
                
                team_size = st.select_slider(
                    "Team size",
                    options=team_size_options,
                    value=team_size_options[default_index]
                )
                
                # Optional description
                company_description = st.text_area(
                    "Brief description of your company (optional)",
                    value=user_info.get('company_description', st.session_state.get('company_description', '')),
                    placeholder="Tell us a bit about what your company does..."
                )
                
                # Form buttons
                col1, col2 = st.columns([1, 1])
                with col1:
                    back = st.form_submit_button("← Back", type="secondary")
                    if back:
                        st.session_state.onboarding_step = 1
                        st.rerun()
                with col2:
                    complete = st.form_submit_button("Complete ✓", type="primary")
                    if complete:
                        # Save all data and complete onboarding
                        save_onboarding_data({
                            "company_name": st.session_state.get('company_name', ''),
                            "industry": st.session_state.get('industry', ''),
                            "business_type": st.session_state.get('business_type', 'Other'),
                            "doc_types": doc_types,
                            "team_size": team_size,
                            "company_description": company_description
                        })
                        complete_onboarding()
    
    # Close the container div
    st.markdown('</div>', unsafe_allow_html=True)

def complete_onboarding():
    """Mark onboarding as completed and refresh the page"""
    # If user skipped the onboarding, we still want to mark it as completed
    # but we don't want to lose any existing data
    user_info = get_user_info() or {}
    
    # Only update the onboarding_completed flag if we're skipping
    # Otherwise, the save_onboarding_data function will handle it
    if not st.session_state.get('company_name'):
        update_user_info(st.session_state.user_id, {
            "onboarding_completed": True
        })
    
    st.session_state.onboarding_completed = True
    st.rerun()

# Check authentication first
if not check_authentication():
    st.warning("Please log in to access this page")
    st.switch_page("pages/login.py")
    st.stop()

def load_user_data_to_session():
    """Load user data into session state for use across the app"""
    user_info = get_user_info()
    if not user_info:
        return
        
    # Store user data in session state for use across the app
    for key, value in user_info.items():
        if key not in st.session_state:
            st.session_state[key] = value

def display_dashboard():
    # Load user data into session state
    load_user_data_to_session()
        
    apply_custom_css()
    
    # Header with profile preview
    header_col1, header_col2 = st.columns([6,1])
    with header_col1:
        credits = get_user_credits(st.session_state.get('user_id'))
        st.markdown("""
            <div class="card" style="margin-bottom: 2rem;">
                <div style="display: flex; align-items: center; gap: 1.5rem;">
                    <div class="profile-avatar">👤</div>
                    <div>
                        <h1 style="margin: 0; font-size: 1.8rem;">Welcome back, {name}</h1>
                        <p style="margin: 0.5rem 0 0 0; opacity: 0.7">{email}</p>
                        <div style="display: flex; gap: 1rem; align-items: center; margin-top: 0.5rem;">
                            <div class="subscription-badge">{plan}</div>
                            {credits_display}
                        </div>
                    </div>
                </div>
            </div>
        """.format(
            name=st.session_state.get('name', 'User'),
            email=st.session_state.get('email', 'user@example.com'),
            plan=st.session_state.get('subscription', 'FREE').upper(),
            credits_display=f'<div style="opacity: 0.8;">Available Credits: {credits}</div>' if st.session_state.get('subscription') != 'pro' else ''
        ), unsafe_allow_html=True)
    
    with header_col2:
        if st.button("👤 Profile", use_container_width=True):
            st.switch_page("pages/3_Account.py")
    
    # Stats Section
    st.markdown("""
        <div class="stats-container">
            <div class="stat-card">
                <h3 style="margin: 0; opacity: 0.7;">Documents Created</h3>
                <div class="stat-value">{docs}/{limit}
                    <span style="font-size: 1rem; opacity: 0.7">
                        {period}
                    </span>
                </div>
                <div class="progress-bar">
                    <div class="progress-bar-fill" style="width: {doc_progress}%;"></div>
                </div>
            </div>
            <div class="stat-card">
                <h3 style="margin: 0; opacity: 0.7;">Storage Used</h3>
                <div class="stat-value">{storage_display}<span style="font-size: 1rem; opacity: 0.7">{storage_unit}</span></div>
                <div class="progress-bar">
                    <div class="progress-bar-fill" style="width: {storage_progress}%;"></div>
                </div>
            </div>
            <div class="stat-card">
                <h3 style="margin: 0; opacity: 0.7;">AI Credits</h3>
                <div class="stat-value">{credits_val}</div>
                <div class="progress-bar">
                    <div class="progress-bar-fill" style="width: {credits_progress}%;"></div>
                </div>
            </div>
        </div>
    """.format(
        docs=st.session_state.get('free_docs_used', 0),
        limit='∞' if st.session_state.get('subscription') == 'pro' else '3',
        period='this month' if st.session_state.get('subscription') == 'pro' else 'remaining',
        doc_progress=min((st.session_state.get('free_docs_used', 0) / 3) * 100, 100) if st.session_state.get('subscription') != 'pro' else 50,
        # Calculate storage values
        storage_display=get_storage_display_values(st.session_state.get('user_id'))[0],
        storage_unit=get_storage_display_values(st.session_state.get('user_id'))[1],
        storage_progress=get_storage_display_values(st.session_state.get('user_id'))[2],
        credits_val='Unlimited' if st.session_state.get('subscription') == 'pro' else credits,
        credits_progress=100 if st.session_state.get('subscription') == 'pro' else (credits / 50) * 100
    ), unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown("### 📝 Quick Actions")
    
    # Template grid
    template_data = [
        {"name": "NDA", "icon": "🤝", "desc": "Create a Non-Disclosure Agreement", "credits": 5},
        {"name": "Invoice", "icon": "💰", "desc": "Generate a professional invoice", "credits": 3},
        {"name": "Proposal", "icon": "📊", "desc": "Draft a business proposal", "credits": 8},
        {"name": "Letter of Intent", "icon": "✍️", "desc": "Write a letter of intent", "credits": 4},
        {"name": "Scope of Work", "icon": "📋", "desc": "Define project scope", "credits": 10},
    ]
    
    cols = st.columns(3)
    for idx, template in enumerate(template_data):
        with cols[idx % 3]:
            credit_info = "" if st.session_state.get('subscription') == 'pro' else f"<p style='color: #3fd7a5;'>{template['credits']} credits</p>"
            st.markdown(f"""
                <div class="card" style="cursor: pointer; transition: transform 0.2s;" 
                     onmouseover="this.style.transform='translateY(-5px)'" 
                     onmouseout="this.style.transform='translateY(0)'">
                    <h3>{template['icon']} {template['name']}</h3>
                    <p style="opacity: 0.7">{template['desc']}</p>
                    {credit_info}
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"Generate {template['name']}", key=f"template_{idx}", use_container_width=True):
                st.session_state.selected_template = template['name'].lower().replace(" ", "_")
                st.switch_page("pages/1_Generate_Document.py")
    
    # Upgrade Card for Free Users
    if st.session_state.get('subscription') != 'pro':
        st.markdown("""
            <div class="card" style="background: linear-gradient(135deg, rgba(63, 215, 165, 0.1) 0%, rgba(38, 133, 108, 0.1) 100%);">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h2 style="margin: 0;">🌟 Upgrade to Pro</h2>
                        <p style="margin: 0.5rem 0;">Unlock unlimited documents and premium features</p>
                    </div>
                    <div>
                        <button class="button-primary" onclick="window.location.href='pages/3_Account.py'">
                            Upgrade Now
                        </button>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Get user stats
    user_info = get_user_info()
    if not user_info:
        st.error("Error loading user information")
        return
    
    # Recent Documents
    st.subheader("Recent Documents")
    recent_docs = get_recent_documents(st.session_state.user_id)
    
    if not recent_docs:
        st.info("No documents generated yet. Start by creating your first document!")
        if st.button("Generate Document"):
            st.switch_page("pages/1_Generate_Document.py")
    else:
        for doc in recent_docs:
            with st.expander(f"{doc['title']} ({get_document_display_name(doc['doc_type'])})"):
                col1, col2 = st.columns([3,1])
                with col1:
                    st.caption(f"Created: {format_date(doc['created_at'])}")
                    st.caption(f"Credits Used: {doc['credits_used']}")
                with col2:
                    if st.button("Generate Similar", key=f"gen_similar_{doc['id']}"):
                        st.session_state.template_doc = doc
                        st.switch_page("pages/1_Generate_Document.py")

def main():
    # Set current page for sidebar highlighting
    st.session_state['current_page'] = __file__
    
    # Create sidebar
    create_sidebar()
    
    # Display dashboard content
    display_dashboard()

if __name__ == "__main__":
    main()

