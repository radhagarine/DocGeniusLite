import streamlit as st
import base64
import os
import json
from datetime import datetime, timedelta

def format_date(date_obj):
    """Format a date object as a readable string"""
    if not date_obj:
        return ""
    return date_obj.strftime("%B %d, %Y")

def can_create_document():
    """Check if the user can create a new document based on their plan and usage"""
    # Pro users can always create documents
    if st.session_state.get('subscription') == 'pro':
        return True, None
    
    # Free users get 3 free documents per month
    free_docs_used = st.session_state.get('free_docs_used', 0)
    if free_docs_used < 3:
        return True, None
    
    return False, "You've reached your free document limit for this month. Purchase this document or upgrade to Pro."

def get_document_display_name(doc_type):
    """Convert document type to display name"""
    display_names = {
        "nda": "Non-Disclosure Agreement",
        "invoice": "Invoice",
        "letter_of_intent": "Letter of Intent",
        "proposal": "Business Proposal",
        "scope_of_work": "Scope of Work"
    }
    return display_names.get(doc_type, doc_type.replace("_", " ").title())

def get_document_description(doc_type):
    """Get a description for a document type"""
    descriptions = {
        "nda": "A legal contract that establishes a confidential relationship between parties. Used when sensitive information needs to be shared but protected from others.",
        "invoice": "A commercial document issued by a seller to a buyer, indicating the products, quantities, and agreed prices for products or services provided.",
        "letter_of_intent": "A document outlining the understanding between parties that wish to enter into a contract. It sets forth the main terms of a deal.",
        "proposal": "A document that offers a solution to a client's problem. Often used in business to suggest services or products to meet specific needs.",
        "scope_of_work": "A document that defines project-specific activities, deliverables, and timelines for a vendor providing services to a client."
    }
    return descriptions.get(doc_type, "")

def create_download_link(file_path, link_text):
    """Create a download link for a file"""
    with open(file_path, "rb") as f:
        file_bytes = f.read()
    
    b64 = base64.b64encode(file_bytes).decode()
    filename = os.path.basename(file_path)
    
    return f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">{link_text}</a>'

def display_rai_indicator(score, flags=None):
    """Display a Responsible AI indicator with the given score"""
    # Determine color based on score
    if score >= 0.8:
        color = "green"
        label = "High Trust"
    elif score >= 0.6:
        color = "orange"
        label = "Medium Trust"
    else:
        color = "red"
        label = "Low Trust"
    
    # Create the indicator
    st.markdown(f"""
    <div style="display: inline-block; padding: 0.3em 0.6em; border-radius: 0.25em; 
                background-color: {color}; color: white; font-weight: bold;">
        {label} ({score:.2f})
    </div>
    """, unsafe_allow_html=True)
    
    # Display flags if provided
    if flags:
        with st.expander("View RAI Details"):
            st.markdown("### Responsible AI Analysis")
            
            # Bias indicator
            bias_level = flags.get("bias", {}).get("level", "low")
            bias_score = flags.get("bias", {}).get("score", 0)
            
            st.markdown(f"**Bias Detection:** {bias_level.title()} ({bias_score:.2f})")
            if bias_level == "high":
                st.warning("The document may contain language that shows strong preferences or prejudices.")
            elif bias_level == "medium":
                st.info("Some language in the document may show subtle preferences.")
            else:
                st.success("The document appears to use neutral language.")
            
            # Hallucination indicator
            hallucination = flags.get("hallucination", "low")
            st.markdown(f"**Hallucination Risk:** {hallucination.title()}")
            if hallucination == "high":
                st.warning("The document may contain unverifiable claims or assertions.")
            elif hallucination == "medium":
                st.info("Some claims in the document may benefit from verification.")
            else:
                st.success("The document appears to contain verifiable information.")
            
            # Security indicator
            security = flags.get("security", "low")
            st.markdown(f"**Security Risk:** {security.title()}")
            if security == "high":
                st.warning("The document may contain sensitive information that requires protection.")
            elif security == "medium":
                st.info("The document contains some information that should be handled with care.")
            else:
                st.success("The document appears to contain minimal sensitive information.")
