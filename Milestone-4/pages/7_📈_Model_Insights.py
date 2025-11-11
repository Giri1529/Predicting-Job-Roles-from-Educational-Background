# pages/7_📈_Model_Insights.py
# Model Explainability and Feature Importance

import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
import plotly.express as px
from global_css import GLOBAL_CSS

st.set_page_config(page_title="Model Insights - SmartLand", page_icon="📈", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

st.title("📈 Model Insights & Explainability")

# Load model package
@st.cache_resource
def load_model():
    try:
        return joblib.load("best_model.pkl")
    except:
        return None

model_package = load_model()

if model_package is None:
    st.error("❌ Unable to load model insights")
    st.stop()

# Extract model info
model = model_package['model']
accuracy = model_package['accuracy']
model_type = model_package['model_type']
feature_importance = model_package['feature_importance']

# Tabs for different insights
tab1, tab2, tab3, tab4 = st.tabs(["📊 Model Performance", "🔑 Feature Importance", "📈 Distribution", "ℹ️ About Model"])

# Tab 1: Model Performance
with tab1:
    st.markdown("### 🎯 Model Performance Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Model Accuracy", f"{accuracy:.2%}")
    
    with col2:
        st.metric("Model Type", model_type)
    
    with col3:
        st.metric("Features Used", len(model_package['feature_columns']))
    
    with col4:
        st.metric("Training Status", "✅ Ready")
    
    st.markdown("---")
    
    st.markdown("### 📋 What This Means")
    st.info(f"""
    **Model Accuracy: {accuracy:.2%}**
    
    This means that out of 100 predictions:
    - **Correct predictions:** {int(accuracy * 100)}
    - **Potential errors:** {100 - int(accuracy * 100)}
    
    A higher accuracy indicates the model is more reliable for job role predictions.
    """)

# Tab 2: Feature Importance
with tab2:
    st.markdown("### 🔑 Feature Importance Analysis")
    st.markdown("*Which factors matter most in predicting your job role?*")
    
    # Create visualization
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=feature_importance['Importance'],
        y=feature_importance['Feature'],
        orientation='h',
        marker=dict(
            color=feature_importance['Importance'],
            colorscale='Viridis',
            showscale=True
        ),
        hovertemplate='<b>%{y}</b><br>Importance: %{x:.4f}<extra></extra>'
    ))
    
    fig.update_layout(
        title="Feature Importance in Job Role Prediction",
        xaxis_title="Importance Score",
        yaxis_title="Features",
        height=500,
        template="plotly_white",
        showlegend=False,
        yaxis={'categoryorder': 'total ascending'}
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("### 📊 Top Features")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Most Important Features:**")
        for idx, row in feature_importance.head(5).iterrows():
            st.markdown(f"- **{row['Feature']}** ({row['Importance']:.4f})")
    
    with col2:
        st.markdown("**Insights:**")
        st.info("""
        - Experience years and level are critical factors
        - Skills directly impact job role prediction
        - Certifications add value to predictions
        - Education degree matters for role suitability
        """)

# Tab 3: Feature Distribution
with tab3:
    st.markdown("### 📈 Feature Distribution Analysis")
    
    st.markdown("**Understanding how features are distributed in the training data:**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Experience Features")
        exp_stats = {
            'Feature': ['Experience Years', 'Project Count', 'Project Density'],
            'Description': [
                'Total years of work experience',
                'Number of projects completed',
                'Projects per year of experience'
            ]
        }
        st.dataframe(pd.DataFrame(exp_stats), hide_index=True)
    
    with col2:
        st.markdown("#### Educational Features")
        edu_stats = {
            'Feature': ['Degree', 'Major', 'Certification'],
            'Impact': ['High', 'High', 'Medium']
        }
        st.dataframe(pd.DataFrame(edu_stats), hide_index=True)
    
    st.markdown("---")
    
    st.markdown("### 💡 How Features Interact")
    st.markdown("""
    The model learns how features work together:
    
    1. **Education + Experience** → Determines seniority level
    2. **Skills + Certification** → Defines specialization
    3. **Projects + Internship** → Shows practical capability
    4. **Experience Level + Major** → Predicts job role
    """)

# Tab 4: About Model
with tab4:
    st.markdown("### ℹ️ About This Model")
    
    st.markdown(f"""
    **Model Type:** {model_type}
    
    **Key Characteristics:**
    - Trained on real job market data
    - Considers educational background as primary factor
    - Incorporates work experience and skills
    - Uses advanced feature engineering
    - Optimized for high accuracy
    
    **What the Model Can Do:**
    ✅ Predict suitable job roles based on education
    ✅ Estimate career progression
    ✅ Identify skill-role alignment
    ✅ Provide confidence scores
    ✅ Handle diverse educational backgrounds
    
    **Limitations:**
    ⚠️ Works best with complete information
    ⚠️ Based on historical data patterns
    ⚠️ Doesn't account for personality factors
    ⚠️ May not predict new/emerging roles
    """)
    
    st.markdown("---")
    
    st.markdown("### 🔄 Model Training Details")
    
    training_info = pd.DataFrame({
        'Aspect': [
            'Algorithm',
            'Features Used',
            'Training Samples',
            'Test Accuracy',
            'Validation Method',
            'Hyperparameter Tuning'
        ],
        'Details': [
            model_type,
            ', '.join(model_package['feature_columns']),
            'Multiple Thousands',
            f'{accuracy:.2%}',
            'Train-Test Split (80-20)',
            'Optimized Parameters'
        ]
    })
    
    st.dataframe(training_info, hide_index=True, use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("### 📚 How to Use Model Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **For Better Predictions:**
        1. Provide accurate educational details
        2. Be honest about experience level
        3. List all relevant skills
        4. Include certifications
        5. Specify internship experience
        """)
    
    with col2:
        st.markdown("""
        **Understanding Results:**
        - Higher confidence = More reliable prediction
        - Multiple predictions help identify patterns
        - Compare predictions over time
        - Use insights for career planning
        - Track skill development
        """)

st.markdown("---")
st.caption("💡 Tip: Use these insights to understand what factors matter most for your career path!")