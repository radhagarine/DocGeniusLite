import streamlit as st
import sys
import os
from time import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auth import check_authentication
from utils.styles import apply_custom_css, render_clickable_logo
from utils.sidebar import create_sidebar

st.set_page_config(
    page_title="DocGenius | AI-Powered Document Management",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

def render_hero_section():
    """Render the hero section of the landing page using Streamlit components"""
    # Create a two-column layout for the hero section
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("<h1 style='font-size: 3.5rem; font-weight: 800; line-height: 1.2;'>Streamline your documents with <span style='background: linear-gradient(135deg, #3fd7a5 0%, #26856c 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>DocGenius</span></h1>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 1.25rem; color: rgba(244, 249, 247, 0.7); margin-bottom: 2rem;'>Create professional business documents efficiently with our intuitive platform. Secure, organized, and designed for your business needs.</p>", unsafe_allow_html=True)
        
        if st.button("Get Started", type="primary", key="hero_signup"):
            st.session_state.auth_mode = 'register'
            st.switch_page("pages/login.py")
    
    with col2:
        # Create a simple visual representation using emojis
        st.markdown("""
        <div style='display: flex; justify-content: center; align-items: center; height: 300px; position: relative;'>
            <div style='position: absolute; font-size: 5rem; z-index: 3; animation: float 6s ease-in-out infinite;'>📄</div>
            <div style='position: absolute; font-size: 4rem; z-index: 2; animation: float 6s ease-in-out infinite 1s; transform: translateX(-60px) translateY(-40px);'>📝</div>
            <div style='position: absolute; font-size: 4rem; z-index: 1; animation: float 6s ease-in-out infinite 2s; transform: translateX(60px) translateY(40px);'>📋</div>
        </div>
        <style>
        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-20px); }
            100% { transform: translateY(0px); }
        }
        </style>
        """, unsafe_allow_html=True)

def render_features_section():
    """Render the features section with cards using Streamlit components"""
    st.markdown("<h2 class='section-title' id='features'>Features</h2>", unsafe_allow_html=True)
    st.markdown("<p class='section-subtitle'>Create a wide range of professional documents for your business needs</p>", unsafe_allow_html=True)
    
    # Add some spacing for better section separation
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    # Use container width to constrain the content for better alignment
    with st.container():
        # First row of document types with spacing columns
        col_space1, col1, col2, col3, col_space2 = st.columns([0.5, 3, 3, 3, 0.5])
        
        with col1:
            st.markdown("""
            <div style="background: rgba(22, 68, 48, 0.3); border-radius: 12px; padding: 1.5rem; border: 1px solid rgba(63, 215, 165, 0.2); height: 100%;">
                <div style="font-size: 2.5rem; margin-bottom: 1rem; text-align: center;">📝</div>
                <h3 style="color: #f4f9f7; font-size: 1.25rem; margin-bottom: 0.75rem; text-align: center;">Business Proposals</h3>
                <p style="color: rgba(244, 249, 247, 0.7); text-align: center;">Create compelling business proposals that win clients and close deals effectively.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: rgba(22, 68, 48, 0.3); border-radius: 12px; padding: 1.5rem; border: 1px solid rgba(63, 215, 165, 0.2); height: 100%;">
                <div style="font-size: 2.5rem; margin-bottom: 1rem; text-align: center;">📄</div>
                <h3 style="color: #f4f9f7; font-size: 1.25rem; margin-bottom: 0.75rem; text-align: center;">Contracts & Agreements</h3>
                <p style="color: rgba(244, 249, 247, 0.7); text-align: center;">Generate legally-sound contracts and agreements tailored to your business requirements, including invoices, scopes of work, and letters of intent.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background: rgba(22, 68, 48, 0.3); border-radius: 12px; padding: 1.5rem; border: 1px solid rgba(63, 215, 165, 0.2); height: 100%;">
                <div style="font-size: 2.5rem; margin-bottom: 1rem; text-align: center;">📊</div>
                <h3 style="color: #f4f9f7; font-size: 1.25rem; margin-bottom: 0.75rem; text-align: center;">Financial Reports</h3>
                <p style="color: rgba(244, 249, 247, 0.7); text-align: center;">Create professional financial statements, budgets, and forecasts with customizable templates.</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Add some spacing between rows
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        
        # Second row of document types with same spacing
        col_space3, col4, col5, col6, col_space4 = st.columns([0.5, 3, 3, 3, 0.5])
        
        with col4:
            st.markdown("""
            <div style="background: rgba(22, 68, 48, 0.3); border-radius: 12px; padding: 1.5rem; border: 1px solid rgba(63, 215, 165, 0.2); height: 100%;">
                <div style="font-size: 2.5rem; margin-bottom: 1rem; text-align: center;">👥</div>
                <h3 style="color: #f4f9f7; font-size: 1.25rem; margin-bottom: 0.75rem; text-align: center;">HR Documents</h3>
                <p style="color: rgba(244, 249, 247, 0.7); text-align: center;">Generate employee handbooks, policies, offer letters, and other essential HR documentation.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col5:
            st.markdown("""
            <div style="background: rgba(22, 68, 48, 0.3); border-radius: 12px; padding: 1.5rem; border: 1px solid rgba(63, 215, 165, 0.2); height: 100%;">
                <div style="font-size: 2.5rem; margin-bottom: 1rem; text-align: center;">📣</div>
                <h3 style="color: #f4f9f7; font-size: 1.25rem; margin-bottom: 0.75rem; text-align: center;">Marketing Materials</h3>
                <p style="color: rgba(244, 249, 247, 0.7); text-align: center;">Create professional brochures, business proposals, NDAs, invoices, scope of work documents, letters of intent, and other marketing collateral.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col6:
            st.markdown("""
            <div style="background: rgba(22, 68, 48, 0.3); border-radius: 12px; padding: 1.5rem; border: 1px solid rgba(63, 215, 165, 0.2); height: 100%;">
                <div style="font-size: 2.5rem; margin-bottom: 1rem; text-align: center;">⚖️</div>
                <h3 style="color: #f4f9f7; font-size: 1.25rem; margin-bottom: 0.75rem; text-align: center;">Legal Documents</h3>
                <p style="color: rgba(244, 249, 247, 0.7); text-align: center;">Generate NDAs, terms of service, privacy policies, and other essential legal documents.</p>
            </div>
            """, unsafe_allow_html=True)

def render_how_it_works():
    """Render the how it works section using Streamlit components"""
    st.markdown("<h2 class='section-title' id='how-it-works'>How DocGenius Works</h2>", unsafe_allow_html=True)
    st.markdown("<p class='section-subtitle'>Our streamlined process makes document creation and management effortless</p>", unsafe_allow_html=True)
    
    # Add some spacing for better section separation
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    # Create three columns for the steps with spacing columns for better alignment
    col_space1, col1, col2, col3, col_space2 = st.columns([0.5, 3, 3, 3, 0.5])
    
    with col1:
        st.markdown("""
        <div style="background: rgba(22, 68, 48, 0.3); border-radius: 12px; padding: 1.5rem; border: 1px solid rgba(63, 215, 165, 0.2); height: 100%; position: relative;">
            <div style="position: absolute; top: -15px; left: -15px; width: 40px; height: 40px; background: linear-gradient(135deg, #3fd7a5 0%, #26856c 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; color: #0a2817;">01</div>
            <h3 style="color: #f4f9f7; font-size: 1.25rem; margin: 1rem 0; text-align: center;">Select a template</h3>
            <p style="color: rgba(244, 249, 247, 0.7); text-align: center;">Choose from our library of professionally designed document templates.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: rgba(22, 68, 48, 0.3); border-radius: 12px; padding: 1.5rem; border: 1px solid rgba(63, 215, 165, 0.2); height: 100%; position: relative;">
            <div style="position: absolute; top: -15px; left: -15px; width: 40px; height: 40px; background: linear-gradient(135deg, #3fd7a5 0%, #26856c 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; color: #0a2817;">02</div>
            <h3 style="color: #f4f9f7; font-size: 1.25rem; margin: 1rem 0; text-align: center;">Customize content</h3>
            <p style="color: rgba(244, 249, 247, 0.7); text-align: center;">Add your business details and personalize the document to match your specific needs.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: rgba(22, 68, 48, 0.3); border-radius: 12px; padding: 1.5rem; border: 1px solid rgba(63, 215, 165, 0.2); height: 100%; position: relative;">
            <div style="position: absolute; top: -15px; left: -15px; width: 40px; height: 40px; background: linear-gradient(135deg, #3fd7a5 0%, #26856c 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; color: #0a2817;">03</div>
            <h3 style="color: #f4f9f7; font-size: 1.25rem; margin: 1rem 0; text-align: center;">Generate & share</h3>
            <p style="color: rgba(244, 249, 247, 0.7); text-align: center;">Create your finalized document and securely share it with stakeholders.</p>
        </div>
        """, unsafe_allow_html=True)
        
    # Add spacing after the section
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

def render_pricing_section():
    """Render the pricing section using Streamlit components"""
    st.markdown("<h2 class='section-title' id='pricing'>Simple, Transparent Pricing</h2>", unsafe_allow_html=True)
    st.markdown("<p class='section-subtitle'>Choose the plan that works best for your needs</p>", unsafe_allow_html=True)
    
    # Create two columns for pricing cards with empty columns for better spacing
    col_space1, col1, col2, col_space2 = st.columns([1, 2, 2, 1])
    
    with col1:
        st.markdown("""
        <div style="background: rgba(22, 68, 48, 0.3); border-radius: 12px; padding: 1.5rem; border: 1px solid rgba(63, 215, 165, 0.2); height: 100%;">
            <div style="text-align: center; margin-bottom: 1.5rem;">
                <h3 style="color: #f4f9f7; font-size: 1.5rem; margin-bottom: 0.5rem;">Free</h3>
                <div style="font-size: 2rem; font-weight: 700; color: #f4f9f7;">$0<span style="font-size: 1rem; font-weight: 400; color: rgba(244, 249, 247, 0.7);">/month</span></div>
            </div>
            <ul style="list-style: none; padding: 0; margin: 0 0 1.5rem 0;">
                <li style="padding: 0.5rem 0; color: #f4f9f7;">✅ 3 documents per month</li>
                <li style="padding: 0.5rem 0; color: #f4f9f7;">✅ Basic templates</li>
                <li style="padding: 0.5rem 0; color: #f4f9f7;">✅ 7-day document storage</li>
                <li style="padding: 0.5rem 0; color: rgba(244, 249, 247, 0.5);">❌ Advanced customization</li>
                <li style="padding: 0.5rem 0; color: rgba(244, 249, 247, 0.5);">❌ Priority support</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Get Started", key="free_plan", use_container_width=True):
            st.session_state.auth_mode = 'register'
            st.switch_page("pages/login.py")
    
    with col2:
        st.markdown("""
        <div style="background: rgba(22, 68, 48, 0.3); border-radius: 12px; padding: 1.5rem; border: 1px solid rgba(63, 215, 165, 0.5); height: 100%; position: relative; box-shadow: 0 0 20px rgba(63, 215, 165, 0.2);">
            <div style="position: absolute; top: -10px; right: -10px; background: #3fd7a5; color: #0a2817; font-size: 0.75rem; font-weight: 700; padding: 0.25rem 0.75rem; border-radius: 20px;">POPULAR</div>
            <div style="text-align: center; margin-bottom: 1.5rem;">
                <h3 style="color: #f4f9f7; font-size: 1.5rem; margin-bottom: 0.5rem;">Pro</h3>
                <div style="font-size: 2rem; font-weight: 700; color: #f4f9f7;">$19<span style="font-size: 1rem; font-weight: 400; color: rgba(244, 249, 247, 0.7);">/month</span></div>
            </div>
            <ul style="list-style: none; padding: 0; margin: 0 0 1.5rem 0;">
                <li style="padding: 0.5rem 0; color: #f4f9f7;">✅ Unlimited documents</li>
                <li style="padding: 0.5rem 0; color: #f4f9f7;">✅ All templates</li>
                <li style="padding: 0.5rem 0; color: #f4f9f7;">✅ 1-year document storage</li>
                <li style="padding: 0.5rem 0; color: #f4f9f7;">✅ Advanced customization</li>
                <li style="padding: 0.5rem 0; color: #f4f9f7;">✅ Priority support</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Upgrade Now", type="primary", key="pro_plan", use_container_width=True):
            st.session_state.auth_mode = 'register'
            st.switch_page("pages/login.py")

def render_testimonials():
    """Render customer testimonials using Streamlit components"""
    st.markdown("<h2 class='section-title' id='testimonials'>What Our Customers Say</h2>", unsafe_allow_html=True)
    st.markdown("<p class='section-subtitle'>Trusted by businesses worldwide</p>", unsafe_allow_html=True)
    
    # Add some spacing for better section separation
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    # Create three columns for testimonials with spacing columns for better alignment
    col_space1, col1, col2, col3, col_space2 = st.columns([0.5, 3, 3, 3, 0.5])
    
    with col1:
        st.markdown("""
        <div style="background: rgba(22, 68, 48, 0.3); border-radius: 12px; padding: 1.5rem; border: 1px solid rgba(63, 215, 165, 0.2); height: 100%;">
            <div style="color: #3fd7a5; font-size: 1.5rem; margin-bottom: 1rem;">❝</div>
            <p style="color: #f4f9f7; font-style: italic; margin-bottom: 1.5rem;">
                "DocGenius has transformed how we handle our legal documents. The AI-powered validation has saved us from countless potential issues."
            </p>
            <div style="display: flex; align-items: center;">
                <div style="width: 40px; height: 40px; border-radius: 50%; background: #3fd7a5; color: #0a2817; display: flex; align-items: center; justify-content: center; font-weight: bold; margin-right: 12px;">S</div>
                <div>
                    <div style="color: #f4f9f7; font-weight: 600;">Sarah Johnson</div>
                    <div style="color: rgba(244, 249, 247, 0.7); font-size: 0.875rem;">Legal Director, TechCorp</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: rgba(22, 68, 48, 0.3); border-radius: 12px; padding: 1.5rem; border: 1px solid rgba(63, 215, 165, 0.2); height: 100%;">
            <div style="color: #3fd7a5; font-size: 1.5rem; margin-bottom: 1rem;">❝</div>
            <p style="color: #f4f9f7; font-style: italic; margin-bottom: 1.5rem;">
                "The document generation is lightning fast and the templates are professional. We've cut our document creation time by 75%."
            </p>
            <div style="display: flex; align-items: center;">
                <div style="width: 40px; height: 40px; border-radius: 50%; background: #3fd7a5; color: #0a2817; display: flex; align-items: center; justify-content: center; font-weight: bold; margin-right: 12px;">M</div>
                <div>
                    <div style="color: #f4f9f7; font-weight: 600;">Michael Chen</div>
                    <div style="color: rgba(244, 249, 247, 0.7); font-size: 0.875rem;">Operations Manager, Startify</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: rgba(22, 68, 48, 0.3); border-radius: 12px; padding: 1.5rem; border: 1px solid rgba(63, 215, 165, 0.2); height: 100%;">
            <div style="color: #3fd7a5; font-size: 1.5rem; margin-bottom: 1rem;">❝</div>
            <p style="color: #f4f9f7; font-style: italic; margin-bottom: 1.5rem;">
                "As a small business owner, DocGenius gives me the confidence that my documents are legally sound without the expense of a legal team."
            </p>
            <div style="display: flex; align-items: center;">
                <div style="width: 40px; height: 40px; border-radius: 50%; background: #3fd7a5; color: #0a2817; display: flex; align-items: center; justify-content: center; font-weight: bold; margin-right: 12px;">E</div>
                <div>
                    <div style="color: #f4f9f7; font-weight: 600;">Emma Rodriguez</div>
                    <div style="color: rgba(244, 249, 247, 0.7); font-size: 0.875rem;">Founder, GreenStart</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    # Add spacing after the section
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

def render_faq_section():
    """Render frequently asked questions section using Streamlit expanders"""
    st.markdown("<h2 class='section-title' id='faq'>Frequently Asked Questions</h2>", unsafe_allow_html=True)
    st.markdown("<p class='section-subtitle'>Find answers to common questions about DocGenius</p>", unsafe_allow_html=True)
    
    # Add some spacing for better section separation
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    # Create a container with spacing for better alignment
    col_space1, col_main, col_space2 = st.columns([1, 10, 1])
    
    with col_main:
        with st.expander("How secure is DocGenius?"):
            st.write("DocGenius uses enterprise-grade encryption for all documents and data. We implement end-to-end encryption, secure authentication, and regular security audits to ensure your information remains protected.")
        
        with st.expander("Can I customize document templates?"):
            st.write("Yes! All plans allow some level of customization. Free users can make basic edits, while Pro users get access to advanced customization options, including custom branding, formatting, and content blocks.")
        
        with st.expander("How does the AI validation work?"):
            st.write("Our AI analyzes your documents for legal compliance, consistency, and potential issues. It checks against current regulations, identifies missing information, and suggests improvements to ensure your documents are accurate and professional.")
        
        with st.expander("Can I cancel my subscription anytime?"):
            st.write("Absolutely. There are no long-term contracts, and you can cancel your subscription at any time. If you cancel, you'll continue to have access until the end of your billing period.")
        
        with st.expander("Do you offer discounts for non-profits or educational institutions?"):
            st.write("Yes, we offer special pricing for non-profits, educational institutions, and startups. Contact our sales team to learn more about our discount programs.")
    
    # Add spacing after the section
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

def render_cta_section():
    """Render call to action section using Streamlit components"""
    # Create a container with spacing for better alignment
    col_space1, col_main, col_space2 = st.columns([1, 10, 1])
    
    with col_main:
        # Create a container with a background
        st.markdown("""
        <div style="background: rgba(22, 68, 48, 0.5); border-radius: 16px; padding: 3rem 2rem; border: 1px solid rgba(63, 215, 165, 0.3); margin: 1rem 0; text-align: center;">
            <h2 style="color: #f4f9f7; font-size: 2rem; margin-bottom: 1rem;">Ready to streamline your document creation?</h2>
            <p style="color: rgba(244, 249, 247, 0.7); font-size: 1.1rem; margin-bottom: 2rem;">Create professional documents with our secure, user-friendly platform.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Get Started for Free", type="primary", use_container_width=True):
                st.session_state.auth_mode = 'register'
                st.switch_page("pages/login.py")
        with col2:
            st.button("Schedule a Demo", type="secondary", use_container_width=True)
    
    # Add spacing after the section
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

def render_navbar():
    """Render a navigation bar at the top of the landing page using Streamlit components"""
    # Create a container for the navbar
    with st.container():
        cols = st.columns([2, 4, 2])
        
        # Logo
        with cols[0]:
            st.markdown("<h2 style='margin-bottom: 0;'><span style='background: linear-gradient(135deg, #3fd7a5 0%, #26856c 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>D</span>oc<span style='background: linear-gradient(135deg, #3fd7a5 0%, #26856c 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>G</span>enius</h2>", unsafe_allow_html=True)
        
        # Navigation links
        with cols[1]:
            nav_cols = st.columns(5)
            with nav_cols[0]:
                st.markdown("<div style='text-align: center;'><a href='#features' style='color: #f4f9f7; text-decoration: none; font-weight: 500;'>Features</a></div>", unsafe_allow_html=True)
            with nav_cols[1]:
                st.markdown("<div style='text-align: center;'><a href='#how-it-works' style='color: #f4f9f7; text-decoration: none; font-weight: 500;'>How It Works</a></div>", unsafe_allow_html=True)
            with nav_cols[2]:
                st.markdown("<div style='text-align: center;'><a href='#pricing' style='color: #f4f9f7; text-decoration: none; font-weight: 500;'>Pricing</a></div>", unsafe_allow_html=True)
            with nav_cols[3]:
                st.markdown("<div style='text-align: center;'><a href='#testimonials' style='color: #f4f9f7; text-decoration: none; font-weight: 500;'>Testimonials</a></div>", unsafe_allow_html=True)
            with nav_cols[4]:
                st.markdown("<div style='text-align: center;'><a href='#faq' style='color: #f4f9f7; text-decoration: none; font-weight: 500;'>FAQ</a></div>", unsafe_allow_html=True)
        
        # Action buttons
        with cols[2]:
            action_cols = st.columns([1, 1])
            with action_cols[0]:
                if st.button("Login", key="navbar_login"):
                    st.session_state.auth_mode = 'login'
                    st.switch_page("pages/login.py")
            with action_cols[1]:
                if st.button("Get Started", type="primary", key="navbar_signup"):
                    st.session_state.auth_mode = 'register'
                    st.switch_page("pages/login.py")

def render_newsletter():
    """Render newsletter signup section using Streamlit components"""
    # Create a container with spacing for better alignment
    col_space1, col_main, col_space2 = st.columns([1, 10, 1])
    
    with col_main:
        st.markdown("<div style='text-align: center; margin: 2rem 0;'>", unsafe_allow_html=True)
        st.markdown("<h2 style='color: #f4f9f7; font-size: 1.75rem; margin-bottom: 0.5rem;'>Stay Updated</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color: rgba(244, 249, 247, 0.7); margin-bottom: 1.5rem;'>Subscribe to our newsletter for the latest features, updates, and security tips.</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Create a row for the email input and button
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Create a form for the newsletter
            with st.form(key="newsletter_form"):
                email = st.text_input("Email address", placeholder="Enter your email address")
                submit = st.form_submit_button("Subscribe", use_container_width=True)
                
                if submit and email:
                    st.success(f"Thank you for subscribing! We'll be in touch soon.")
        
        st.markdown("<p style='text-align: center; color: rgba(244, 249, 247, 0.5); font-size: 0.875rem; margin-top: 1rem;'>We respect your privacy. Unsubscribe at any time.</p>", unsafe_allow_html=True)
    
    # Add spacing after the section
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

def apply_landing_page_css():
    """Apply custom CSS specific to the landing page"""
    # Read the CSS file
    with open('landing_styles.css', 'r') as f:
        css = f.read()
    
    # Add additional CSS to hide the header button and ensure consistent spacing
    additional_css = """
    /* Hide the header collapse/expand button */
    button[kind="headerNoPadding"],
    button[data-testid="stBaseButton-headerNoPadding"],
    .st-emotion-cache-2ttwo3.em9zgd018 {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* Ensure consistent spacing in horizontal blocks */
    .stHorizontalBlock.st-emotion-cache-ocqkz7.eu6p4el0 {
        gap: 1rem !important;
        margin-left: 0 !important;
        margin-right: 0 !important;
        padding: 0 !important;
        width: 100% !important;
    }
    
    /* Ensure all columns in horizontal blocks have consistent spacing */
    .stHorizontalBlock.st-emotion-cache-ocqkz7.eu6p4el0 > div {
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
        box-sizing: border-box !important;
    }
    """
    
    # Apply the CSS
    st.markdown(f'<style>{css}{additional_css}</style>', unsafe_allow_html=True)

def render_footer():
    """Render the footer section using Streamlit components"""
    # Create a container with spacing for better alignment
    col_space1, col_main, col_space2 = st.columns([1, 10, 1])
    
    with col_main:
        st.markdown("<hr style='margin-top: 2rem; opacity: 0.2;'>", unsafe_allow_html=True)
        
        # Footer columns
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("### DocGenius")
            st.markdown("AI-powered document management for modern businesses.")
            st.markdown("🐦 Twitter | 💼 LinkedIn | 📱 Facebook")
        
        with col2:
            st.markdown("### Product")
            st.markdown("• [Features](#features)")
            st.markdown("• [Pricing](#pricing)")
            st.markdown("• [Testimonials](#testimonials)")
            st.markdown("• [FAQ](#faq)")
        
        with col3:
            st.markdown("### Resources")
            st.markdown("• Documentation")
            st.markdown("• Blog")
            st.markdown("• Support")
            st.markdown("• Community")
        
        with col4:
            st.markdown("### Company")
            st.markdown("• About Us")
            st.markdown("• Careers")
            st.markdown("• Contact")
            st.markdown("• Partners")
        
        # Copyright and legal
        st.markdown("<div style='text-align: center; margin-top: 2rem; padding-top: 1rem; border-top: 1px solid rgba(63, 215, 165, 0.1);'>", unsafe_allow_html=True)
        st.markdown("<span style='color: rgba(244, 249, 247, 0.7); font-size: 0.875rem;'>Terms of Service | Privacy Policy | Cookie Policy</span>", unsafe_allow_html=True)
        st.markdown("<p style='color: rgba(244, 249, 247, 0.7); font-size: 0.875rem; margin-top: 0.5rem;'>&copy; 2023 DocGenius. All rights reserved.</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

def render_scroll_to_top():
    """Render a scroll-to-top button using Streamlit components"""
    # Create a container with spacing for better alignment
    col_space1, col_main, col_space2 = st.columns([1, 10, 1])
    
    with col_main:
        # Center the button
        col1, col2, col3 = st.columns([3, 4, 3])
        with col2:
            if st.button("↑ Back to Top", use_container_width=True):
                st.markdown("""
                    <script>
                        window.scrollTo({top: 0, behavior: 'smooth'});
                    </script>
                    """, unsafe_allow_html=True)

def main():
    # Set current page for sidebar highlighting
    st.session_state['current_page'] = __file__
    
    # Apply custom CSS
    apply_custom_css()
    apply_landing_page_css()
    
    # Hide the sidebar for the landing page
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
    
    if check_authentication():
        # Redirect to dashboard if already logged in
        st.switch_page("pages/0_Dashboard.py")
    else:
        # Render the landing page
        render_navbar()
        render_hero_section()
        render_features_section()
        render_how_it_works()
        render_pricing_section()
        render_testimonials()
        render_faq_section()
        render_cta_section()
        render_newsletter()
        render_footer()
        render_scroll_to_top()

if __name__ == "__main__":
    main()