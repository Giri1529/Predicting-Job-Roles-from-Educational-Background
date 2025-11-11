# pages/9_🎓_Skill_Gap.py
# Skill Gap Analysis and Career Development

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from auth_helper import require_auth, get_current_user
from db_helper import fetch_history
from global_css import GLOBAL_CSS

st.set_page_config(page_title="Skill Gap Analysis - SmartLand", page_icon="🎓", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

@require_auth
def main():
    user = get_current_user()
    
    st.title("🎓 Skill Gap Analysis")
    st.markdown("Identify skill gaps and create your personalized development roadmap")
    
    # Fetch user predictions
    predictions = fetch_history(user['user_id'], limit=100)
    
    if not predictions:
        st.warning("📭 Make a prediction first to analyze your skill gaps!")
        if st.button("🎯 Make a Prediction"):
            st.switch_page("pages/3_🎯_Prediction.py")
        st.stop()
    
    # Convert to DataFrame
    df = pd.DataFrame(predictions, columns=[
        'id', 'user_id', 'timestamp', 'degree', 'major', 'skill1', 'skill2',
        'certification', 'experience_years', 'project_count', 'internship',
        'experience_level', 'predicted_label', 'confidence'
    ])
    
    # Get latest prediction
    latest = df.iloc[0]
    predicted_role = latest['predicted_label']
    
    st.markdown(f"### 📊 Analysis for: **{predicted_role}**")
    
    # ============================================
    # ROLE-SPECIFIC SKILL REQUIREMENTS
    # ============================================
    role_skills = {
        'Data Scientist': {
            'required': ['Python', 'SQL', 'Machine Learning', 'Statistics', 'Data Analysis'],
            'nice_to_have': ['Deep Learning', 'Spark', 'Tableau'],
            'certifications': ['AI Specialist', 'Data Analyst', 'Machine Learning'],
            'experience': '2-3 years',
            'description': 'Analyze data and build predictive models'
        },
        'ML Engineer': {
            'required': ['Python', 'Machine Learning', 'Deep Learning', 'TensorFlow', 'SQL'],
            'nice_to_have': ['Kubernetes', 'MLOps', 'Cloud'],
            'certifications': ['Machine Learning', 'AI Specialist', 'AWS'],
            'experience': '3-5 years',
            'description': 'Build and deploy machine learning systems'
        },
        'Software Developer': {
            'required': ['Java', 'Python', 'C++', 'SQL', 'Git'],
            'nice_to_have': ['React', 'Docker', 'Cloud'],
            'certifications': ['Web Developer', 'Cloud'],
            'experience': '1-3 years',
            'description': 'Develop and maintain software applications'
        },
        'Data Analyst': {
            'required': ['SQL', 'Python', 'Data Analysis', 'Tableau', 'Excel'],
            'nice_to_have': ['Power BI', 'Looker', 'Statistics'],
            'certifications': ['Data Analyst', 'Cloud'],
            'experience': '1-2 years',
            'description': 'Transform data into actionable insights'
        },
        'Security Analyst': {
            'required': ['Cybersecurity', 'SQL', 'Python', 'Networking', 'Linux'],
            'nice_to_have': ['Penetration Testing', 'Forensics', 'Cloud Security'],
            'certifications': ['Cybersecurity', 'AWS', 'Azure'],
            'experience': '2-4 years',
            'description': 'Protect systems and networks from threats'
        },
        'Business Analyst': {
            'required': ['SQL', 'Data Analysis', 'Excel', 'Communication', 'Python'],
            'nice_to_have': ['Tableau', 'Power BI', 'Project Management'],
            'certifications': ['Data Analyst', 'Cloud'],
            'experience': '2-3 years',
            'description': 'Bridge business and technology gap'
        }
    }
    
    # Get requirements for predicted role or use default
    if predicted_role in role_skills:
        requirements = role_skills[predicted_role]
    else:
        requirements = {
            'required': ['Python', 'SQL', 'Communication', 'Problem Solving'],
            'nice_to_have': ['Cloud', 'Machine Learning', 'Data Analysis'],
            'certifications': ['AI Specialist', 'Data Analyst', 'AWS'],
            'experience': '2-3 years',
            'description': 'Professional in technology'
        }
    
    # ============================================
    # DISPLAY ROLE INFO
    # ============================================
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        ### 📌 {predicted_role}
        
        **Description:** {requirements['description']}
        
        **Recommended Experience:** {requirements['experience']}
        """)
    
    with col2:
        st.markdown(f"""
        **Your Current Profile:**
        - 🎓 Degree: {latest['degree']}
        - 📚 Major: {latest['major']}
        - 💼 Experience: {latest['experience_years']} years
        - 📊 Projects: {latest['project_count']}
        - 📜 Certification: {latest['certification']}
        """)
    
    st.markdown("---")
    
    # ============================================
    # SKILL GAP ANALYSIS
    # ============================================
    st.markdown("### 🎯 Skill Gap Analysis")
    
    current_skills = [latest['skill1'], latest['skill2']]
    required_skills = requirements['required']
    nice_to_have = requirements['nice_to_have']
    
    # Create skill matrix
    skill_matrix = []
    for skill in required_skills:
        status = '✅ Have' if skill in current_skills else '❌ Missing'
        skill_matrix.append({'Skill': skill, 'Status': status, 'Priority': 'High'})
    
    for skill in nice_to_have:
        status = '✅ Have' if skill in current_skills else '⭕ Nice-to-have'
        skill_matrix.append({'Skill': skill, 'Status': status, 'Priority': 'Medium'})
    
    skill_df = pd.DataFrame(skill_matrix)
    st.dataframe(skill_df, use_container_width=True, hide_index=True)
    
    # Calculate skill match percentage
    have_required = sum(1 for s in required_skills if s in current_skills)
    skill_match = (have_required / len(required_skills)) * 100
    
    st.markdown("---")
    
    # ============================================
    # SKILL MATCH VISUALIZATION
    # ============================================
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Skill Match Score")
        
        # Create gauge chart
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=skill_match,
            domain={'x': [0, 100], 'y': [0, 100]},
            title={'text': "Skill Match %"},
            delta={'reference': 80},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 40], 'color': "#ffcccc"},
                    {'range': [40, 70], 'color': "#ffffcc"},
                    {'range': [70, 100], 'color': "#ccffcc"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        fig_gauge.update_layout(height=400)
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    with col2:
        st.markdown("### 📈 Skills Breakdown")
        
        skills_summary = {
            'Category': ['Required Skills\nYou Have', 'Required Skills\nMissing', 'Nice-to-have'],
            'Count': [
                have_required,
                len(required_skills) - have_required,
                sum(1 for s in nice_to_have if s in current_skills)
            ],
            'Color': ['#90EE90', '#FF6B6B', '#FFE66D']
        }
        
        fig_summary = go.Figure(go.Bar(
            x=skills_summary['Category'],
            y=skills_summary['Count'],
            marker_color=skills_summary['Color'],
            text=skills_summary['Count'],
            textposition='auto'
        ))
        fig_summary.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_summary, use_container_width=True)
    
    st.markdown("---")
    
    # ============================================
    # DEVELOPMENT ROADMAP
    # ============================================
    st.markdown("### 🚀 Your Learning Roadmap")
    
    missing_skills = [s for s in required_skills if s not in current_skills]
    
    if missing_skills:
        st.markdown("#### 🔴 Priority Skills to Learn")
        for i, skill in enumerate(missing_skills[:5], 1):
            col1, col2 = st.columns([1, 3])
            with col1:
                st.markdown(f"**{i}. {skill}**")
            with col2:
                # Learning resources
                resources = {
                    'Python': '📚 Udemy, Codecademy, DataCamp',
                    'SQL': '📚 Mode Analytics, W3Schools, Leetcode',
                    'Machine Learning': '📚 Andrew Ng Course, Kaggle, Fast.ai',
                    'Deep Learning': '📚 TensorFlow Tutorials, PyTorch Docs',
                    'Data Analysis': '📚 Pandas Docs, DataCamp, Analytics Vidhya',
                    'Java': '📚 Oracle Tutorials, LeetCode, HackerRank',
                    'C++': '📚 GeeksforGeeks, Codeforces',
                    'AWS': '📚 AWS Academy, A Cloud Guru',
                    'Azure': '📚 Microsoft Learn, Pluralsight',
                    'Docker': '📚 Official Docs, Play with Docker',
                    'Cybersecurity': '📚 Coursera, SANS Institute'
                }
                resource = resources.get(skill, '📚 Udemy, Coursera')
                st.caption(f"Resources: {resource}")
    else:
        st.success("✅ You have all required skills! Consider learning nice-to-have skills.")
    
    st.markdown("---")
    
    # ============================================
    # RECOMMENDATIONS
    # ============================================
    st.markdown("### 💡 Personalized Recommendations")
    
    recommendations = []
    
    # Experience recommendation
    if latest['experience_years'] < 2:
        recommendations.append("🎯 Build more hands-on projects (target: 10+ projects)")
    else:
        recommendations.append("✅ Your experience level is good")
    
    # Certification recommendation
    if latest['certification'] == 'None':
        rec_cert = requirements['certifications'][0]
        recommendations.append(f"📜 Get certified: **{rec_cert}** certification")
    else:
        recommendations.append(f"✅ Good! You have: {latest['certification']}")
    
    # Internship recommendation
    if latest['internship'] == 'No' and latest['experience_years'] < 1:
        recommendations.append("🏢 Consider internship for practical experience")
    else:
        recommendations.append("✅ Good internship/project experience")
    
    # Skill diversification
    if latest['skill1'] == latest['skill2']:
        recommendations.append("🛠️ Diversify your skills - learn a different technology")
    else:
        recommendations.append("✅ Good skill diversification")
    
    for i, rec in enumerate(recommendations, 1):
        st.markdown(f"{i}. {rec}")
    
    st.markdown("---")
    
    # ============================================
    # QUICK ACTIONS
    # ============================================
    st.markdown("### ⚡ Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Update Profile", use_container_width=True):
            st.switch_page("pages/3_🎯_Prediction.py")
    
    with col2:
        if st.button("📊 View Analytics", use_container_width=True):
            st.switch_page("pages/8_📊_Analytics.py")
    
    with col3:
        if st.button("🏠 Go Home", use_container_width=True):
            st.switch_page("app.py")

if __name__ == "__main__":
    main()