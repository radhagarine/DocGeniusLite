import streamlit as st
import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auth import check_authentication
from db import get_user_documents
from utils import get_document_display_name, display_rai_indicator, format_date
from utils.sidebar import create_sidebar

# Page configuration
st.set_page_config(
    page_title="Document History - DocGenius Lite",
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

# Document history page
st.title("Document History")

# Get user's documents
user_id = st.session_state.get('user_id')
documents = get_user_documents(user_id)

# Display document history
if not documents:
    st.info("You haven't created any documents yet. Create your first document from the Generate Document page.")
else:
    # Display documents in a table
    retention_days = 30
    st.markdown(f"Your documents from the past {retention_days} days:")
    
    # Create a data table
    data = []
    for doc in documents:
        doc_id, doc_type, title, created_at, rai_score = doc
        data.append({
            "ID": doc_id,
            "Document Type": get_document_display_name(doc_type),
            "Title": title,
            "Created": format_date(created_at),
            "Trust Score": f"{rai_score:.2f}"
        })
    
    # Free plan retention notice
    if st.session_state.get('subscription') != 'pro':
        st.info(f"Free plan: Documents are retained for {retention_days} days. Upgrade to Pro for unlimited retention.")
    
    # Filter options
    doc_types = list(set([d["Document Type"] for d in data]))
    doc_types.insert(0, "All")
    
    filter_type = st.selectbox("Filter by document type:", doc_types)
    
    # Apply filter
    if filter_type != "All":
        filtered_data = [d for d in data if d["Document Type"] == filter_type]
    else:
        filtered_data = data
    
    # Display data
    if filtered_data:
        # Use different display methods based on number of documents
        if len(filtered_data) > 5:
            # Use a table for many documents
            st.dataframe(
                filtered_data,
                use_container_width=True,
                column_config={
                    "ID": st.column_config.TextColumn("ID", width="small"),
                    "Document Type": st.column_config.TextColumn("Document Type", width="medium"),
                    "Title": st.column_config.TextColumn("Title", width="large"),
                    "Created": st.column_config.TextColumn("Created", width="medium"),
                    "Trust Score": st.column_config.ProgressColumn(
                        "Trust Score",
                        width="medium",
                        format="%f",
                        min_value=0,
                        max_value=1,
                    ),
                },
                hide_index=True,
            )
        else:
            # Use expandable cards for fewer documents
            for doc in filtered_data:
                with st.expander(f"{doc['Title']} ({doc['Document Type']})"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**Created:** {doc['Created']}")
                        st.markdown(f"**Document Type:** {doc['Document Type']}")
                    
                    with col2:
                        st.markdown("**Trust Score:**")
                        score = float(doc['Trust Score'])
                        display_rai_indicator(score)
                    
                    # Action buttons
                    btn1, btn2, btn3 = st.columns(3)
                    with btn1:
                        if st.button("View", key=f"view_{doc['ID']}"):
                            # This would navigate to document view
                            st.info("Document view would open here")
                    with btn2:
                        if st.button("Download PDF", key=f"pdf_{doc['ID']}"):
                            st.info("PDF download would start here")
                    with btn3:
                        if st.button("Download DOCX", key=f"docx_{doc['ID']}"):
                            st.info("DOCX download would start here")
    else:
        st.info(f"No {filter_type} documents found.")
    
    # Pagination (for future implementation when there are many documents)
    if len(data) > 10:
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 3, 1])
        with col1:
            st.button("← Previous")
        with col2:
            st.write("Page 1 of 1")
        with col3:
            st.button("Next →")
