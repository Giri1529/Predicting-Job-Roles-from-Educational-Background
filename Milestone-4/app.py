# app.py (PREMIUM VERSION WITH DARK/LIGHT MODE & FEATURES)
# Main Entry Point for SmartLand Job Role Predictor

import streamlit as st
from db_helper import init_db
from auth_helper import is_authenticated, get_current_user, logout
from global_css import GLOBAL_CSS
import time

# Initialize database
init_db()

# Page configuration
st.set_page_config(
    page_title="SmartLand - AI Job Role Predictor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# THEME CONFIGURATION
# ============================================

# Initialize session state for theme
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'  # Default: dark mode

if 'sidebar_expanded' not in st.session_state:
    st.session_state.sidebar_expanded = True

if 'show_notifications' not in st.session_state:
    st.session_state.show_notifications = True

# ============================================
# THEME CSS
# ============================================

DARK_MODE_CSS = """
<style>
:root {
    --bg-primary: #0f1419;
    --bg-secondary: #1a1f2e;
    --text-primary: #ffffff;
    --text-secondary: #b0b8c1;
    --border-color: rgba(102, 126, 234, 0.2);
}

body {
    background-color: var(--bg-primary);
    color: var(--text-primary);
}

.stApp {
    background-color: var(--bg-primary);
}

[data-testid="stSidebar"] {
    background-color: var(--bg-secondary);
}

/* Dark mode cards */
.metric-card {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.15), rgba(118, 75, 162, 0.15)) !important;
    border: 1px solid var(--border-color) !important;
}

.info-box {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.08), rgba(118, 75, 162, 0.08)) !important;
    border: 1px solid var(--border-color) !important;
}

.feature-item {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.08), rgba(118, 75, 162, 0.08)) !important;
    border: 1px solid var(--border-color) !important;
}
</style>
"""

LIGHT_MODE_CSS = """
<style>
:root {
    --bg-primary: #ffffff;
    --bg-secondary: #f8f9fa;
    --text-primary: #2d3748;
    --text-secondary: #718096;
    --border-color: rgba(102, 126, 234, 0.15);
}

body {
    background-color: var(--bg-primary);
    color: var(--text-primary);
}

.stApp {
    background-color: var(--bg-primary);
}

[data-testid="stSidebar"] {
    background-color: var(--bg-secondary);
}

/* Light mode cards */
.metric-card {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.08), rgba(118, 75, 162, 0.08)) !important;
    border: 1px solid var(--border-color) !important;
}

.info-box {
    background: linear-gradient(135deg, rgba(240, 243, 246, 0.5), rgba(226, 232, 240, 0.5)) !important;
}

.feature-item {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.05), rgba(118, 75, 162, 0.05)) !important;
}
</style>
"""

# Apply global CSS
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# Apply theme CSS
if st.session_state.theme == 'dark':
    st.markdown(DARK_MODE_CSS, unsafe_allow_html=True)
else:
    st.markdown(LIGHT_MODE_CSS, unsafe_allow_html=True)

# ============================================
# PREMIUM CUSTOM CSS
# ============================================

PREMIUM_CSS = """
<style>
/* Enhanced Animations */
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes slideUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Main Container */
.main-container {
    animation: fadeIn 0.5s ease-in;
}

/* Notification Badge */
.notification-badge {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    display: inline-block;
    margin-bottom: 1rem;
}

/* Premium Button */
.premium-button {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    color: white !important;
    border-radius: 15px !important;
    padding: 0.75rem 1.5rem !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 10px 25px rgba(102, 126, 234, 0.2) !important;
}

.premium-button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4) !important;
}

/* Stats Grid */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}

/* Welcome Section */
.welcome-banner {
    background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #667eea);
    background-size: 400% 400%;
    animation: gradientShift 15s ease infinite;
    padding: 2rem;
    border-radius: 20px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
}

/* Feature Showcase */
.feature-showcase {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}

/* User Card */
.user-card {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
    border: 1px solid rgba(102, 126, 234, 0.2);
    border-radius: 15px;
    padding: 1.5rem;
    text-align: center;
}

.user-avatar {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background: linear-gradient(135deg, #667eea, #764ba2);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    margin: 0 auto 1rem;
    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
}

/* Quick Links */
.quick-link {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
    border: 1px solid rgba(102, 126, 234, 0.2);
    padding: 1rem;
    border-radius: 12px;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
    margin: 0.5rem 0;
}

.quick-link:hover {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.2), rgba(118, 75, 162, 0.2));
    border-color: rgba(240, 147, 251, 0.4);
    transform: translateY(-2px);
}

/* Footer */
.footer {
    text-align: center;
    padding: 2rem;
    border-top: 1px solid rgba(102, 126, 234, 0.1);
    margin-top: 3rem;
    opacity: 0.8;
}

/* Status Indicator */
.status-online {
    display: inline-block;
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: #10b981;
    margin-right: 0.5rem;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}
</style>
"""

st.markdown(PREMIUM_CSS, unsafe_allow_html=True)

# ============================================
# SIDEBAR WITH THEME TOGGLE & SETTINGS
# ============================================

with st.sidebar:
    # Theme Toggle
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("🌙" if st.session_state.theme == 'light' else "☀️", 
                     help="Toggle Dark/Light Mode",
                     key="theme_toggle"):
            st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
            st.rerun()
    
    with col2:
        st.caption(f"{'🌙 Dark Mode' if st.session_state.theme == 'dark' else '☀️ Light Mode'}")
    
    with col3:
        if st.button("⚙️", help="Settings", key="settings_btn"):
            st.session_state.show_settings = True
    
    st.markdown("---")
    
    # User Info (if logged in)
    if is_authenticated():
        user = get_current_user()
        
        st.markdown("""
            <div class='user-card'>
                <div class='user-avatar'>👤</div>
                <h3 style='margin: 0.5rem 0;'>""" + user['username'] + """</h3>
                <p style='margin: 0; opacity: 0.8; font-size: 0.9rem;'>✅ Active</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
    
    # Main Navigation
    st.subheader("📊 Navigation")
    st.page_link("pages/1_🏠_Home.py", label="🏠 Home", use_container_width=True)
    st.page_link("pages/3_🎯_Prediction.py", label="🎯 Make Prediction", use_container_width=True)
    st.page_link("pages/4_📊_Results.py", label="📊 My Results", use_container_width=True)
    st.page_link("pages/5_👤_Profile.py", label="👤 My Profile", use_container_width=True)
    
    st.markdown("---")
    
    # Advanced Tools
    st.subheader("🔍 Advanced Tools")
    st.page_link("pages/7_📈_Model_Insights.py", label="📈 Model Insights", use_container_width=True)
    st.page_link("pages/8_📊_Analytics.py", label="📊 Analytics", use_container_width=True)
    st.page_link("pages/9_🎓_Skill_Gap.py", label="🎓 Skill Gap", use_container_width=True)
    
    if is_authenticated():
        user = get_current_user()
        if user['role'] == 'admin':
            st.markdown("---")
            st.subheader("⚙️ Admin")
            st.page_link("pages/6_⚙️_Admin_Panel.py", label="⚙️ Admin Panel", use_container_width=True)
    
    st.markdown("---")
    
    # Stats
    st.subheader("📈 Quick Stats")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Theme", "Dark" if st.session_state.theme == 'dark' else "Light")
    
    with col2:
        if is_authenticated():
            st.metric("Status", "Online")
        else:
            st.metric("Status", "Offline")
    
    st.markdown("---")
    
    # Logout or Login
    if is_authenticated():
        if st.button("🚪 Logout", use_container_width=True, type="secondary"):
            logout()
    else:
        st.info("👈 Please login to continue")
        st.page_link("pages/2_🔐_Login.py", label="🔐 Login / Sign Up", use_container_width=True)
    
    st.markdown("---")
    
    # Footer Info
    st.markdown("""
        <div style='font-size: 0.8rem; opacity: 0.6; text-align: center;'>
            <p>SmartLand v2.0</p>
            <p>AI Job Role Predictor</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# MAIN CONTENT
# ============================================

# Hero Section
st.markdown("""
    <div class='welcome-banner'>
        <h1 style='margin: 0; font-size: 3rem;'>🎓 SmartLand</h1>
        <h3 style='margin: 0.5rem 0 0 0; opacity: 0.95;'>AI-Powered Career Intelligence Platform</h3>
    </div>
    """, unsafe_allow_html=True)

if is_authenticated():
    user = get_current_user()
    
    # Welcome Section
    st.markdown(f"""
        <div class='notification-badge'>
            👋 Welcome back, <strong>{user['username']}</strong>!
        </div>
        """, unsafe_allow_html=True)
    
    # Quick Stats
    st.markdown("### 📊 Quick Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div class='metric-card'>
                <div style='font-size: 2rem;'>🎯</div>
                <h3 style='margin: 0.5rem 0 0 0;'>Predictions</h3>
                <p style='margin: 0; opacity: 0.7;'>Ready to predict</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class='metric-card'>
                <div style='font-size: 2rem;'>📈</div>
                <h3 style='margin: 0.5rem 0 0 0;'>Analytics</h3>
                <p style='margin: 0; opacity: 0.7;'>Track your journey</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class='metric-card'>
                <div style='font-size: 2rem;'>🎓</div>
                <h3 style='margin: 0.5rem 0 0 0;'>Skills</h3>
                <p style='margin: 0; opacity: 0.7;'>Identify gaps</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
            <div class='metric-card'>
                <div style='font-size: 2rem;'>⭐</div>
                <h3 style='margin: 0.5rem 0 0 0;'>Insights</h3>
                <p style='margin: 0; opacity: 0.7;'>Model analysis</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Main CTA Buttons
    st.markdown("### ⚡ Get Started")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎯 Make Prediction", use_container_width=True, type="primary"):
            st.switch_page("pages/3_🎯_Prediction.py")
    
    with col2:
        if st.button("📊 View Analytics", use_container_width=True):
            st.switch_page("pages/8_📊_Analytics.py")
    
    with col3:
        if st.button("🎓 Skill Gap", use_container_width=True):
            st.switch_page("pages/9_🎓_Skill_Gap.py")
    
    st.markdown("---")
    
    # Advanced Features
    st.markdown("### 🚀 Advanced Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class='feature-item'>
                <h4>🤖 AI Model</h4>
                <p>Advanced machine learning with 85%+ accuracy trained on real industry data</p>
            </div>
            """, unsafe_allow_html=True)
        if st.button("Explore Model", use_container_width=True, key="model_btn"):
            st.switch_page("pages/7_📈_Model_Insights.py")
    
    with col2:
        st.markdown("""
            <div class='feature-item'>
                <h4>📊 Analytics</h4>
                <p>Comprehensive dashboard with visual analytics and trend analysis</p>
            </div>
            """, unsafe_allow_html=True)
        if st.button("View Dashboard", use_container_width=True, key="analytics_btn"):
            st.switch_page("pages/8_📊_Analytics.py")
    
    with col3:
        st.markdown("""
            <div class='feature-item'>
                <h4>🎓 Learning</h4>
                <p>Personalized skill gap analysis with learning recommendations</p>
            </div>
            """, unsafe_allow_html=True)
        if st.button("Start Learning", use_container_width=True, key="learning_btn"):
            st.switch_page("pages/9_🎓_Skill_Gap.py")
    
    # Admin Section
    if user['role'] == 'admin':
        st.markdown("---")
        st.markdown("### ⚙️ Admin Controls")
        
        if st.button("🔧 Admin Panel", use_container_width=True):
            st.switch_page("pages/6_⚙️_Admin_Panel.py")

else:
    # Not logged in
    st.info("👈 Please **login or sign up** from the sidebar to get started!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.page_link("pages/2_🔐_Login.py", label="🔐 Login", use_container_width=True)
    
    with col2:
        st.page_link("pages/2_🔐_Login.py", label="📝 Sign Up", use_container_width=True)
    
    st.markdown("---")
    
    # Features Overview
    st.markdown("### ✨ Why SmartLand?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 🎯 Accurate Predictions
        - Advanced ML algorithms
        - Trained on industry data
        - 85%+ accuracy
        
        #### 📊 Analytics
        - Prediction history
        - Visual trends
        - Export reports
        """)
    
    with col2:
        st.markdown("""
        #### 🔐 Secure
        - JWT authentication
        - Email verification
        - Data privacy
        
        #### 💼 Career Insights
        - Skill analysis
        - Learning roadmap
        - Recommendations
        """)

# ============================================
# FOOTER
# ============================================

st.markdown("""
    <div class='footer'>
        <p><strong>🎓 SmartLand</strong> • AI Job Role Prediction System</p>
        <p style='font-size: 0.9rem;'>✨ <em>Empowering careers with artificial intelligence</em></p>
        <p style='font-size: 0.85rem; opacity: 0.6;'>© 2024 SmartLand • v2.0 Premium</p>
    </div>
    """, unsafe_allow_html=True)