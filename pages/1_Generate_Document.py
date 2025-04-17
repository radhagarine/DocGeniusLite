import streamlit as st
import os
import json
import sys
import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auth import check_authentication, get_user_info, update_user_info
from document_generator import (
    get_document_parameters, 
    generate_document_content, 
    generate_pdf, 
    generate_docx,
    get_industry_profile
)
from utils.document import (
    get_document_display_name, 
    get_document_description, 
    create_download_link, 
    display_rai_indicator,
    calculate_required_credits,
    get_user_credits,
    deduct_credits
)
from utils.sidebar import create_sidebar

def next_step():
    st.session_state.wizard_step += 1

def prev_step():
    st.session_state.wizard_step -= 1

def reset_wizard():
    st.session_state.wizard_step = 1
    st.session_state.doc_type = None
    st.session_state.doc_params = {}
    st.session_state.generated_content = None
    st.session_state.rai_results = None

# Page configuration
st.set_page_config(
    page_title="Generate Document - DocGenius Lite",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set current page for sidebar highlighting
st.session_state['current_page'] = __file__

# Create sidebar
create_sidebar()

# Check authentication
if not check_authentication():
    st.warning("Please log in to access this page")
    st.stop()

# Load user data into session state if not already there
def load_user_data_to_session():
    """Load user data into session state for use across the app"""
    user_info = get_user_info()
    if not user_info:
        return
        
    # Store user data in session state for use across the app
    for key, value in user_info.items():
        if key not in st.session_state:
            st.session_state[key] = value
            
# Load user data
load_user_data_to_session()

# Initialize session state for document wizard
if 'wizard_step' not in st.session_state:
    st.session_state.wizard_step = 1

if 'doc_type' not in st.session_state:
    st.session_state.doc_type = None

if 'doc_params' not in st.session_state:
    st.session_state.doc_params = {}

if 'generated_content' not in st.session_state:
    st.session_state.generated_content = None

if 'rai_results' not in st.session_state:
    st.session_state.rai_results = None

# Get user's industry profile
profile = get_industry_profile(st.session_state.get('user_id'))
if not profile and st.session_state.wizard_step == 1:
    st.warning("Please complete your industry profile to better personalize your documents")
    if st.button("Complete Profile"):
        st.switch_page("pages/onboarding.py")

# Document types
DOC_TYPES = {
    "nda": "Non-Disclosure Agreement",
    "invoice": "Invoice",
    "letter_of_intent": "Letter of Intent",
    "proposal": "Business Proposal",
    "scope_of_work": "Scope of Work"
}

# Main content
st.title("Generate Document")

# Calculate required credits for selected document type
def get_required_credits():
    if not st.session_state.doc_type:
        return 0
    return calculate_required_credits(st.session_state.doc_type)

# Check if user has enough credits
def check_credits():
    if st.session_state.get('subscription') == 'pro':
        return True
    
    required_credits = get_required_credits()
    available_credits = get_user_credits(st.session_state.get('user_id'))
    
    return available_credits >= required_credits

# Wizard Step 1: Select Document Type
if st.session_state.wizard_step == 1:
    st.subheader("Step 1: Select Document Type")
    
    # Display available credits for free users
    if st.session_state.get('subscription') != 'pro':
        credits = get_user_credits(st.session_state.get('user_id'))
        st.info(f"Available AI Credits: {credits}")
    
    # If profile exists, show personalized recommendations
    if profile:
        st.markdown("### 🎯 Recommended for Your Industry")
        industry_docs = []
        if profile['industry'] == 'Technology & Software':
            industry_docs = ['proposal', 'scope_of_work', 'nda']
        elif profile['industry'] == 'Healthcare':
            industry_docs = ['nda', 'scope_of_work', 'letter_of_intent']
        elif profile['industry'] == 'Finance & Banking':
            industry_docs = ['nda', 'proposal', 'letter_of_intent']
        
        for doc_type in industry_docs:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"### {DOC_TYPES[doc_type]}")
                st.markdown(get_document_description(doc_type))
                credit_cost = calculate_required_credits(doc_type)
                if st.session_state.get('subscription') != 'pro':
                    st.caption(f"Cost: {credit_cost} credits")
            with col2:
                if st.button(f"Select", key=f"select_{doc_type}_recommended"):
                    st.session_state.doc_type = doc_type
                    if check_credits():
                        next_step()
                    else:
                        st.error(f"Insufficient credits. You need {credit_cost} credits to generate this document.")
                        st.info("Purchase more credits or upgrade to Pro for unlimited document generation.")
                        if st.button("Purchase Credits"):
                            st.switch_page("pages/3_Account.py")
                        st.stop()
        
        st.markdown("### 📄 All Document Types")
    
    # Document type selection
    for doc_type, display_name in DOC_TYPES.items():
        if not profile or doc_type not in industry_docs:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"### {display_name}")
                st.markdown(get_document_description(doc_type))
                credit_cost = calculate_required_credits(doc_type)
                if st.session_state.get('subscription') != 'pro':
                    st.caption(f"Cost: {credit_cost} credits")
            with col2:
                if st.button(f"Select", key=f"select_{doc_type}"):
                    st.session_state.doc_type = doc_type
                    if check_credits():
                        next_step()
                    else:
                        st.error(f"Insufficient credits. You need {credit_cost} credits to generate this document.")
                        st.info("Purchase more credits or upgrade to Pro for unlimited document generation.")
                        if st.button("Purchase Credits"):
                            st.switch_page("pages/3_Account.py")
                        st.stop()

