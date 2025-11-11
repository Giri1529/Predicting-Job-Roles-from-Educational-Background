# pages/1_🏠_Home.py
# Home Page with Features and Information

import streamlit as st
from auth_helper import get_current_user
from db_helper import get_dashboard_stats
from global_css import GLOBAL_CSS

st.set_page_config(page_title="Home - SmartLand", page_icon="🏠", layout="wide")

st.markdown(GLOBAL_CSS, unsafe_allow_html=True)



# Custom CSS
st.markdown("""
    <style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏠 Home - SmartLand Platform")

user = get_current_user()

if user:
    st.markdown(f"## Welcome back, **{user['username']}**! 👋")
    
    # Get dashboard stats
    stats = get_dashboard_stats()
    
    st.markdown("### 📊 Platform Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class='metric-card'>
                <h2>{stats['total_users']}</h2>
                <p>Total Users</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class='metric-card'>
                <h2>{stats['total_predictions']}</h2>
                <p>Predictions Made</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class='metric-card'>
                <h2>{stats['avg_rating']}⭐</h2>
                <p>Average Rating</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class='metric-card'>
                <h2>{stats['top_role']}</h2>
                <p>Top Predicted Role</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
else:
    st.warning("Please login to view personalized content")

# About Section
st.markdown("### 📖 About SmartLand")
st.markdown("""
<div class='info-box'>
<p>SmartLand is an AI-powered job role prediction system that helps students and professionals 
find the most suitable career paths based on their education, skills, and experience.</p>

<p>Our advanced machine learning algorithms analyze your profile and provide accurate 
predictions to guide your career decisions.</p>
</div>
""", unsafe_allow_html=True)

# Features Section
st.markdown("### ✨ Key Features")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class='info-box'>
        <h4>🎯 Accurate Predictions</h4>
        <ul>
            <li>Advanced ML algorithms</li>
            <li>Trained on real industry data</li>
            <li>High accuracy rate</li>
            <li>Multiple job role options</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='info-box'>
        <h4>🔒 Secure & Private</h4>
        <ul>
            <li>JWT authentication</li>
            <li>Encrypted passwords</li>
            <li>Data privacy guaranteed</li>
            <li>GDPR compliant</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='info-box'>
        <h4>📊 Analytics Dashboard</h4>
        <ul>
            <li>Track your predictions</li>
            <li>View prediction history</li>
            <li>Export results as CSV</li>
            <li>Visual analytics</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='info-box'>
        <h4>💼 Career Insights</h4>
        <ul>
            <li>Job role recommendations</li>
            <li>Skill gap analysis</li>
            <li>Career path suggestions</li>
            <li>Industry trends</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# How It Works
st.markdown("### 🔄 How It Works")

st.markdown("""
<div class='info-box'>
<ol>
    <li><strong>Create Account:</strong> Sign up with your email and create a profile</li>
    <li><strong>Enter Details:</strong> Provide your educational background, skills, and experience</li>
    <li><strong>Get Prediction:</strong> Our AI analyzes your profile and predicts suitable job roles</li>
    <li><strong>View Results:</strong> See your predictions with confidence scores and recommendations</li>
    <li><strong>Track History:</strong> Access all your past predictions and track your progress</li>
</ol>
</div>
""", unsafe_allow_html=True)

# Sample Job Recommendations
st.markdown("### 💼 Sample Job Recommendations")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class='info-box'>
        <h4>🤖 AI/ML Roles</h4>
        <ul>
            <li>Data Scientist</li>
            <li>ML Engineer</li>
            <li>AI Specialist</li>
            <li>Data Analyst</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='info-box'>
        <h4>💻 Development Roles</h4>
        <ul>
            <li>Software Developer</li>
            <li>Full Stack Developer</li>
            <li>Frontend Developer</li>
            <li>Backend Developer</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class='info-box'>
        <h4>🔐 Security Roles</h4>
        <ul>
            <li>Cybersecurity Engineer</li>
            <li>Security Analyst</li>
            <li>Penetration Tester</li>
            <li>Security Consultant</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Quick Actions
if user:
    st.markdown("---")
    st.markdown("### ⚡ Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎯 Make a Prediction", use_container_width=True, type="primary"):
            st.switch_page("pages/3_🎯_Prediction.py")
    
    with col2:
        if st.button("📊 View My Results", use_container_width=True):
            st.switch_page("pages/4_📊_Results.py")
    
    with col3:
        if st.button("👤 Edit Profile", use_container_width=True):
            st.switch_page("pages/5_👤_Profile.py")

st.markdown("---")
st.caption("© 2024 SmartLand - Empowering Career Decisions with AI")