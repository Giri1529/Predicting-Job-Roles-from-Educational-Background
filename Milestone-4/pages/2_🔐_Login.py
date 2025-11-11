# pages/2_🔐_Login.py (FIXED - OTP only on signup)
# Login and Sign Up Page with JWT Authentication + Email OTP Verification on Signup Only

import streamlit as st
from db_helper import register_user, verify_user
from auth_helper import create_token, is_authenticated
import re
from global_css import GLOBAL_CSS  # ← ADD THIS LINE



st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

st.set_page_config(page_title="Login - SmartLand", page_icon="🔐", layout="centered")

st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# Custom CSS
st.markdown("""
    <style>
    .login-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        height: 3em;
        font-size: 18px;
    }
    .otp-box {
        background-color: #f0f8ff;
        border-left: 4px solid #667eea;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# Check if already logged in
if is_authenticated():
    st.success("✅ You are already logged in!")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏠 Go to Home"):
            st.switch_page("app.py")
    with col2:
        if st.button("🎯 Make Prediction"):
            st.switch_page("pages/3_🎯_Prediction.py")
    st.stop()

# Header
st.markdown("""
    <div class='login-header'>
        <h1>🔐 Welcome to SmartLand</h1>
        <p>Login or Create Your Account</p>
    </div>
    """, unsafe_allow_html=True)

# Check if in OTP verification mode (only for signup)
if 'email_pending_verification' in st.session_state and st.session_state.email_pending_verification:
    st.markdown("### 📧 Email Verification (Signup)")
    st.markdown(f"We've sent an OTP to **{st.session_state.get('pending_email', 'your email')}**")
    
    with st.form("otp_verification_form"):
        otp_input = st.text_input("Enter 6-digit OTP", placeholder="000000", max_chars=6)
        
        verify_btn = st.form_submit_button("✅ Verify OTP", use_container_width=True, type="primary")
        
        if verify_btn:
            if not otp_input or len(otp_input) != 6:
                st.error("❌ Please enter a valid 6-digit OTP")
            else:
                # Get stored OTP
                if "otp" in st.session_state and otp_input == st.session_state["otp"]:
                    st.success("✅ Email Verified Successfully!")
                    st.balloons()
                    st.session_state.email_pending_verification = False
                    st.info("👈 Now login with your username and password from the Login tab")
                    st.rerun()
                else:
                    st.error("❌ Invalid OTP. Please try again.")
    
    st.markdown("---")
    if st.button("← Back to Signup"):
        st.session_state.email_pending_verification = False
        st.rerun()

else:
    # Login/Signup tabs
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Sign Up"])
    
    # ============================================================================
    # LOGIN TAB
    # ============================================================================
    with tab1:
        st.subheader("Login to Your Account")
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            submit_login = st.form_submit_button("🚀 Login", use_container_width=True, type="primary")
            
            if submit_login:
                if not username or not password:
                    st.error("❌ Please enter both username and password")
                else:
                    with st.spinner("Authenticating..."):
                        user_data = verify_user(username, password)
                        
                        if user_data:
                            # ✅ LOGIN SUCCESSFUL - NO OTP NEEDED
                            # Create JWT token
                            token = create_token(
                                user_data['user_id'],
                                username,
                                user_data['role']
                            )
                            
                            # Store token in session
                            st.session_state.token = token
                            st.session_state.user_id = user_data['user_id']
                            st.session_state.username = username
                            st.session_state.role = user_data['role']
                            
                            st.success(f"✅ Welcome back, {username}!")
                            st.balloons()
                            
                            # Redirect based on role
                            if user_data['role'] == 'admin':
                                st.info("🔧 Redirecting to Admin Panel...")
                                st.switch_page("pages/6_⚙️_Admin_Panel.py")
                            else:
                                st.info("🎯 Redirecting to Prediction Page...")
                                st.switch_page("pages/3_🎯_Prediction.py")
                        else:
                            st.error("❌ Invalid username or password")
        
        st.markdown("---")
        st.info("""
        💡 **Demo Admin Account:**
        - Username: `giridhar`
        - Password: `Giridhar@25`
        """)
    
    # ============================================================================
    # SIGN UP TAB
    # ============================================================================
    with tab2:
        st.subheader("Create New Account")
        
        with st.form("signup_form"):
            new_username = st.text_input("Username", placeholder="Choose a username (3+ characters)")
            new_email = st.text_input("Email", placeholder="Enter your email")
            new_password = st.text_input("Password", type="password", placeholder="Choose a password (6+ characters)")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter password")
            
            agree_terms = st.checkbox("I agree to the Terms and Conditions")
            
            submit_signup = st.form_submit_button("📝 Create Account", use_container_width=True, type="primary")
            
            if submit_signup:
                # Validation
                errors = []
                
                if not new_username or not new_email or not new_password:
                    errors.append("❌ All fields are required")
                
                if len(new_username) < 3:
                    errors.append("❌ Username must be at least 3 characters")
                
                if not re.match(r"[^@]+@[^@]+\.[^@]+", new_email):
                    errors.append("❌ Invalid email format")
                
                if len(new_password) < 6:
                    errors.append("❌ Password must be at least 6 characters")
                
                if new_password != confirm_password:
                    errors.append("❌ Passwords do not match")
                
                if not agree_terms:
                    errors.append("❌ Please agree to the Terms and Conditions")
                
                # Display errors or register
                if errors:
                    for error in errors:
                        st.error(error)
                else:
                    with st.spinner("Creating your account..."):
                        success = register_user(new_username, new_email, new_password)
                        
                        if success:
                            # ✅ ACCOUNT CREATED - NOW SEND OTP FOR EMAIL VERIFICATION
                            st.success("✅ Account created! Now verifying your email...")
                            
                            # Generate and send OTP
                            from auth_helper import send_otp_email, generate_otp
                            otp = generate_otp()
                            
                            # Store OTP in session
                            st.session_state["otp"] = otp
                            st.session_state.email_pending_verification = True
                            st.session_state.pending_email = new_email
                            
                            # Send OTP email
                            if send_otp_email(new_email, otp):
                                st.balloons()
                                st.info("📧 OTP has been sent to your email! Please check and enter it below.")
                                st.rerun()
                            else:
                                st.warning("⚠️ Account created but OTP email failed to send. You can login directly.")
                                st.info("👈 Please login from the Login tab")
                        else:
                            st.error("❌ Username already exists. Please choose a different username.")
        
        st.markdown("---")
        st.info("✨ **Account Benefits:**\n- Save your predictions\n- View prediction history\n- Track your progress\n- Access career insights")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🔒 Your data is secure with us | ✉️ Email verified signup</p>
        <p>© 2024 SmartLand - AI Job Role Prediction System</p>
    </div>
    """, unsafe_allow_html=True)