# Wizard Step 2: Fill Parameters
elif st.session_state.wizard_step == 2:
    st.subheader(f"Step 2: Fill {DOC_TYPES[st.session_state.doc_type]} Details")
    
    # Get parameters for selected document type
    parameters = get_document_parameters(st.session_state.doc_type)
    
    # Pre-fill form with user information from onboarding
    if not st.session_state.doc_params:
        # Get user info from session state or database
        user_info = {}
        for key in ['company_name', 'industry', 'business_type', 'company_description', 'team_size']:
            if key in st.session_state:
                user_info[key] = st.session_state.get(key)
        
        # Initialize doc_params with user information
        st.session_state.doc_params = {
            # Business information
            'business_name': user_info.get('company_name', ''),
            'company_name': user_info.get('company_name', ''),
            'industry': user_info.get('industry', ''),
            'business_type': user_info.get('business_type', ''),
            'company_description': user_info.get('company_description', ''),
            'company_logo': st.session_state.get('company_logo', ''),
            
            # If we have user contact info
            'business_email': st.session_state.get('email', ''),
            'contact_email': st.session_state.get('email', ''),
            'contact_name': st.session_state.get('name', ''),
            
            # Current date for date fields
            'date': datetime.date.today(),
            'invoice_date': datetime.date.today(),
            'effective_date': datetime.date.today(),
            
            # Due date (30 days from today)
            'due_date': datetime.date.today() + datetime.timedelta(days=30),
            
            # Default currency
            'currency': 'USD',
            
            # Default payment terms
            'payment_terms': 'Net 30'
        }
        
        # Add any additional fields from profile if it exists
        if profile:
            for key, value in profile.items():
                if key not in st.session_state.doc_params and value:
                    st.session_state.doc_params[key] = value
    
    # Add autofill toggle
    use_autofill = st.checkbox("Use information from your profile (autofill)", value=True, 
                              help="Automatically fill form fields with information from your profile")
    
    if not use_autofill:
        # Clear pre-filled values if autofill is disabled
        st.session_state.doc_params = {}
        st.info("Autofill disabled. Please fill in all fields manually.")
    
    # Parameter input form
    with st.form("document_params"):
        for section in parameters:
            st.markdown(f"### {section['section']}")
            
            for param in section['fields']:
                param_id = param['id']
                default_value = st.session_state.doc_params.get(param_id, '')
                
                # Choose appropriate input based on parameter type
                if param['type'] == 'text':
                    value = st.text_input(
                        param['label'], 
                        value=default_value,
                        help=param.get('help', ''),
                        key=f"param_{param_id}"
                    )
                elif param['type'] == 'textarea':
                    value = st.text_area(
                        param['label'], 
                        value=default_value,
                        help=param.get('help', ''),
                        key=f"param_{param_id}"
                    )
                elif param['type'] == 'date':
                    value = st.date_input(
                        param['label'],
                        value=default_value if default_value else None,
                        help=param.get('help', ''),
                        key=f"param_{param_id}"
                    )
                elif param['type'] == 'number':
                    value = st.number_input(
                        param['label'],
                        value=float(default_value) if default_value else 0.0,
                        help=param.get('help', ''),
                        key=f"param_{param_id}"
                    )
                elif param['type'] == 'select':
                    value = st.selectbox(
                        param['label'],
                        options=param['options'],
                        index=param['options'].index(default_value) if default_value in param['options'] else 0,
                        help=param.get('help', ''),
                        key=f"param_{param_id}"
                    )
                
                # Store value in session state
                st.session_state.doc_params[param_id] = value
                
                # Save business address to user profile if it's entered and not already saved
                if param_id == 'business_address' and value and use_autofill and 'business_address' not in st.session_state:
                    st.session_state.business_address = value
        
        # Form submission buttons
        col1, col2 = st.columns(2)
        with col1:
            back_button = st.form_submit_button("← Back")
        with col2:
            next_button = st.form_submit_button("Generate Document →")
    
    # Handle form submission
    if back_button:
        prev_step()
    
    if next_button:
        # Validate required fields
        required_fields = []
        for section in parameters:
            for param in section['fields']:
                if param.get('required', False):
                    if not st.session_state.doc_params.get(param['id']):
                        required_fields.append(param['label'])
        
        if required_fields:
            st.error(f"Please fill in the following required fields: {', '.join(required_fields)}")
        else:
            try:
                # Save business information to user profile if autofill is enabled
                if use_autofill:
                    business_fields = {
                        'business_name': 'company_name',
                        'business_address': 'business_address',
                        'business_phone': 'business_phone',
                        'business_email': 'business_email'
                    }
                    
                    update_data = {}
                    for form_field, profile_field in business_fields.items():
                        if form_field in st.session_state.doc_params and st.session_state.doc_params[form_field]:
                            update_data[profile_field] = st.session_state.doc_params[form_field]
                    
                    if update_data:
                        # Update session state
                        for key, value in update_data.items():
                            st.session_state[key] = value
                        
                        # Update user profile in database
                        update_user_info(st.session_state.user_id, update_data)
                
                # Generate document content with industry profile
                st.session_state.generated_content = generate_document_content(
                    st.session_state.doc_type, 
                    st.session_state.doc_params,
                    st.session_state.get('user_id')  # Pass user_id for industry customization
                )
                
                # Get RAI analysis
                from rai import analyze_document
                st.session_state.rai_results = analyze_document(
                    st.session_state.generated_content,
                    st.session_state.doc_type
                )
                
                # Deduct credits if not on pro plan
                if st.session_state.get('subscription') != 'pro':
                    credits_required = calculate_required_credits(st.session_state.doc_type)
                    success = deduct_credits(
                        st.session_state.get('user_id'),
                        credits_required,
                        None,  # Document ID will be updated after saving
                        f"Generated {DOC_TYPES[st.session_state.doc_type]}"
                    )
                    
                    if not success:
                        st.error("Failed to deduct credits. Please try again.")
                        st.stop()
                
                next_step()
                
            except Exception as e:
                st.error(f"Error generating document: {str(e)}")

