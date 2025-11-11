# pages/8_📊_Analytics.py
# Analytics Dashboard with Visualizations

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from auth_helper import require_auth, get_current_user
from db_helper import fetch_history, get_user_prediction_count
from datetime import datetime, timedelta
from global_css import GLOBAL_CSS

st.set_page_config(page_title="Analytics - SmartLand", page_icon="📊", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

@require_auth
def main():
    user = get_current_user()
    
    st.title("📊 Analytics Dashboard")
    st.markdown(f"**Personalized Analytics for {user['username']}**")
    
    # Fetch user predictions
    predictions = fetch_history(user['user_id'], limit=1000)
    
    if not predictions:
        st.warning("📭 No predictions yet. Make your first prediction to see analytics!")
        if st.button("🎯 Make a Prediction"):
            st.switch_page("pages/3_🎯_Prediction.py")
        st.stop()
    
    # ✅ FIXED: Added 'confidence' column (14 columns total)
    df = pd.DataFrame(predictions, columns=[
        'id', 'user_id', 'timestamp', 'degree', 'major', 'skill1', 'skill2',
        'certification', 'experience_years', 'project_count', 'internship',
        'experience_level', 'predicted_label', 'confidence'
    ])
    
    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # ============================================
    # KEY METRICS
    # ============================================
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Predictions", len(df))
    
    with col2:
        st.metric("Unique Job Roles", df['predicted_label'].nunique())
    
    with col3:
        avg_exp = df['experience_years'].mean()
        st.metric("Avg Experience", f"{avg_exp:.1f} years")
    
    with col4:
        avg_projects = df['project_count'].mean()
        st.metric("Avg Projects", f"{avg_projects:.1f}")
    
    st.markdown("---")
    
    # ============================================
    # TABS FOR DIFFERENT ANALYSES
    # ============================================
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Trends", "🎯 Predictions", "🛠️ Skills", "🎓 Education", "📥 Export"
    ])
    
    # Tab 1: Trends
    with tab1:
        st.markdown("### 📈 Prediction Trends Over Time")
        
        # Predictions over time
        daily_counts = df.groupby(df['timestamp'].dt.date).size().reset_index(name='count')
        daily_counts['timestamp'] = pd.to_datetime(daily_counts['timestamp'])
        
        fig_trend = px.line(daily_counts, x='timestamp', y='count',
                           title='Predictions Over Time',
                           labels={'timestamp': 'Date', 'count': 'Number of Predictions'},
                           markers=True)
        fig_trend.update_layout(hovermode='x unified', height=400)
        st.plotly_chart(fig_trend, use_container_width=True)
        
        # Experience progression
        st.markdown("#### 💼 Experience Progression")
        exp_data = df[['timestamp', 'experience_years']].sort_values('timestamp')
        
        fig_exp = go.Figure()
        fig_exp.add_trace(go.Scatter(
            x=exp_data['timestamp'],
            y=exp_data['experience_years'],
            mode='lines+markers',
            fill='tozeroy',
            name='Experience (Years)'
        ))
        fig_exp.update_layout(
            title='Your Experience Growth',
            xaxis_title='Date',
            yaxis_title='Years of Experience',
            height=350,
            hovermode='x unified'
        )
        st.plotly_chart(fig_exp, use_container_width=True)
    
    # Tab 2: Predictions Distribution
    with tab2:
        st.markdown("### 🎯 Job Role Distribution")
        
        role_counts = df['predicted_label'].value_counts().reset_index()
        role_counts.columns = ['Role', 'Count']
        
        fig_roles = px.bar(role_counts, x='Role', y='Count',
                          title='Predicted Job Roles',
                          labels={'Count': 'Number of Predictions'},
                          color='Count',
                          color_continuous_scale='Viridis')
        fig_roles.update_layout(height=400)
        st.plotly_chart(fig_roles, use_container_width=True)
        
        # Most common role
        most_common = df['predicted_label'].value_counts().index[0]
        st.success(f"🏆 Your most predicted role: **{most_common}**")
        
        # Role statistics table
        st.markdown("#### 📊 Role Statistics")
        st.dataframe(role_counts, use_container_width=True)
    
    # Tab 3: Skills Analysis
    with tab3:
        st.markdown("### 🛠️ Skills Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Primary Skills")
            skill1_counts = df['skill1'].value_counts().reset_index()
            skill1_counts.columns = ['Skill', 'Count']
            
            fig_skill1 = px.pie(skill1_counts, values='Count', names='Skill',
                               title='Primary Skills Distribution')
            st.plotly_chart(fig_skill1, use_container_width=True)
        
        with col2:
            st.markdown("#### Secondary Skills")
            skill2_counts = df['skill2'].value_counts().reset_index()
            skill2_counts.columns = ['Skill', 'Count']
            
            fig_skill2 = px.pie(skill2_counts, values='Count', names='Skill',
                               title='Secondary Skills Distribution')
            st.plotly_chart(fig_skill2, use_container_width=True)
        
        # Certifications
        st.markdown("#### 📜 Certifications")
        cert_counts = df['certification'].value_counts().reset_index()
        cert_counts.columns = ['Certification', 'Count']
        
        fig_cert = px.bar(cert_counts, y='Certification', x='Count',
                         orientation='h',
                         title='Certifications Distribution',
                         color='Count',
                         color_continuous_scale='Blues')
        fig_cert.update_layout(height=300)
        st.plotly_chart(fig_cert, use_container_width=True)
    
    # Tab 4: Education Analysis
    with tab4:
        st.markdown("### 🎓 Education Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Degree Distribution")
            degree_counts = df['degree'].value_counts().reset_index()
            degree_counts.columns = ['Degree', 'Count']
            
            fig_degree = px.pie(degree_counts, values='Count', names='Degree',
                               title='Degrees')
            st.plotly_chart(fig_degree, use_container_width=True)
        
        with col2:
            st.markdown("#### Major Distribution")
            major_counts = df['major'].value_counts().reset_index()
            major_counts.columns = ['Major', 'Count']
            
            fig_major = px.pie(major_counts, values='Count', names='Major',
                              title='Majors')
            st.plotly_chart(fig_major, use_container_width=True)
        
        # Experience Level Distribution
        st.markdown("#### 📊 Experience Level")
        exp_level_counts = df['experience_level'].value_counts().reset_index()
        exp_level_counts.columns = ['Level', 'Count']
        
        fig_exp_level = px.bar(exp_level_counts, x='Level', y='Count',
                              title='Experience Level Distribution',
                              color='Count',
                              color_continuous_scale='Greens')
        fig_exp_level.update_layout(height=300)
        st.plotly_chart(fig_exp_level, use_container_width=True)
    
    # Tab 5: Export
    with tab5:
        st.markdown("### 📥 Export Your Data")
        
        # Prepare export data
        export_df = df.copy()
        export_df['timestamp'] = export_df['timestamp'].astype(str)
        
        # CSV Export
        csv_data = export_df.to_csv(index=False)
        st.download_button(
            label="📥 Download as CSV",
            data=csv_data,
            file_name=f"predictions_{user['username']}_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        st.markdown("---")
        
        # Summary Statistics
        st.markdown("### 📊 Summary Statistics")
        
        summary_stats = {
            'Metric': [
                'Total Predictions',
                'Date Range',
                'Average Experience',
                'Average Projects',
                'Internship Count',
                'Most Common Role',
                'Most Used Skill'
            ],
            'Value': [
                len(df),
                f"{df['timestamp'].min().date()} to {df['timestamp'].max().date()}",
                f"{df['experience_years'].mean():.2f} years",
                f"{df['project_count'].mean():.2f}",
                df[df['internship'] == 'Yes'].shape[0],
                df['predicted_label'].value_counts().index[0],
                df['skill1'].value_counts().index[0]
            ]
        }
        
        summary_df = pd.DataFrame(summary_stats)
        st.dataframe(summary_df, use_container_width=True, hide_index=True)
        
        # Download Summary
        summary_csv = summary_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Summary as CSV",
            data=summary_csv,
            file_name=f"summary_{user['username']}_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )

if __name__ == "__main__":
    main()