import streamlit as st
from auth import check_authentication, logout

# Page configuration
st.set_page_config(
    page_title="Account - DocGenius Lite",
    page_icon="📄",
    layout="wide"
)

# Check authentication
if not check_authentication():
    st.warning("Please log in to access this page")
    st.stop()

# Account management page
st.title("Your Account")

# Display user information
user_email = st.session_state.get('email', 'Not available')
subscription = st.session_state.get('subscription', 'free')

# Account details card
st.markdown("### Account Details")
st.markdown(f"**Email:** {user_email}")
st.markdown(f"**Subscription:** {subscription.upper()}")

# Plan information
st.markdown("---")
st.markdown("### Your Plan")

# Display different information based on current plan
if subscription == 'pro':
    st.success("You are currently on the Pro plan!")
    st.markdown("**Benefits of your Pro plan:**")
    st.markdown("- Unlimited document generation")
    st.markdown("- Unlimited document history retention")
    st.markdown("- Advanced RAI metrics and insights")
    
    # Cancellation option
    if st.button("Cancel Pro Subscription", key="cancel_sub"):
        # This would integrate with the payment processor to cancel subscription
        st.warning("This would cancel your subscription at the end of your billing period.")
        st.info("For demo purposes, this functionality is not implemented.")
else:
    st.info("You are currently on the Free plan.")
    
    # Show document usage
    free_docs_used = st.session_state.get('free_docs_used', 0)
    free_docs_limit = 3
    
    st.markdown(f"**Free documents this month:** {free_docs_used}/{free_docs_limit}")
    st.progress(free_docs_used/free_docs_limit)
    
    # Pro plan upgrade
    st.markdown("### Upgrade to Pro")
    st.markdown("**Pro plan benefits:**")
    st.markdown("- Unlimited document generation")
    st.markdown("- Unlimited document history retention")
    st.markdown("- Advanced RAI metrics and insights")
    st.markdown("- Priority email support")
    
    # Payment form
    with st.expander("Upgrade to Pro - $9/month"):
        # Simulated payment form
        st.markdown("### Payment Information")
        with st.form("upgrade_form"):
            st.text_input("Card Number", placeholder="4242 4242 4242 4242")
            col1, col2 = st.columns(2)
            with col1:
                st.text_input("Expiration Date", placeholder="MM/YY")
            with col2:
                st.text_input("CVC", placeholder="123")
            
            st.text_input("Name on Card", placeholder="John Smith")
            agree = st.checkbox("I agree to the terms of service")
            
            submit_payment = st.form_submit_button("Subscribe - $9/month")
        
        if submit_payment:
            if agree:
                # In a real app, this would process the subscription through Stripe
                st.success("🎉 Subscription successful! You now have Pro access.")
                
                # Update session state
                st.session_state['subscription'] = 'pro'
                
                # Offer reload
                if st.button("Reload page"):
                    st.rerun()
            else:
                st.error("Please agree to the terms of service")

# Preferences
st.markdown("---")
st.markdown("### Preferences")

# Theme preference
theme_pref = st.radio(
    "Application Theme",
    ["Light", "Dark", "System Default"],
    index=2
)

# Default document type
from utils import get_document_display_name
doc_types = ["nda", "invoice", "letter_of_intent", "proposal", "scope_of_work"]
default_doc = st.selectbox(
    "Default Document Type",
    options=doc_types,
    format_func=get_document_display_name
)

if st.button("Save Preferences"):
    st.success("Preferences saved!")

# Account actions
st.markdown("---")
st.markdown("### Account Actions")

col1, col2 = st.columns(2)
with col1:
    if st.button("Log Out", key="logout_btn"):
        logout()
        st.success("You have been logged out.")
        st.rerun()

with col2:
    if st.button("Delete Account", key="delete_account"):
        st.warning("⚠️ This action cannot be undone. All your data will be permanently deleted.")
        
        confirm = st.text_input("Type 'DELETE' to confirm")
        if confirm == "DELETE":
            # This would delete the user account in a real implementation
            st.error("Account deletion functionality would be implemented here.")
            st.info("For demo purposes, this functionality is not active.")