# Wizard Step 3: Preview and Export
elif st.session_state.wizard_step == 3:
    st.subheader(f"Step 3: Preview Your {DOC_TYPES[st.session_state.doc_type]}")
    
    # Display RAI indicator
    st.markdown("### Document Trust Score")
    display_rai_indicator(
        st.session_state.rai_results['score'],
        st.session_state.rai_results['flags']
    )
    
    # Display document preview
    st.markdown("### Document Preview")
    st.markdown(st.session_state.generated_content, unsafe_allow_html=True)
    
    # Export options
    st.markdown("### Export Options")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Generate PDF"):
            with st.spinner("Generating PDF..."):
                pdf_path = generate_pdf(
                    st.session_state.generated_content,
                    f"{DOC_TYPES[st.session_state.doc_type]}"
                )
                st.markdown(create_download_link(pdf_path, "Download PDF"), unsafe_allow_html=True)
                os.unlink(pdf_path)
    
    with col2:
        if st.button("Generate DOCX"):
            with st.spinner("Generating DOCX..."):
                docx_path = generate_docx(
                    st.session_state.generated_content,
                    f"{DOC_TYPES[st.session_state.doc_type]}"
                )
                st.markdown(create_download_link(docx_path, "Download DOCX"), unsafe_allow_html=True)
                os.unlink(docx_path)
    
    # Feedback and buttons
    st.markdown("### How would you rate this document?")
    rating = st.slider("Rating", 1, 5, 5)
    feedback = st.text_area("Comments (optional)")
    
    if st.button("Submit Feedback & Create New Document"):
        # In a real implementation, save feedback to database
        st.success("Thank you for your feedback!")
        reset_wizard()
    
    # Back button
    if st.button("← Back to Edit"):
        prev_step()
