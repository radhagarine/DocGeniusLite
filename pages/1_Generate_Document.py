import streamlit as st
import os
import json
import requests
import base64
from auth import check_authentication
from document_generator import get_document_parameters, generate_document_content, generate_pdf, generate_docx
from utils import get_document_display_name, get_document_description, create_download_link, display_rai_indicator, can_create_document

# Page configuration
st.set_page_config(
    page_title="Generate Document - DocGenius Lite",
    page_icon="📄",
    layout="wide"
)

# Check authentication
if not check_authentication():
    st.warning("Please log in to access this page")
    st.stop()

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

# Functions to navigate wizard
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

# Check if user can create a document
can_create, message = can_create_document()
if not can_create:
    st.warning(message)
    
    # Offer options to purchase or upgrade
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Purchase This Document ($3)", key="purchase_single"):
            st.session_state.wizard_step = 4  # Skip to payment step
    with col2:
        if st.button("Upgrade to Pro ($9/month)", key="upgrade_pro"):
            st.switch_page("pages/3_Account.py")
    
    st.stop()

# Wizard Step 1: Select Document Type
if st.session_state.wizard_step == 1:
    st.subheader("Step 1: Select Document Type")
    
    # Display document type options in a grid
    col1, col2 = st.columns(2)
    
    with col1:
        for doc_type in list(DOC_TYPES.keys())[:3]:
            if st.button(DOC_TYPES[doc_type], key=f"btn_{doc_type}", use_container_width=True):
                st.session_state.doc_type = doc_type
                next_step()
    
    with col2:
        for doc_type in list(DOC_TYPES.keys())[3:]:
            if st.button(DOC_TYPES[doc_type], key=f"btn_{doc_type}", use_container_width=True):
                st.session_state.doc_type = doc_type
                next_step()
    
    # Display document descriptions
    if 'selected_doc_info' not in st.session_state:
        st.session_state.selected_doc_info = list(DOC_TYPES.keys())[0]
    
    st.session_state.selected_doc_info = st.selectbox(
        "View document information:",
        options=list(DOC_TYPES.keys()),
        format_func=lambda x: DOC_TYPES[x],
        index=list(DOC_TYPES.keys()).index(st.session_state.selected_doc_info)
    )
    
    st.info(get_document_description(st.session_state.selected_doc_info))

# Wizard Step 2: Fill Document Parameters
elif st.session_state.wizard_step == 2:
    st.subheader(f"Step 2: Complete {DOC_TYPES[st.session_state.doc_type]} Details")
    
    # Get parameters for the selected document type
    parameters = get_document_parameters(st.session_state.doc_type)
    
    # Create a form for document parameters
    with st.form("document_params_form"):
        st.write("Please fill in the following information:")
        
        # Display parameter inputs grouped by sections
        for section in parameters:
            st.markdown(f"### {section['section']}")
            
            for param in section['fields']:
                param_id = param['id']
                
                # Set default value from session state if exists
                default_value = st.session_state.doc_params.get(param_id, param.get('default', ''))
                
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
        
        # Form submission buttons
        col1, col2 = st.columns(2)
        with col1:
            back_button = st.form_submit_button("← Back")
        with col2:
            next_button = st.form_submit_button("Preview Document →")
    
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
            # Generate document content
            try:
                st.session_state.generated_content = generate_document_content(
                    st.session_state.doc_type, 
                    st.session_state.doc_params
                )
                
                # Get RAI analysis
                # In a real implementation, this would call the API to get analysis
                # For this demo, we'll use a placeholder
                from rai import analyze_document
                st.session_state.rai_results = analyze_document(
                    st.session_state.generated_content,
                    st.session_state.doc_type
                )
                
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
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Generate PDF"):
            with st.spinner("Generating PDF..."):
                pdf_path = generate_pdf(
                    st.session_state.generated_content,
                    f"{DOC_TYPES[st.session_state.doc_type]}"
                )
                st.markdown(create_download_link(pdf_path, "Download PDF"), unsafe_allow_html=True)
                os.unlink(pdf_path)  # Clean up the file after providing the download link
    
    with col2:
        if st.button("Generate DOCX"):
            with st.spinner("Generating DOCX..."):
                docx_path = generate_docx(
                    st.session_state.generated_content,
                    f"{DOC_TYPES[st.session_state.doc_type]}",
                    st.session_state.doc_type
                )
                st.markdown(create_download_link(docx_path, "Download DOCX"), unsafe_allow_html=True)
                os.unlink(docx_path)  # Clean up the file after providing the download link
    
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

# Wizard Step 4: Payment (if needed)
elif st.session_state.wizard_step == 4:
    st.subheader("Document Purchase")
    
    st.info("This document will cost $3.00 USD.")
    
    # Simulate credit card input
    st.markdown("### Payment Information")
    with st.form("payment_form"):
        st.text_input("Card Number", placeholder="4242 4242 4242 4242")
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Expiration Date", placeholder="MM/YY")
        with col2:
            st.text_input("CVC", placeholder="123")
        
        st.text_input("Name on Card", placeholder="John Smith")
        
        submit_payment = st.form_submit_button("Pay $3.00")
    
    if submit_payment:
        # In a real app, this would process the payment through Stripe
        st.success("Payment successful! Your document is now available.")
        
        # Update user's document count in session
        st.session_state.free_docs_used = st.session_state.get('free_docs_used', 0) + 1
        
        # Go to document preview
        st.session_state.wizard_step = 3
        st.rerun()
    
    if st.button("← Back"):
        prev_step()
