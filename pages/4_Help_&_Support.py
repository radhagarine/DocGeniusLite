import streamlit as st
from auth import check_authentication
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.sidebar import create_sidebar

# Page configuration
st.set_page_config(
    page_title="Help & Support - DocGenius Lite",
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

# Help and Support page
st.title("Help & Support")

# FAQ section
st.markdown("## Frequently Asked Questions")

# FAQ questions with expandable answers
with st.expander("What is DocGenius Lite?"):
    st.markdown("""
    DocGenius Lite is a document generation platform designed for small businesses, 
    solopreneurs, and freelancers who need legally sound and professional-looking
    documents without technical knowledge or legal teams.
    
    It allows you to quickly generate common business documents like NDAs, invoices,
    proposals, and more through a simple, intuitive interface.
    """)

with st.expander("How many free documents can I create?"):
    st.markdown("""
    With the free plan, you can create up to 3 documents per month. 
    
    If you need more documents, you can either:
    - Purchase individual documents for $3 each
    - Upgrade to the Pro plan for $9/month with unlimited documents
    """)

with st.expander("What document types are available?"):
    st.markdown("""
    DocGenius Lite currently supports the following document types:
    
    1. Non-Disclosure Agreement (NDA)
    2. Invoice
    3. Letter of Intent
    4. Business Proposal
    5. Scope of Work
    
    More document types will be available in future updates.
    """)

with st.expander("What is the Responsible AI (RAI) indicator?"):
    st.markdown("""
    The Responsible AI (RAI) indicator provides transparency about the quality and trustworthiness
    of the generated document. It measures:
    
    - **Bias**: Does the document use fair and balanced language?
    - **Hallucination**: Does the document contain claims that can't be verified?
    - **Security**: How sensitive is the information in the document?
    
    These metrics help you make informed decisions about the document's content and use.
    """)

with st.expander("How do I export my documents?"):
    st.markdown("""
    After creating a document, you'll have the option to export it in two formats:
    
    1. **PDF**: A widely compatible format for sharing and printing
    2. **DOCX**: Microsoft Word format for further editing if needed
    
    Simply click the respective button in the document preview page to download your document.
    """)

with st.expander("How long are my documents stored?"):
    st.markdown("""
    - **Free plan**: Documents are stored for 30 days
    - **Pro plan**: Unlimited document history retention
    
    You can view your documents in the "Document History" page, where you can preview,
    download, or regenerate them as needed.
    """)

# Contact Support section
st.markdown("## Contact Support")

with st.form("support_form"):
    st.markdown("If you need help with anything not covered in the FAQ, please fill out this form:")
    
    support_topic = st.selectbox(
        "What do you need help with?",
        [
            "Select a topic...",
            "Account issues",
            "Billing/payment",
            "Document generation problems",
            "Feature request",
            "Bug report",
            "Other"
        ]
    )
    
    support_message = st.text_area("Describe your issue or question in detail:")
    
    submit_button = st.form_submit_button("Submit Support Request")

if submit_button:
    if support_topic == "Select a topic...":
        st.error("Please select a topic for your support request.")
    elif not support_message:
        st.error("Please describe your issue or question.")
    else:
        # In a real app, this would send the support request to a ticketing system
        st.success("Your support request has been submitted! We'll respond within 48 hours.")

# Feedback section
st.markdown("## Product Feedback")
st.markdown("We're constantly improving DocGenius Lite. Help us make it better by sharing your thoughts!")

feedback_type = st.radio(
    "What kind of feedback do you have?",
    ["Feature request", "Improvement suggestion", "General feedback"]
)

feedback_text = st.text_area("Your feedback:")

if st.button("Submit Feedback"):
    if feedback_text:
        # In a real app, this would store the feedback in a database
        st.success("Thank you for your feedback! It helps us improve DocGenius Lite.")
    else:
        st.error("Please enter your feedback before submitting.")

# Help resources
st.markdown("## Additional Resources")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Video Tutorials")
    st.markdown("- [Getting Started with DocGenius Lite](#)")
    st.markdown("- [Creating Your First Document](#)")
    st.markdown("- [Understanding Document Templates](#)")
    st.markdown("- [Responsible AI Features Explained](#)")

with col2:
    st.markdown("### Helpful Articles")
    st.markdown("- [Best Practices for Document Creation](#)")
    st.markdown("- [Legal Considerations for Small Businesses](#)")
    st.markdown("- [Understanding RAI Metrics](#)")
    st.markdown("- [Customizing Your Documents](#)")
