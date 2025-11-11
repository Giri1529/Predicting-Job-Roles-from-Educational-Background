# ============================================================================
# pages/6_⚙️_Admin_Panel.py (UPDATED - Edu2Job Branding)
# ============================================================================

import streamlit as st
import pandas as pd
import joblib
from auth_helper import require_admin, get_current_user
from global_css import GLOBAL_CSS
from db_helper import (
    get_all_users, delete_user, update_user_role, get_all_predictions,
    get_all_feedback, log_model_action, log_dataset_upload,
    get_model_logs, get_dataset_uploads, get_dashboard_stats
)
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

st.set_page_config(page_title="Admin Panel - Edu2Job", page_icon="⚙️", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

@require_admin
def main():
    user = get_current_user()
    
    st.title("⚙️ Admin Control Panel")
    st.markdown(f"**Admin:** {user['username']}")
    
    stats = get_dashboard_stats()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Users", stats['total_users'])
    col2.metric("Total Predictions", stats['total_predictions'])
    col3.metric("Avg Rating", f"{stats['avg_rating']}⭐")
    col4.metric("Top Role", stats['top_role'])
    
    st.markdown("---")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "👥 User Management", 
        "📊 Prediction Logs", 
        "📁 Dataset Upload", 
        "🤖 Model Retraining"
    ])
    
    with tab1:
        st.subheader("👥 User Management")
        
        users = get_all_users()
        if users:
            df_users = pd.DataFrame(users, columns=[
                "ID", "Username", "Email", "Role", "Created", "Last Login"
            ])
            st.dataframe(df_users, use_container_width=True)
            
            col1, col2 = st.columns(2)
            with col1:
                user_to_delete = st.number_input("Delete User ID", min_value=1, step=1)
                if st.button("🗑️ Delete User"):
                    if delete_user(user_to_delete):
                        st.success("✅ User deleted!")
                        st.rerun()
                    else:
                        st.error("❌ Delete failed")
            
            with col2:
                user_to_update = st.number_input("Update User ID", min_value=1, step=1)
                new_role = st.selectbox("New Role", ["user", "admin"])
                if st.button("🔄 Update Role"):
                    if update_user_role(user_to_update, new_role):
                        st.success("✅ Role updated!")
                        st.rerun()
    
    with tab2:
        st.subheader("📊 All Prediction Logs")
        
        predictions = get_all_predictions(1000)
        if predictions:
            df_pred = pd.DataFrame(predictions, columns=[
                "ID", "Username", "Timestamp", "Degree", "Major", 
                "Skill1", "Skill2", "Predicted Role"
            ])
            st.dataframe(df_pred, use_container_width=True)
            
            csv = df_pred.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Logs", csv, "prediction_logs.csv")
        else:
            st.info("No predictions yet")
    
    with tab3:
        st.subheader("📁 Dataset Upload & Management")
        
        uploaded_file = st.file_uploader("Upload New Training Dataset (CSV)", type=['csv'])
        
        if uploaded_file:
            df_new = pd.read_csv(uploaded_file)
            st.dataframe(df_new.head(10))
            
            if st.button("💾 Save Dataset"):
                df_new.to_csv("final_high_accuracy_job_dataset.csv", index=False)
                log_dataset_upload(user['user_id'], uploaded_file.name, len(df_new), "success")
                st.success(f"✅ Saved {len(df_new)} rows!")
        
        st.markdown("---")
        st.subheader("📜 Upload History")
        uploads = get_dataset_uploads(20)
        if uploads:
            df_uploads = pd.DataFrame(uploads, columns=[
                "ID", "Admin", "Timestamp", "Filename", "Rows", "Status"
            ])
            st.dataframe(df_uploads)
    
    with tab4:
        st.subheader("🤖 Model Retraining")
        
        if st.button("🔄 Retrain Model", type="primary"):
            with st.spinner("Training model..."):
                try:
                    df = pd.read_csv("final_high_accuracy_job_dataset.csv")
                    
                    X = df.drop(['job_role'], axis=1, errors='ignore')
                    y = df['job_role'] if 'job_role' in df.columns else df.iloc[:, -1]
                    
                    le = LabelEncoder()
                    for col in X.select_dtypes(include=['object']).columns:
                        X[col] = le.fit_transform(X[col].astype(str))
                    
                    y_encoded = le.fit_transform(y)
                    
                    X_train, X_test, y_train, y_test = train_test_split(
                        X, y_encoded, test_size=0.2, random_state=42
                    )
                    
                    model = RandomForestClassifier(n_estimators=100, random_state=42)
                    model.fit(X_train, y_train)
                    
                    accuracy = accuracy_score(y_test, model.predict(X_test))
                    
                    joblib.dump((model, le), "best_model.pkl")
                    
                    log_model_action(user['user_id'], "retrain", "RandomForest", 
                                   accuracy, f"Retrained on {len(df)} samples")
                    
                    st.success(f"✅ Model retrained! Accuracy: {accuracy*100:.2f}%")
                    st.balloons()
                
                except Exception as e:
                    st.error(f"❌ Retraining failed: {e}")
        
        st.markdown("---")
        st.subheader("📜 Model Logs")
        logs = get_model_logs(20)
        if logs:
            df_logs = pd.DataFrame(logs, columns=[
                "ID", "Admin", "Timestamp", "Action", "Model", "Accuracy", "Details"
            ])
            st.dataframe(df_logs)

if __name__ == "__main__":
    main()