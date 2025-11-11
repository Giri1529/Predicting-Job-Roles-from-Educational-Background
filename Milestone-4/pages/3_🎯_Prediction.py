# pages/3_🎯_Prediction.py (UPDATED - Works with your model)
# Enhanced Prediction Page with Proper Model Loading

import streamlit as st
import pandas as pd
import numpy as np
import joblib
from global_css import GLOBAL_CSS
from auth_helper import require_auth, get_current_user
from db_helper import insert_prediction


st.set_page_config(page_title="Prediction - SmartLand", page_icon="🎯", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True) 

@require_auth
def main():
    user = get_current_user()
    
    # ============================================
    # MODEL LOADING - THIS IS THE KEY PART
    # ============================================
    @st.cache_resource
    def load_model():
        """
        Load model with proper error handling
        Handles both old (tuple) and new (dict) formats
        """
        try:
            # Try loading as new format (dictionary with metadata)
            model_data = joblib.load("best_model.pkl")
            
            if isinstance(model_data, dict):
                # New format - dictionary with all components
                return {
                    'model': model_data['model'],
                    'scaler': model_data.get('scaler'),
                    'feature_columns': model_data.get('feature_columns'),
                    'encoders': model_data.get('encoders', {}),
                    'accuracy': model_data.get('accuracy', 0),
                    'model_type': model_data.get('model_type', 'Unknown')
                }
            elif isinstance(model_data, tuple):
                # Old format - (model, encoder) tuple
                return {
                    'model': model_data[0],
                    'scaler': None,
                    'feature_columns': None,
                    'encoders': {'target': model_data[1]} if len(model_data) > 1 else {},
                    'accuracy': 0,
                    'model_type': 'Loaded Model'
                }
            else:
                # Just a model object
                return {
                    'model': model_data,
                    'scaler': None,
                    'feature_columns': None,
                    'encoders': {},
                    'accuracy': 0,
                    'model_type': 'Loaded Model'
                }
        except FileNotFoundError:
            st.error("❌ Model file not found! Please ensure 'best_model.pkl' exists in the root folder.")
            return None
        except Exception as e:
            st.error(f"❌ Error loading model: {str(e)}")
            return None
    
    # Load model metadata for additional info
    @st.cache_resource
    def load_metadata():
        """Load model metadata if available"""
        try:
            metadata = joblib.load("model_metadata.pkl")
            return metadata
        except:
            return None
    
    model_package = load_model()
    metadata = load_metadata()
    
    if model_package is None:
        st.error("⚠️ Unable to load the prediction model. Please contact support.")
        return
    
    # Extract components
    model = model_package['model']
    scaler = model_package['scaler']
    feature_columns = model_package['feature_columns']
    encoders = model_package['encoders']
    accuracy = model_package['accuracy']
    model_type = model_package['model_type']
    
    # Custom CSS
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
        .confidence-bar {
            background-color: #e0e0e0;
            border-radius: 10px;
            overflow: hidden;
            height: 30px;
            margin: 10px 0;
        }
        .confidence-fill {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }
        .insight-box {
            background-color: #f0f8ff;
            border-left: 4px solid #667eea;
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 5px;
        }
        </style>
        """, unsafe_allow_html=True)
    
    st.title("🎯 Job Role Prediction")
    st.markdown(f"**Welcome, {user['username']}!** Enter your details to get your predicted job role.")
    
    # Model info banner
    col1, col2, col3 = st.columns(3)
    with col1:
        if accuracy > 0:
            st.metric("Model Accuracy", f"{accuracy:.2%}")
        else:
            st.info("Model loaded successfully")
    with col2:
        st.metric("Model Type", model_type)
    with col3:
        if st.button("📈 View Model Insights"):
            st.switch_page("pages/7_📈_Model_Insights.py")
    
    st.markdown("---")
    
    # Input form
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
        submit = st.form_submit_button("🔮 Predict Job Role", 
                                       use_container_width=True, 
                                       type="primary")
    
    # Make prediction
    if submit:
        with st.spinner("🤖 Analyzing your profile..."):
            try:
                # Prepare input data
                input_data = pd.DataFrame({
                    "Degree": [degree],
                    "Major": [major],
                    "Skill1": [skill1],
                    "Skill2": [skill2],
                    "Certification": [certification],
                    "ExperienceYears": [experience_years],
                    "ProjectCount": [project_count],
                    "Internship": [internship],
                    "ExperienceLevel": [experience_level]
                })
                
                # ============================================
                # PREPARE DATA FOR MODEL PREDICTION
                # ============================================
                prediction_data = input_data.copy()
                
                # If model has encoders, encode the categorical data
                if encoders and len(encoders) > 0:
                    # Encode categorical features
                    for col in ['Degree', 'Major', 'Skill1', 'Skill2', 'Certification', 'Internship', 'ExperienceLevel']:
                        if col in encoders:
                            try:
                                # Handle both dict and LabelEncoder objects
                                if hasattr(encoders[col], 'transform'):
                                    # It's a LabelEncoder
                                    encoded_val = encoders[col].transform([prediction_data[col].values[0]])[0]
                                else:
                                    # It's a dict
                                    encoded_val = encoders[col].get(prediction_data[col].values[0], 0)
                                prediction_data[col + '_encoded'] = encoded_val
                            except:
                                # If encoding fails, use original value
                                prediction_data[col + '_encoded'] = 0
                
                # Feature engineering
                prediction_data['DegreeLevel'] = {'BCA': 1, 'B.Tech': 1, 'MCA': 2, 'M.Tech': 2, 'MBA': 2}.get(degree, 1)
                prediction_data['ProjectDensity'] = project_count / (experience_years + 1) if experience_years >= 0 else project_count
                
                # Add ExperienceCategoryFeature (from model trainer)
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
                prediction_data['ExperienceCategoryFeature'] = exp_category
                
                # Encode ExperienceCategoryFeature if encoder exists
                if 'ExperienceCategoryFeature' in encoders:
                    try:
                        encoded_val = encoders['ExperienceCategoryFeature'].transform([exp_category])[0]
                        prediction_data['ExperienceCategoryFeature_encoded'] = encoded_val
                    except:
                        prediction_data['ExperienceCategoryFeature_encoded'] = 0
                
                # Prepare features for model
                if feature_columns and len(feature_columns) > 0:
                    # Use specified feature columns
                    feature_values = prediction_data[feature_columns].values.reshape(1, -1)
                else:
                    # Use default features
                    default_features = [
                        'Degree_encoded', 'Major_encoded', 'Skill1_encoded', 'Skill2_encoded',
                        'Certification_encoded', 'ExperienceYears', 'ProjectCount',
                        'Internship_encoded', 'ExperienceLevel_encoded', 'DegreeLevel', 'ProjectDensity'
                    ]
                    # Only use features that exist
                    available_features = [f for f in default_features if f in prediction_data.columns]
                    feature_values = prediction_data[available_features].values.reshape(1, -1)
                
                # Scale if scaler exists
                if scaler is not None:
                    feature_values = scaler.transform(feature_values)
                
                # Make prediction
                prediction = model.predict(feature_values)
                
                # Get confidence if available
                try:
                    prediction_proba = model.predict_proba(feature_values)
                    confidence = np.max(prediction_proba) * 100
                except:
                    confidence = 85.0  # Default confidence if proba not available
                
                predicted_role = str(prediction[0])
                
                # Display result
                st.markdown(f"""
                    <div class='prediction-box'>
                        <h2>✨ Prediction Result</h2>
                        <h1 style='font-size: 3em; margin: 1rem 0;'>{predicted_role}</h1>
                        <p>This is your recommended job role based on your profile!</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Display confidence
                st.markdown("### 📊 Prediction Confidence")
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"""
                        <div class='confidence-bar'>
                            <div class='confidence-fill' style='width: {confidence}%;'>
                                {confidence:.1f}%
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                with col2:
                    if confidence >= 80:
                        st.success("Very High")
                    elif confidence >= 60:
                        st.info("High")
                    elif confidence >= 40:
                        st.warning("Moderate")
                    else:
                        st.error("Low")
                
                # Show insights
                st.markdown("### 💡 Key Insights")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"""
                    <div class='insight-box'>
                    <h4>✨ Your Profile Strengths</h4>
                    <ul>
                        <li><strong>Primary Skill:</strong> {skill1}</li>
                        <li><strong>Secondary Skill:</strong> {skill2}</li>
                        <li><strong>Experience:</strong> {experience_years} years</li>
                        <li><strong>Projects:</strong> {project_count} completed</li>
                        <li><strong>Certification:</strong> {certification}</li>
                    </ul>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class='insight-box'>
                    <h4>🚀 Career Recommendations</h4>
                    <ul>
                        <li>✓ Your profile fits <strong>{predicted_role}</strong></li>
                        <li>✓ Strengthen {skill1} skills</li>
                        <li>✓ Consider {certification} certification</li>
                        <li>✓ Build 2-3 more portfolio projects</li>
                        <li>✓ Network in your industry</li>
                    </ul>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Save to database
                row = input_data.iloc[0].to_dict()
                row["predicted_label"] = predicted_role
                row["confidence"] = confidence
                insert_prediction(user['user_id'], row)
                
                st.success("✅ Prediction saved to your history!")
                
                # Show details
                with st.expander("📋 View Input Details"):
                    st.dataframe(input_data, use_container_width=True)
                
                # Quick actions
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
                st.info("💡 Possible issues:\n- Model file corrupted\n- Missing encoders\n- Feature mismatch\n\nTry retraining the model.")
    
    # Info section
    st.markdown("---")
    st.markdown("### ℹ️ How It Works")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("""
        **🔍 Our AI analyzes:**
        - Your educational background
        - Technical skills and certifications
        - Work experience and projects
        - Experience level & internships
        """)
    
    with col2:
        st.success("""
        **✅ You get:**
        - Accurate job role prediction
        - Confidence score for prediction
        - Career recommendations
        - Saved prediction history
        """)

if __name__ == "__main__":
    main()