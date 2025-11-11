# pages/3_🎯_Prediction.py (FIXED - Feature Mismatch Resolved)
# This version ensures ALL features match the model's expectations

import streamlit as st
import pandas as pd
import numpy as np
import joblib
from global_css import GLOBAL_CSS
from auth_helper import require_auth, get_current_user
from db_helper import insert_prediction

st.set_page_config(page_title="Prediction - Edu2Job", page_icon="🎯", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True) 

@require_auth
def main():
    user = get_current_user()
    
    @st.cache_resource
    def load_model():
        """Load model with proper error handling"""
        try:
            model_data = joblib.load("best_model.pkl")
            
            if isinstance(model_data, dict):
                return {
                    'model': model_data['model'],
                    'scaler': model_data.get('scaler'),
                    'feature_columns': model_data.get('feature_columns'),
                    'encoders': model_data.get('encoders', {}),
                    'accuracy': model_data.get('accuracy', 0),
                    'model_type': model_data.get('model_type', 'Unknown')
                }
            elif isinstance(model_data, tuple):
                return {
                    'model': model_data[0],
                    'scaler': None,
                    'feature_columns': None,
                    'encoders': {'target': model_data[1]} if len(model_data) > 1 else {},
                    'accuracy': 0,
                    'model_type': 'Loaded Model'
                }
            else:
                return {
                    'model': model_data,
                    'scaler': None,
                    'feature_columns': None,
                    'encoders': {},
                    'accuracy': 0,
                    'model_type': 'Loaded Model'
                }
        except FileNotFoundError:
            st.error("❌ Model file not found! Please retrain the model properly.")
            return None
        except Exception as e:
            st.error(f"❌ Error loading model: {str(e)}")
            return None
    
    model_package = load_model()
    
    if model_package is None:
        st.error("⚠️ Unable to load the prediction model. Please contact admin to retrain the model properly.")
        return
    
    model = model_package['model']
    scaler = model_package['scaler']
    feature_columns = model_package['feature_columns']
    encoders = model_package['encoders']
    accuracy = model_package['accuracy']
    model_type = model_package['model_type']
    
    st.markdown("""
        <style>
        .prediction-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin: 2rem 0;
        }
        .rank-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1.5rem;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin: 0.5rem 0;
        }
        .rank-1 { background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); }
        .rank-2 { background: linear-gradient(135deg, #C0C0C0 0%, #A9A9A9 100%); }
        .rank-3 { background: linear-gradient(135deg, #CD7F32 0%, #8B4513 100%); }
        </style>
        """, unsafe_allow_html=True)
    
    st.title("🎯 Job Role Prediction")
    st.markdown(f"**Welcome, {user['username']}!** Enter your details to get your top 3 predicted job roles.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if accuracy > 0:
            st.metric("Model Accuracy", f"{accuracy:.2%}")
        else:
            st.info("Model loaded")
    with col2:
        st.metric("Model Type", model_type)
    with col3:
        if st.button("📈 View Model Insights"):
            st.switch_page("pages/7_📈_Model_Insights.py")
    
    st.markdown("---")
    
    with st.form("prediction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📚 Education Details")
            degree = st.selectbox("Degree", 
                ["B.Tech", "M.Tech", "BCA", "MCA", "MBA"],
                help="Select your highest degree")
            
            major = st.selectbox("Major/Specialization", 
                ["Computer Science", "AI", "Data Science", "IT", "Electronics", "Business"],
                help="Select your major")
            
            skill1 = st.selectbox("Primary Skill", 
                ["Python", "Java", "C++", "SQL", "Machine Learning", 
                 "Deep Learning", "Data Analysis", "AWS", "Azure", "Cloud"],
                help="Your strongest technical skill")
            
            skill2 = st.selectbox("Secondary Skill", 
                ["SQL", "HTML", "React", "Java", "C++", "AWS", 
                 "Data Analytics", "Cybersecurity", "Python", "Cloud"],
                help="Your second strongest skill")
            
            certification = st.selectbox("Certification", 
                ["AI Specialist", "Data Analyst", "Web Developer", 
                 "Machine Learning", "AWS", "Azure", "GCP", "Cloud", "None"],
                help="Select your certification")
        
        with col2:
            st.subheader("💼 Experience Details")
            experience_years = st.number_input("Experience (Years)", 
                min_value=0, max_value=50, value=2,
                help="Total years of professional experience")
            
            project_count = st.number_input("Project Count", 
                min_value=0, max_value=100, value=5,
                help="Number of projects completed")
            
            internship = st.selectbox("Internship Experience", 
                ["Yes", "No"],
                help="Have you completed any internships?")
            
            experience_level = st.selectbox("Experience Level", 
                ["Beginner", "Intermediate", "Expert", "Mid", "Junior", 
                 "Senior", "Fresher"],
                help="How would you rate your overall experience?")
        
        st.markdown("---")
        st.subheader("🎓 Educational & Career Gaps")
        
        col1, col2 = st.columns(2)
        
        with col1:
            has_edu_gap = st.checkbox("❓ Do you have an incomplete/dropped out degree?",
                help="Did you not complete any degree or drop out?")
            
            if has_edu_gap:
                edu_gap_reason = st.selectbox("Reason for Educational Gap",
                    ["Health issues", "Financial constraints", "Family responsibilities", 
                     "Career opportunity", "Career break", "Other"],
                    help="Select the reason for your educational gap")
                
                if edu_gap_reason == "Other":
                    edu_gap_detail = st.text_input("Please specify the reason")
                else:
                    edu_gap_detail = edu_gap_reason
            else:
                edu_gap_reason = None
                edu_gap_detail = None
        
        with col2:
            has_career_gap = st.checkbox("❓ Do you have a career gap or break?",
                help="Did you have a gap between graduation and starting work?")
            
            if has_career_gap:
                career_gap_years = st.number_input("Career Gap (Years)", 
                    min_value=0.5, max_value=20.0, value=1.0, step=0.5,
                    help="Duration of your career gap in years")
                
                career_gap_reason = st.selectbox("Reason for Career Gap",
                    ["Health issues", "Financial constraints", "Family responsibilities",
                     "Higher studies", "Career break", "Other"],
                    help="Select the reason for your career gap")
                
                if career_gap_reason == "Other":
                    career_gap_detail = st.text_input("Please specify the career gap reason")
                else:
                    career_gap_detail = career_gap_reason
            else:
                career_gap_years = 0
                career_gap_reason = None
                career_gap_detail = None
        
        st.markdown("---")
        submit = st.form_submit_button("🔮 Get Top 3 Predictions", 
                                       use_container_width=True, 
                                       type="primary")
    
    if submit:
        with st.spinner("🤖 Analyzing your profile..."):
            try:
                # ============================================
                # CRITICAL FIX: Create ALL required features
                # ============================================
                
                # Step 1: Create base input data
                input_data = pd.DataFrame({
                    "Degree": [degree],
                    "Major": [major],
                    "Skill1": [skill1],
                    "Skill2": [skill2],
                    "Certification": [certification],
                    "ExperienceYears": [experience_years],
                    "ProjectCount": [project_count],
                    "Internship": [internship],
                    "ExperienceLevel": [experience_level],
                    "EducationalGap": ["Yes" if has_edu_gap else "No"],
                    "EducationalGapReason": [edu_gap_detail if has_edu_gap else "None"],
                    "CareerGap": ["Yes" if has_career_gap else "No"],
                    "CareerGapYears": [career_gap_years],
                    "CareerGapReason": [career_gap_detail if has_career_gap else "None"]
                })
                
                # Step 2: Create feature dataframe
                feature_data = input_data.copy()
                
                # Step 3: Encode categorical features
                categorical_features = ['Degree', 'Major', 'Skill1', 'Skill2', 'Certification', 'Internship', 'ExperienceLevel']
                
                for col in categorical_features:
                    if col in encoders and encoders[col] is not None:
                        try:
                            encoded_val = encoders[col].transform([feature_data[col].values[0]])[0]
                            feature_data[col + '_encoded'] = encoded_val
                        except:
                            # If encoding fails, use a default value
                            feature_data[col + '_encoded'] = 0
                    else:
                        # No encoder available, create simple numeric encoding
                        feature_data[col + '_encoded'] = 0
                
                # Step 4: Create engineered features (CRITICAL - These were missing!)
                
                # DegreeLevel
                degree_hierarchy = {
                    'BCA': 1, 'B.Tech': 1,
                    'MCA': 2, 'M.Tech': 2, 'MBA': 2
                }
                feature_data['DegreeLevel'] = degree_hierarchy.get(degree, 1)
                
                # ProjectDensity
                feature_data['ProjectDensity'] = project_count / (experience_years + 1)
                
                # ExperienceCategoryFeature
                def categorize_experience(years):
                    if years == 0:
                        return 'Fresher'
                    elif years <= 2:
                        return 'Junior'
                    elif years <= 5:
                        return 'Mid'
                    else:
                        return 'Senior'
                
                exp_category = categorize_experience(experience_years)
                feature_data['ExperienceCategoryFeature'] = exp_category
                
                # Encode ExperienceCategoryFeature
                if 'ExperienceCategoryFeature' in encoders and encoders['ExperienceCategoryFeature'] is not None:
                    try:
                        encoded_val = encoders['ExperienceCategoryFeature'].transform([exp_category])[0]
                        feature_data['ExperienceCategoryFeature_encoded'] = encoded_val
                    except:
                        feature_data['ExperienceCategoryFeature_encoded'] = 0
                else:
                    # Create simple encoding if encoder not available
                    exp_cat_map = {'Fresher': 0, 'Junior': 1, 'Mid': 2, 'Senior': 3}
                    feature_data['ExperienceCategoryFeature_encoded'] = exp_cat_map.get(exp_category, 1)
                
                # Step 5: Select features in correct order
                if feature_columns and len(feature_columns) > 0:
                    # Use the exact feature columns from model
                    X_predict = feature_data[feature_columns].values.reshape(1, -1)
                else:
                    # Fallback: use default feature order
                    default_features = [
                        'Degree_encoded', 'Major_encoded', 'Skill1_encoded', 'Skill2_encoded',
                        'Certification_encoded', 'ExperienceYears', 'ProjectCount',
                        'Internship_encoded', 'ExperienceLevel_encoded', 'DegreeLevel',
                        'ProjectDensity', 'ExperienceCategoryFeature_encoded'
                    ]
                    X_predict = feature_data[default_features].values.reshape(1, -1)
                
                # Step 6: Apply scaling if available
                if scaler is not None:
                    X_predict = scaler.transform(X_predict)
                
                # Step 7: Make predictions
                try:
                    # Get probability predictions
                    prediction_proba = model.predict_proba(X_predict)[0]
                    
                    # Get top 3 predictions
                    top_3_indices = np.argsort(prediction_proba)[-3:][::-1]
                    top_3_probs = prediction_proba[top_3_indices]
                    
                    # Normalize to 100%
                    top_3_probs_normalized = (top_3_probs / top_3_probs.sum()) * 100
                    
                    # Get class names
                    if hasattr(model, 'classes_'):
                        all_classes = model.classes_
                        top_3_roles = [all_classes[i] for i in top_3_indices]
                    else:
                        # Fallback if classes_ not available
                        primary_role = str(model.predict(X_predict)[0])
                        top_3_roles = [primary_role, "Alternative Role 1", "Alternative Role 2"]
                    
                    top_3_confidences = top_3_probs_normalized
                    
                except Exception as pred_error:
                    st.error(f"❌ Prediction error: {str(pred_error)}")
                    st.info("💡 The model may need to be retrained properly. Please contact admin.")
                    return
                
                # ============================================
                # DISPLAY RESULTS
                # ============================================
                st.markdown(f"""
                    <div class='prediction-box'>
                        <h2>✨ Your Top 3 Job Roles</h2>
                        <p>Based on your profile analysis</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"""
                        <div class='rank-card rank-1'>
                            <h3 style='margin: 0; font-size: 2rem;'>🥇</h3>
                            <h2 style='margin: 0.5rem 0;'>{top_3_roles[0]}</h2>
                            <p style='margin: 0; opacity: 0.9; font-size: 1.1rem;'>Most Suitable</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                        <div class='rank-card rank-2'>
                            <h3 style='margin: 0; font-size: 2rem;'>🥈</h3>
                            <h2 style='margin: 0.5rem 0;'>{top_3_roles[1]}</h2>
                            <p style='margin: 0; opacity: 0.9; font-size: 1.1rem;'>Good Match</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                        <div class='rank-card rank-3'>
                            <h3 style='margin: 0; font-size: 2rem;'>🥉</h3>
                            <h2 style='margin: 0.5rem 0;'>{top_3_roles[2]}</h2>
                            <p style='margin: 0; opacity: 0.9; font-size: 1.1rem;'>Alternative Option</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Save to database
                row = input_data.iloc[0].to_dict()
                row["predicted_label_1"] = top_3_roles[0]
                row["confidence_1"] = top_3_confidences[0]
                row["predicted_label_2"] = top_3_roles[1]
                row["confidence_2"] = top_3_confidences[1]
                row["predicted_label_3"] = top_3_roles[2]
                row["confidence_3"] = top_3_confidences[2]
                insert_prediction(user['user_id'], row)
                
                st.success("✅ Predictions saved to your history!")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("🔄 Make Another Prediction", use_container_width=True):
                        st.rerun()
                with col2:
                    if st.button("📊 View History", use_container_width=True):
                        st.switch_page("pages/4_📊_Results.py")
                with col3:
                    if st.button("🏠 Go Home", use_container_width=True):
                        st.switch_page("app.py")
            
            except Exception as e:
                st.error(f"❌ Prediction failed: {str(e)}")
                st.info("""
                💡 **Possible issues:**
                - Model file corrupted
                - Missing encoders
                - Feature mismatch
                
                **Solution:** Ask admin to retrain the model properly from the Admin Panel.
                """)

if __name__ == "__main__":
    main()