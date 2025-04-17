import streamlit as st
import sys
import os
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auth import check_authentication, logout, get_user_info, update_user_info, delete_user
from utils.document import (
    get_document_display_name,
    get_user_credits,
    get_credit_history,
    add_credits,
    get_document_count,
    get_user_storage_used
)
from utils.sidebar import create_sidebar
from utils.styles import add_home_button

def format_date_display(date_value):
    """Format a date value for display, handling both string and datetime objects"""
    if isinstance(date_value, datetime):
        return date_value.strftime('%B %d, %Y %H:%M')
    elif isinstance(date_value, str):
        try:
            # Try to parse the string as a datetime
            dt = datetime.fromisoformat(date_value.replace('Z', '+00:00'))
            return dt.strftime('%B %d, %Y %H:%M')
        except (ValueError, TypeError):
            # If parsing fails, return the original string
            return date_value
    else:
        # For any other type, convert to string
        return str(date_value)

# Page configuration
st.set_page_config(
    page_title="Account - DocGenius Lite",
    page_icon="👤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set current page for sidebar highlighting
st.session_state['current_page'] = __file__

# Create sidebar
create_sidebar()

# Add a Home button at the top
add_home_button()

# Check authentication
if not check_authentication():
    st.warning("Please log in to access this page")
    st.stop()

# Get user info for profile section
user_info = get_user_info() or {}

# Custom CSS for modern card-based design
st.markdown("""
    <style>
    .profile-card {
        background: rgba(22, 68, 48, 0.3);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 2rem;
        border: 1px solid rgba(63, 215, 165, 0.2);
        margin-bottom: 2rem;
    }
    .profile-header {
        display: flex;
        align-items: center;
        gap: 1.5rem;
        margin-bottom: 2rem;
    }
    .profile-avatar {
        width: 80px;
        height: 80px;
        background: linear-gradient(135deg, #3fd7a5 0%, #26856c 100%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        color: white;
    }
    .profile-info h1 {
        margin: 0;
        font-size: 1.8rem;
        color: #f4f9f7;
    }
    .profile-info p {
        margin: 0.5rem 0 0 0;
        color: rgba(244, 249, 247, 0.7);
    }
    .stat-card {
        background: rgba(10, 40, 23, 0.3);
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid rgba(63, 215, 165, 0.1);
    }
    .subscription-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        background: linear-gradient(135deg, #3fd7a5 0%, #26856c 100%);
        border-radius: 20px;
        font-size: 0.8rem;
        margin-top: 0.5rem;
    }
    .credit-history {
        margin-top: 1rem;
    }
    .credit-transaction {
        background: rgba(10, 40, 23, 0.3);
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
        border: 1px solid rgba(63, 215, 165, 0.1);
    }
    .credit-amount {
        font-weight: bold;
        color: #3fd7a5;
    }
    .credit-amount.negative {
        color: #ff4b4b;
    }
    </style>
""", unsafe_allow_html=True)

# Main content
st.markdown("""
    <div class="profile-card">
        <div class="profile-header">
            <div class="profile-avatar">👤</div>
            <div class="profile-info">
                <h1>{name}</h1>
                <p>{email}</p>
                <div class="subscription-badge">{plan}</div>
            </div>
        </div>
    </div>
""".format(
    name=st.session_state.get('name', 'User'),
    email=st.session_state.get('email', 'Not available'),
    plan=st.session_state.get('subscription', 'FREE').upper()
), unsafe_allow_html=True)

# Business Profile (moved from onboarding)
st.markdown("### 🏢 Business Profile")

# Create tabs for different profile sections
profile_tab, company_tab = st.tabs(["Personal Information", "Company Information"])

with profile_tab:
    col1, col2 = st.columns(2)
    with col1:
        profile_name = st.text_input("Name", value=user_info.get('name', ''), key="profile_name")
    with col2:
        st.text_input("Email", value=user_info.get('email', ''), disabled=True)
        
    # Save button for profile tab
    if st.button("Save Personal Information", key="save_profile"):
        # Update the user's profile information
        update_data = {
            "name": profile_name
        }
        
        with st.spinner("Updating profile information..."):
            if update_user_info(st.session_state.user_id, update_data):
                # Update session state to reflect changes
                st.session_state.name = profile_name
                st.success("Profile information updated successfully!")
                # Use rerun to refresh the page with updated data
                st.rerun()
            else:
                st.error("Failed to update profile information. Please try again.")

with company_tab:
    col1, col2 = st.columns(2)
    with col1:
        # Get default values from user_info with fallbacks
        default_company_name = user_info.get('company_name', '')
        
        # Get industry with proper default handling
        industry_options = ["Technology", "Healthcare", "Finance", "Education", "Other"]
        default_industry = user_info.get('industry', 'Technology')
        industry_index = 0  # Default to first option
        
        if default_industry in industry_options:
            industry_index = industry_options.index(default_industry)
            
        # Get business type with proper default handling
        business_type_options = ["B2B", "B2C", "Non-profit", "Government", "Other"]
        default_business_type = user_info.get('business_type', 'B2B')
        business_type_index = 0  # Default to first option
        
        if default_business_type in business_type_options:
            business_type_index = business_type_options.index(default_business_type)
        
        # Display form fields with proper defaults
        company_name = st.text_input("Company Name", value=default_company_name)
        industry = st.selectbox(
            "Industry",
            industry_options,
            index=industry_index
        )
        business_type = st.selectbox(
            "Business Type",
            business_type_options,
            index=business_type_index
        )
    
    with col2:
        # Get team size with proper default handling
        team_size_options = ["1-10", "11-50", "51-200", "201-500", "500+"]
        default_team_size = user_info.get('team_size', '1-10')
        
        # Make sure the default value is in the options
        if default_team_size not in team_size_options:
            default_team_size = "1-10"
            
        team_size = st.select_slider(
            "Team Size",
            options=team_size_options,
            value=default_team_size
        )
        business_address = st.text_input("Business Address", value=user_info.get('business_address', ''))
        
        # Phone number with validation
        business_phone = st.text_input(
            "Business Phone", 
            value=user_info.get('business_phone', ''),
            help="Enter a valid phone number (e.g., +1-555-123-4567)"
        )
        
        # Simple phone validation
        if business_phone and not (
            business_phone.replace('-', '').replace('+', '').replace(' ', '').replace('(', '').replace(')', '').isdigit() and
            len(business_phone.replace('-', '').replace('+', '').replace(' ', '').replace('(', '').replace(')', '')) >= 7
        ):
            st.warning("Please enter a valid phone number")
    
    # Document types
    st.subheader("Document Preferences")
    doc_types_options = ["Proposals", "Invoices", "NDAs", "Letters of Intent", "Scope of Work"]
    
    # Get existing doc types from user info
    existing_doc_types = []
    if user_info.get('doc_types'):
        existing_doc_types = user_info.get('doc_types').split(',')
    
    doc_types = st.multiselect(
        "What types of documents do you create most often?",
        doc_types_options,
        default=existing_doc_types
    )
    
    # Company description
    company_description = st.text_area(
        "Brief description of your company",
        value=user_info.get('company_description', ''),
        placeholder="Tell us a bit about what your company does..."
    )
    
    # Save button for company tab
    if st.button("Save Company Information", key="save_company"):
        # Here you would update the user's company information
        update_data = {
            "company_name": company_name,
            "industry": industry,
            "business_type": business_type,
            "team_size": team_size,
            "business_address": business_address,
            "business_phone": business_phone,
            "doc_types": ','.join(doc_types) if isinstance(doc_types, list) else doc_types,
            "company_description": company_description,
            "onboarding_completed": True
        }
        
        if update_user_info(st.session_state.user_id, update_data):
            st.success("Company information updated successfully!")
        else:
            st.error("Failed to update company information. Please try again.")

# Usage Stats
col1, col2, col3 = st.columns(3)
with col1:
    # Get actual document count
    doc_count = get_document_count(st.session_state.get('user_id', ''))
    
    st.markdown("""
        <div class="stat-card">
            <h3>Documents Created</h3>
            <h2>{} <span style="font-size: 0.8rem; opacity: 0.7;">of {}</span></h2>
        </div>
    """.format(
        doc_count,
        'Unlimited' if st.session_state.get('subscription') == 'pro' else '3'
    ), unsafe_allow_html=True)

with col2:
    # Get actual storage used
    storage_used = get_user_storage_used(st.session_state.get('user_id', ''))
    storage_limit = 'Unlimited' if st.session_state.get('subscription') == 'pro' else '1'
    
    # Convert to GB if over 1000 MB
    if storage_used > 1000:
        storage_display = f"{storage_used/1000:.2f}<small>GB</small>"
    else:
        storage_display = f"{storage_used}<small>MB</small>"
    
    st.markdown(f"""
        <div class="stat-card">
            <h3>Storage Used</h3>
            <h2>{storage_display} <span style="font-size: 0.8rem; opacity: 0.7;">of {storage_limit}GB</span></h2>
        </div>
    """, unsafe_allow_html=True)

with col3:
    credits = get_user_credits(st.session_state.get('user_id'))
    st.markdown("""
        <div class="stat-card">
            <h3>AI Credits</h3>
            <h2>{}</h2>
        </div>
    """.format('Unlimited' if st.session_state.get('subscription') == 'pro' else credits), unsafe_allow_html=True)

# Credit Management (for free users)
if st.session_state.get('subscription') != 'pro':
    st.markdown("### 💎 AI Credits")
    
    credit_packages = [
        {"amount": 50, "price": 5},
        {"amount": 100, "price": 9},
        {"amount": 200, "price": 15}
    ]
    
    col1, col2, col3 = st.columns(3)
    for idx, package in enumerate(credit_packages):
        with [col1, col2, col3][idx]:
            st.markdown(f"""
                <div style='background: rgba(63, 215, 165, 0.1); padding: 1rem; border-radius: 8px; text-align: center;'>
                    <h3>{package['amount']} Credits</h3>
                    <p style='font-size: 1.5rem; color: #3fd7a5;'>${package['price']}</p>
                    <p style='opacity: 0.7;'>${package['price']/package['amount']:.2f}/credit</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"Purchase ${package['price']}", key=f"buy_credits_{package['amount']}"):
                try:
                    # Here you would integrate with your payment processor (e.g., Stripe)
                    # For demo, we'll just add the credits
                    add_credits(
                        st.session_state.get('user_id'),
                        package['amount'],
                        f"Purchased {package['amount']} credits"
                    )
                    st.success(f"Successfully added {package['amount']} credits!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to purchase credits: {str(e)}")
    
    # Credit History
    st.markdown("### 📊 Credit History")
    transactions = get_credit_history(st.session_state.get('user_id'))
    
    if transactions:
        for transaction in transactions:
            amount, trans_type, description, created_at, doc_title = transaction
            st.markdown(f"""
                <div class="credit-transaction">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong>{description}</strong><br>
                            <small style="opacity: 0.7;">{format_date_display(created_at)}</small>
                        </div>
                        <div class="credit-amount {'negative' if amount < 0 else ''}">
                            {amount:+d} credits
                        </div>
                    </div>
                    {f'<div style="margin-top: 0.5rem; opacity: 0.7;">Document: {doc_title}</div>' if doc_title else ''}
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No credit transactions yet.")

# Subscription Section
st.markdown("### 💫 Subscription")
if st.session_state.get('subscription') == 'pro':
    st.success("You're on the Pro plan!")
    if st.button("Manage Subscription"):
        st.info("This would open the subscription management portal in a real implementation.")
else:
    with st.expander("🌟 Upgrade to Pro - $9/month"):
        st.markdown("""
            <div style='background: rgba(63, 215, 165, 0.1); padding: 1rem; border-radius: 8px; margin-bottom: 1rem;'>
                <h4 style='margin: 0;'>Pro Plan Benefits</h4>
                <ul style='margin: 1rem 0;'>
                    <li>Unlimited document generation</li>
                    <li>No credit system - generate as many documents as you need</li>
                    <li>Priority support</li>
                    <li>Unlimited storage</li>
                    <li>Advanced AI features</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("upgrade_form"):
            st.text_input("Card Number", placeholder="4242 4242 4242 4242")
            col1, col2 = st.columns(2)
            with col1:
                st.text_input("Expiration Date", placeholder="MM/YY")
            with col2:
                st.text_input("CVC", placeholder="123")
            
            st.text_input("Name on Card", placeholder="John Smith")
            agree = st.checkbox("I agree to the terms of service")
            
            if st.form_submit_button("Subscribe - $9/month"):
                if agree:
                    st.success("🎉 Subscription successful! You now have Pro access.")
                    st.session_state['subscription'] = 'pro'
                    st.rerun()
                else:
                    st.error("Please agree to the terms of service")

# Preferences
st.markdown("### ⚙️ Preferences")

# Get current preferences from user_info
current_theme = user_info.get('theme_preference', 'System')
current_default_doc = user_info.get('default_doc_type', 'nda')
current_notifications = user_info.get('notification_preferences', 'Security Alerts').split(',') if user_info.get('notification_preferences') else ["Security Alerts"]

theme_pref = st.select_slider(
    "Theme Mode",
    options=["Light", "System", "Dark"],
    value=current_theme
)

doc_types = ["nda", "invoice", "letter_of_intent", "proposal", "scope_of_work"]
default_doc = st.selectbox(
    "Default Document Type",
    options=doc_types,
    index=doc_types.index(current_default_doc) if current_default_doc in doc_types else 0,
    format_func=get_document_display_name
)

notification_options = ["Document Generation Updates", "Security Alerts", "Product News", "Tips & Tutorials"]
notification_prefs = st.multiselect(
    "Notifications",
    notification_options,
    default=current_notifications
)

if st.button("Save Preferences", type="primary"):
    with st.spinner("Saving preferences..."):
        # Update user preferences
        update_data = {
            "theme_preference": theme_pref,
            "default_doc_type": default_doc,
            "notification_preferences": ','.join(notification_prefs) if notification_prefs else ""
        }
        
        if update_user_info(st.session_state.user_id, update_data):
            # Update session state
            st.session_state['theme_preference'] = theme_pref
            st.session_state['default_doc_type'] = default_doc
            st.session_state['notification_preferences'] = ','.join(notification_prefs)
            
            st.success("✅ Preferences saved successfully!")
        else:
            st.error("Failed to save preferences. Please try again.")

# Account Actions
st.markdown("### 🛠️ Account Actions")
col1, col2 = st.columns(2)
with col1:
    if st.button("📤 Log Out", type="secondary", use_container_width=True):
        logout()
        st.success("You have been logged out.")
        st.rerun()

with col2:
    if st.button("❌ Delete Account", type="secondary", use_container_width=True):
        with st.form(key="delete_account_form"):
            st.warning("⚠️ This action cannot be undone. All your data will be permanently deleted.")
            st.markdown("""
                **The following will be deleted:**
                - Your user profile and settings
                - All documents you've created
                - Credit transaction history
                - All other account data
            """)
            confirm = st.text_input("Type 'DELETE' to confirm")
            
            submit_button = st.form_submit_button("Permanently Delete My Account")
            
            if submit_button:
                if confirm == "DELETE":
                    with st.spinner("Deleting account..."):
                        success, message = delete_user(st.session_state.get('user_id'))
                        if success:
                            # Log the user out
                            logout()
                            st.success("Your account has been successfully deleted.")
                            st.info("You will be redirected to the home page in 5 seconds.")
                            # Add JavaScript to redirect after 5 seconds
                            st.markdown("""
                                <script>
                                    setTimeout(function() {
                                        window.location.href = "/";
                                    }, 5000);
                                </script>
                            """, unsafe_allow_html=True)
                            st.stop()
                        else:
                            st.error(f"Failed to delete account: {message}")
                else:
                    st.error("Please type 'DELETE' to confirm account deletion.")
