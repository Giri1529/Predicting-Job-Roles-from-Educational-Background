# pages/4_📊_Results.py (UPDATED - Top 3 Predictions + Logout)
# Results Page - View Prediction History

import streamlit as st
import pandas as pd
from auth_helper import require_auth, get_current_user, logout
from db_helper import fetch_history, insert_feedback
from global_css import GLOBAL_CSS

st.set_page_config(page_title="Results - Edu2Job", page_icon="📊", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

@require_auth
def main():
    user = get_current_user()
    
    # LOGOUT BUTTON
    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button("🚪 Logout", type="secondary", use_container_width=True):
            logout()
    
    st.title("📊 My Prediction Results")
    st.markdown(f"**View your prediction history, {user['username']}**")
    
    predictions = fetch_history(user['user_id'], limit=500)
    
    if not predictions:
        st.warning("🔭 No predictions yet. Make your first prediction!")
        if st.button("🎯 Make a Prediction"):
            st.switch_page("pages/3_🎯_Prediction.py")
        st.stop()
    
    # Enhanced DataFrame with TOP 3 predictions
    df = pd.DataFrame(predictions, columns=[
        "ID", "UserID", "Timestamp", "Degree", "Major", "Skill1", "Skill2",
        "Certification", "Experience", "Projects", "Internship", "Level",
        "Role 1", "Confidence 1",
        "Role 2", "Confidence 2",
        "Role 3", "Confidence 3",
        "Edu Gap", "Edu Gap Reason",
        "Career Gap", "Career Gap Years", "Career Gap Reason"
    ])
    
    tab1, tab2, tab3 = st.tabs(["📋 All Predictions", "📊 Statistics", "⭐ Feedback"])
    
    # ============================================
    # TAB 1: All Predictions
    # ============================================
    with tab1:
        st.markdown(f"### Total Predictions: {len(df)}")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            degree_filter = st.multiselect(
                "Filter by Degree",
                df['Degree'].unique(),
                default=None
            )
        
        with col2:
            role_filter = st.multiselect(
                "Filter by Top Predicted Role",
                df['Role 1'].unique(),
                default=None
            )
        
        with col3:
            skill_filter = st.multiselect(
                "Filter by Primary Skill",
                df['Skill1'].unique(),
                default=None
            )
        
        filtered_df = df.copy()
        
        if degree_filter:
            filtered_df = filtered_df[filtered_df['Degree'].isin(degree_filter)]
        
        if role_filter:
            filtered_df = filtered_df[filtered_df['Role 1'].isin(role_filter)]
        
        if skill_filter:
            filtered_df = filtered_df[filtered_df['Skill1'].isin(skill_filter)]
        
        st.markdown(f"**Showing {len(filtered_df)} of {len(df)} predictions**")
        
        # Display with TOP 3 predictions
        display_df = filtered_df[[
            "Timestamp", "Degree", "Major", "Skill1", "Skill2",
            "Certification", "Experience", "Projects",
            "Role 1", "Role 2", "Role 3"
        ]].copy()
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Expandable detailed view
        with st.expander("📋 View Detailed Information (with Gaps)"):
            detailed_df = filtered_df[[
                "Timestamp", "Degree", "Major", "Experience",
                "Role 1", "Role 2", "Role 3",
                "Edu Gap", "Edu Gap Reason",
                "Career Gap", "Career Gap Years", "Career Gap Reason"
            ]].copy()
            st.dataframe(detailed_df, use_container_width=True, hide_index=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            csv_data = filtered_df.to_csv(index=False)
            st.download_button(
                label="📥 Download as CSV",
                data=csv_data,
                file_name=f"predictions_{user['username']}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            if st.button("🔄 Refresh Data", use_container_width=True):
                st.rerun()
    
    # ============================================
    # TAB 2: Statistics
    # ============================================
    with tab2:
        st.markdown("### 📊 Your Prediction Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Predictions", len(df))
        
        with col2:
            st.metric("Unique Top Roles", df['Role 1'].nunique())
        
        with col3:
            avg_exp = df['Experience'].mean()
            st.metric("Avg Experience", f"{avg_exp:.1f} years")
        
        with col4:
            most_common = df['Role 1'].value_counts().index[0]
            st.metric("Most Predicted", most_common)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🎯 Top 5 Predicted Roles (1st Position)")
            role_counts = df['Role 1'].value_counts().head(5)
            for role, count in role_counts.items():
                percentage = (count / len(df)) * 100
                st.write(f"**{role}**: {count} times ({percentage:.1f}%)")
        
        with col2:
            st.markdown("#### 🛠️ Skills Breakdown")
            st.write("**Primary Skills:**")
            skill1_counts = df['Skill1'].value_counts().head(5)
            for skill, count in skill1_counts.items():
                st.write(f"- {skill}: {count}")
            
            st.write("**Secondary Skills:**")
            skill2_counts = df['Skill2'].value_counts().head(5)
            for skill, count in skill2_counts.items():
                st.write(f"- {skill}: {count}")
        
        st.markdown("---")
        
        st.markdown("#### 📈 Gap Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            edu_gap_count = (df['Edu Gap'] == 'Yes').sum()
            st.metric("Educational Gaps", edu_gap_count)
            if edu_gap_count > 0:
                st.write("**Reasons:**")
                gap_reasons = df[df['Edu Gap'] == 'Yes']['Edu Gap Reason'].value_counts()
                for reason, count in gap_reasons.items():
                    st.write(f"- {reason}: {count}")
        
        with col2:
            career_gap_count = (df['Career Gap'] == 'Yes').sum()
            st.metric("Career Gaps", career_gap_count)
            if career_gap_count > 0:
                avg_gap = df[df['Career Gap'] == 'Yes']['Career Gap Years'].mean()
                st.write(f"**Avg Duration:** {avg_gap:.1f} years")
                st.write("**Reasons:**")
                gap_reasons = df[df['Career Gap'] == 'Yes']['Career Gap Reason'].value_counts()
                for reason, count in gap_reasons.items():
                    st.write(f"- {reason}: {count}")
    
    # ============================================
    # TAB 3: Feedback
    # ============================================
    with tab3:
        st.markdown("### ⭐ Rate Your Experience")
        
        with st.form("feedback_form"):
            rating = st.slider("How accurate were the predictions?", 1, 5, 4)
            comments = st.text_area(
                "Any feedback or suggestions?",
                placeholder="Share your thoughts about the predictions...",
                height=150
            )
            
            submit_feedback = st.form_submit_button("💬 Submit Feedback", use_container_width=True, type="primary")
            
            if submit_feedback:
                if not comments.strip():
                    st.warning("Please add some comments!")
                else:
                    insert_feedback(user['user_id'], rating, comments)
                    st.success("✅ Thank you for your feedback!")
                    st.balloons()
        
        st.markdown("---")
        st.info("""
        💡 **Your feedback helps us improve!**
        
        We use your ratings and comments to:
        - Improve model accuracy
        - Better understand user needs
        - Add new features
        - Fix any issues
        
        Thank you for using Edu2Job! 🙏
        """)
    
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎯 Make New Prediction", use_container_width=True):
            st.switch_page("pages/3_🎯_Prediction.py")
    
    with col2:
        if st.button("📊 View Analytics", use_container_width=True):
            st.switch_page("pages/8_📊_Analytics.py")
    
    with col3:
        if st.button("🏠 Go Home", use_container_width=True):
            st.switch_page("app.py")

if __name__ == "__main__":
    main()