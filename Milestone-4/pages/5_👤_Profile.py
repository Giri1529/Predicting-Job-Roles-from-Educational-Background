import streamlit as st
from auth_helper import require_auth, get_current_user
from db_helper import get_user_info, update_user_profile, change_password, insert_feedback
from global_css import GLOBAL_CSS

st.set_page_config(page_title="Profile - SmartLand", page_icon="👤", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

@require_auth
def main():
    user = get_current_user()
    user_info = get_user_info(user['user_id'])
    
    st.title("👤 My Profile")
    
    tab1, tab2, tab3 = st.tabs(["📝 Profile Info", "🔐 Change Password", "⭐ Feedback"])
    
    # Tab 1: Profile Info
    with tab1:
        st.subheader("Profile Information")
        
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Username", value=user_info['username'], disabled=True)
            new_email = st.text_input("Email", value=user_info['email'])
        with col2:
            st.text_input("Role", value=user_info['role'].title(), disabled=True)
            st.text_input("Member Since", value=user_info['created_at'], disabled=True)
        
        if st.button("💾 Update Profile"):
            if update_user_profile(user['user_id'], new_email):
                st.success("✅ Profile updated!")
            else:
                st.error("❌ Update failed")
    
    # Tab 2: Change Password
    with tab2:
        st.subheader("Change Password")
        
        with st.form("change_password"):
            old_pwd = st.text_input("Current Password", type="password")
            new_pwd = st.text_input("New Password", type="password")
            confirm_pwd = st.text_input("Confirm New Password", type="password")
            
            if st.form_submit_button("🔒 Change Password"):
                if new_pwd != confirm_pwd:
                    st.error("❌ Passwords don't match")
                elif change_password(user['user_id'], old_pwd, new_pwd):
                    st.success("✅ Password changed!")
                else:
                    st.error("❌ Current password incorrect")
    
    # Tab 3: Feedback
    with tab3:
        st.subheader("Share Your Feedback")
        
        with st.form("feedback_form"):
            rating = st.slider("Rating", 1, 5, 4)
            comment = st.text_area("Comments")
            
            if st.form_submit_button("📤 Submit Feedback"):
                insert_feedback(user['user_id'], rating, comment)
                st.success("✅ Thank you for your feedback!")

if __name__ == "__main__":
    main()