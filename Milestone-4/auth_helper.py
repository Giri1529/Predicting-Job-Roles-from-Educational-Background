# auth_helper.py
# JWT Authentication + Email OTP Verification for SmartLand Application

import jwt
import datetime
import smtplib
import random
from email.mime.text import MIMEText
from functools import wraps
import streamlit as st

# =============================
# CONFIGURATION - SET THESE!
# =============================
SECRET_KEY = "1fcc649c6502207128d04612c9b358aa42808112b999a2c1f1dc647b7bbf5e4e"
ALGORITHM = "HS256"
TOKEN_EXPIRY_HOURS = 24

# Email configuration for sending OTP
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_ADDRESS = "girinaruto1529@gmail.com"             # ✅ Your email
EMAIL_PASSWORD = "tgosxoyfavhzqzun"                   # ✅ Your Gmail App Password (no spaces)

# ======================================
# JWT TOKEN CREATION & VALIDATION
# ======================================
def create_token(user_id, username, role):
    payload = {
        'user_id': user_id,
        'username': username,
        'role': role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=TOKEN_EXPIRY_HOURS),
        'iat': datetime.datetime.utcnow()
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return {'error': 'Token expired. Login again.'}
    except jwt.InvalidTokenError:
        return {'error': 'Invalid token'}
    except Exception as e:
        return {'error': str(e)}

def verify_token(token):
    payload = decode_token(token)
    if 'error' in payload:
        return False, payload['error']
    return True, payload

# ======================================
# EMAIL OTP FUNCTIONS
# ======================================
def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(receiver_email, otp):
    try:
        msg = MIMEText(f"Your OTP for login is: {otp}\n\nThis code is valid for 5 minutes.")
        msg["Subject"] = "SmartLand Login Verification"
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = receiver_email

        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, receiver_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        st.error(f"⚠ Failed to send OTP email: {e}")
        return False

def start_email_verification(email, user_id, username, role):
    otp = generate_otp()
    st.session_state["otp"] = otp
    st.session_state["otp_user"] = {
        "email": email,
        "user_id": user_id,
        "username": username,
        "role": role
    }
    send_otp_email(email, otp)

def verify_otp(user_input_otp):
    if "otp" not in st.session_state or "otp_user" not in st.session_state:
        return False, "OTP expired. Try login again."

    if user_input_otp == st.session_state["otp"]:
        user = st.session_state["otp_user"]
        token = create_token(user["user_id"], user["username"], user["role"])

        st.session_state.token = token
        st.session_state.username = user["username"]
        st.session_state.role = user["role"]

        del st.session_state["otp"]
        del st.session_state["otp_user"]

        return True, "✅ OTP Verified. Login Successful."
    else:
        return False, "❌ Invalid OTP"

# ======================================
# AUTH DECORATORS
# ======================================
def require_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'token' not in st.session_state or not st.session_state.token:
            st.error("🔒 Please login first.")
            if st.button("Go to Login Page"):
                st.switch_page("pages/2_🔐_Login.py")
            st.stop()

        is_valid, payload = verify_token(st.session_state.token)
        if not is_valid:
            st.error(f"❌ Authentication failed: {payload}")
            st.session_state.clear()
            if st.button("Go to Login Page"):
                st.switch_page("pages/2_🔐_Login.py")
            st.stop()

        return func(*args, **kwargs)
    return wrapper

def require_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'token' not in st.session_state:
            st.error("Admin access required.")
            st.stop()
        
        is_valid, payload = verify_token(st.session_state.token)
        if not is_valid:
            st.error("Invalid/Expired token.")
            st.stop()

        if payload.get("role") != "admin":
            st.error("Access Denied: Admins only.")
            st.stop()

        return func(*args, **kwargs)
    return wrapper

# ======================================
# USER STATE HELPERS
# ======================================
def get_current_user():
    if 'token' not in st.session_state:
        return None
    is_valid, payload = verify_token(st.session_state.token)
    if not is_valid:
        return None
    return {
        'user_id': payload.get('user_id'),
        'username': payload.get('username'),
        'role': payload.get('role')
    }

def is_authenticated():
    return get_current_user() is not None

def is_admin():
    user = get_current_user()
    return user and user.get("role") == "admin"

def logout():
    st.session_state.clear()
    st.rerun()

def refresh_token():
    user = get_current_user()
    if user:
        return create_token(user["user_id"], user["username"], user["role"])
    return None

def get_token_expiry():
    if 'token' not in st.session_state:
        return None
    is_valid, payload = verify_token(st.session_state.token)
    if not is_valid:
        return None
    exp = payload.get('exp')
    if exp:
        remaining = datetime.datetime.fromtimestamp(exp) - datetime.datetime.utcnow()
        return int(remaining.total_seconds() / 60)
    return None
