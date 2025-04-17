
import streamlit as st
import sys
import os
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auth import check_authentication
from db import get_db_connection

# Page configuration
st.set_page_config(
    page_title="Complete Your Profile - DocGenius Lite",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Set current page for sidebar highlighting
st.session_state['current_page'] = __file__

# Hide the sidebar for onboarding page
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }
    section[data-testid="stSidebarUserContent"] {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

# Check authentication
if not check_authentication():
    st.warning("Please log in to access this page")
    st.stop()

# Remove modal overlay and instead use dedicated onboarding pages with step navigation

if 'show_onboarding_modal' not in st.session_state:
    st.session_state.show_onboarding_modal = True

def render_onboarding_modal():
    # Use brand colors for modal styling
    primary_color = "#3FD7A5"  # Default primary brand color
    secondary_color = "#26856C"  # Default secondary brand color

    # Override with saved brand colors if available
    if 'industry_profile' in st.session_state:
        brand_colors = st.session_state.industry_profile.get('brand_colors', {})
        primary_color = brand_colors.get('primary', primary_color)
        secondary_color = brand_colors.get('secondary', secondary_color)

    # Inject CSS for dark mode modal with blur overlay using brand colors
    st.markdown(
        f"""
        <style>
        .modal-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: rgba(10, 40, 23, 0.85);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            z-index: 1000;
        }}
        .modal-container {{
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(22, 68, 48, 0.95);
            border-radius: 16px;
            padding: 2rem;
            width: 90%;
            max-width: 600px;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.7);
            color: white;
            z-index: 1100;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        .modal-close-button {{
            position: absolute;
            top: 12px;
            right: 12px;
            background: transparent;
            border: none;
            font-size: 2.5rem;
            color: {primary_color};
            cursor: pointer;
            transition: color 0.3s ease;
        }}
        .modal-close-button:hover {{
            color: {secondary_color};
        }}
        .modal-header {{
            font-size: 1.8rem;
            margin-bottom: 0.5rem;
            font-weight: 700;
        }}
        .modal-subheader {{
            font-size: 1.2rem;
            margin-bottom: 1.5rem;
            color: #ccc;
        }}
        .modal-button {{
            background-color: {primary_color};
            color: white;
            border: none;
            padding: 0.6rem 1.2rem;
            border-radius: 8px;
            font-size: 1rem;
            cursor: pointer;
            transition: background-color 0.3s ease;
            margin-top: 1rem;
        }}
        .modal-button:hover {{
            background-color: {secondary_color};
        }}
        </style>
        <div class="modal-overlay"></div>
        <div class="modal-container" role="dialog" aria-modal="true" aria-labelledby="modal-title">
            <button class="modal-close-button" aria-label="Close onboarding modal" onclick="window.location.href='/pages/0_Dashboard.py'">&times;</button>
    """,
        unsafe_allow_html=True,
    )

    # Render onboarding steps inside modal container using Streamlit components
    progress = (st.session_state.onboarding_step - 1) / 3
    st.progress(progress)

    if st.session_state.onboarding_step == 1:
        st.markdown('<h2 class="modal-header">Tell us about your business</h2>', unsafe_allow_html=True)
        st.markdown('<p class="modal-subheader">Let\'s personalize your document generation experience</p>', unsafe_allow_html=True)

        industry = st.selectbox(
            "What industry are you in?",
            [
                "Technology & Software",
                "Professional Services",
                "Healthcare",
                "Finance & Banking",
                "Real Estate",
                "Manufacturing",
                "Retail & E-commerce",
                "Education",
                "Construction",
                "Other",
            ],
            help="Select the industry that best describes your business",
        )

        company_size = st.select_slider(
            "Company Size",
            options=["1-10", "11-50", "51-200", "201-500", "501+"],
            help="Number of employees in your organization",
        )

        business_type = st.selectbox(
            "Business Type",
            [
                "B2B (Business to Business)",
                "B2C (Business to Consumer)",
                "Both B2B and B2C",
                "Non-profit",
                "Government/Public Sector",
            ],
            help="Select your primary business model",
        )

        if st.button("Continue →", key="step1_continue"):
            st.session_state.industry_profile.update(
                {
                    "industry": industry,
                    "company_size": company_size,
                    "business_type": business_type,
                }
            )
            st.session_state.onboarding_step = 2
            st.experimental_rerun()

    elif st.session_state.onboarding_step == 2:
        st.markdown('<h2 class="modal-header">Tell us more</h2>', unsafe_allow_html=True)
        st.markdown('<p class="modal-subheader">This helps us tailor document content to your needs</p>', unsafe_allow_html=True)

        target_market = st.text_area(
            "Who is your target market?", help="Describe your ideal customers or clients"
        )

        company_description = st.text_area(
            "Company Description", help="A brief description of what your company does"
        )

        document_preferences = st.multiselect(
            "What types of documents do you create most often?",
            [
                "Business Proposals",
                "Contracts & Agreements",
                "Marketing Materials",
                "Technical Documentation",
                "Financial Reports",
                "HR Documents",
                "Legal Documents",
            ],
            help="Select all that apply",
        )

        back_col, continue_col = st.columns(2)
        with back_col:
            if st.button("← Back", key="step2_back"):
                st.session_state.onboarding_step = 1
                st.experimental_rerun()
        with continue_col:
            if st.button("Continue →", key="step2_continue"):
                st.session_state.industry_profile.update(
                    {
                        "target_market": target_market,
                        "company_description": company_description,
                        "document_preferences": document_preferences,
                    }
                )
                st.session_state.onboarding_step = 3
                st.experimental_rerun()

    elif st.session_state.onboarding_step == 3:
        st.markdown('<h2 class="modal-header">Brand & Style Preferences</h2>', unsafe_allow_html=True)
        st.markdown('<p class="modal-subheader">Help us match your brand identity</p>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            primary_color = st.color_picker(
                "Primary Brand Color", primary_color, help="Choose your main brand color"
            )

        with col2:
            secondary_color = st.color_picker(
                "Secondary Brand Color", secondary_color, help="Choose a complementary brand color"
            )

        tone_options = [
            "Professional and formal",
            "Friendly and approachable",
            "Technical and detailed",
            "Creative and innovative",
            "Direct and concise",
        ]

        document_tone = st.select_slider(
            "Preferred Document Tone",
            options=tone_options,
            value="Professional and formal",
            help="Choose the writing style for your documents",
        )

        back_col, complete_col = st.columns(2)
        with back_col:
            if st.button("← Back", key="step3_back"):
                st.session_state.onboarding_step = 2
                st.experimental_rerun()
        with complete_col:
            if st.button("Complete Setup →", key="step3_complete"):
                st.session_state.industry_profile.update(
                    {
                        "brand_colors": {
                            "primary": primary_color,
                            "secondary": secondary_color,
                        },
                        "document_tone": document_tone,
                    }
                )

                if save_industry_profile():
                    st.success("🎉 Profile setup complete!")
                    st.markdown(
                        """
                        <meta http-equiv="refresh" content="2; url=/pages/0_Dashboard.py">
                        """,
                        unsafe_allow_html=True,
                    )
                    st.stop()

    st.markdown("</div>", unsafe_allow_html=True)

# Render modal if visible
if st.session_state.show_onboarding_modal:
    render_onboarding_modal()
else:
    st.write("Onboarding completed or closed.")
