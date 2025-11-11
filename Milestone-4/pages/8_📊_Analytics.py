# pages/8_📊_Analytics.py (ENHANCED - Career Trajectory + AI Insights)
# Advanced Analytics with Trends and Predictions

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from auth_helper import require_auth, get_current_user, logout
from db_helper import fetch_history, get_user_prediction_count, get_role_progression, get_role_trends
from datetime import datetime, timedelta
from global_css import GLOBAL_CSS

st.set_page_config(page_title="Analytics - Edu2Job", page_icon="📊", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

@require_auth
def main():
    user = get_current_user()
    
    # LOGOUT BUTTON
    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button("🚪 Logout", type="secondary", use_container_width=True):
            logout()
    
    st.title("📊 Advanced Analytics Dashboard")
    st.markdown(f"**Career Intelligence for {user['username']}**")
    
    predictions = fetch_history(user['user_id'], limit=1000)
    
    if not predictions:
        st.warning("🔭 No predictions yet. Make your first prediction to see analytics!")
        if st.button("🎯 Make a Prediction"):
            st.switch_page("pages/3_🎯_Prediction.py")
        st.stop()
    
    # Enhanced DataFrame with TOP 3 predictions
    df = pd.DataFrame(predictions, columns=[
        'id', 'user_id', 'timestamp', 'degree', 'major', 'skill1', 'skill2',
        'certification', 'experience_years', 'project_count', 'internship',
        'experience_level', 
        'predicted_label_1', 'confidence_1',
        'predicted_label_2', 'confidence_2',
        'predicted_label_3', 'confidence_3',
        'educational_gap', 'educational_gap_reason',
        'career_gap', 'career_gap_years', 'career_gap_reason'
    ])
    
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Quick Stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Predictions", len(df))
    
    with col2:
        st.metric("Unique Job Roles", df['predicted_label_1'].nunique())
    
    with col3:
        avg_exp = df['experience_years'].mean()
        st.metric("Avg Experience", f"{avg_exp:.1f} years")
    
    with col4:
        avg_projects = df['project_count'].mean()
        st.metric("Avg Projects", f"{avg_projects:.1f}")
    
    st.markdown("---")
    
    # AI INSIGHTS SECTION
    st.markdown("### 🤖 AI-Powered Career Insights")
    
    # Get role trends
    role_trends = get_role_trends(user['user_id'])
    
    if role_trends and len(role_trends) > 0:
        trending_role = role_trends[0][0]
        trend_count = role_trends[0][1]
        
        # Calculate trend percentage
        trend_percentage = (trend_count / len(df)) * 100
        
        # AI Insight Box
        insight_msg = f"""
        📈 **Career Trajectory Insight:** Based on your last {len(df)} predictions, you're **strongly trending toward {trending_role}** roles ({trend_percentage:.1f}% of predictions).
        
        🎯 **Recommended Actions:**
        - Deep dive into {trending_role} specific skills
        - Build 2-3 portfolio projects focused on {trending_role}
        - Consider advanced certifications in this domain
        """
        
        st.info(insight_msg)
        
        # Show top 3 trending roles
        if len(role_trends) > 1:
            st.markdown("#### 🔥 Your Top Trending Roles")
            trend_df = pd.DataFrame(role_trends[:3], columns=['Role', 'Predictions'])
            
            fig_trends = px.bar(trend_df, x='Predictions', y='Role', orientation='h',
                               title='Your Most Predicted Roles',
                               color='Predictions',
                               color_continuous_scale='Blues')
            fig_trends.update_layout(height=300, showlegend=False)
            st.plotly_chart(fig_trends, use_container_width=True)
    else:
        st.info("🔄 Make more predictions to see AI-powered career insights!")
    
    st.markdown("---")
    
    # TABS
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📈 Career Trajectory", "🎯 Predictions", "🛠️ Skills", "🎓 Education", "📊 Gaps Analysis", "📥 Export"
    ])
    
    # ============================================
    # TAB 1: CAREER TRAJECTORY
    # ============================================
    with tab1:
        st.markdown("### 📈 Your Career Progression Over Time")
        
        # Get role progression data
        progression_data = get_role_progression(user['user_id'])
        
        if progression_data and len(progression_data) > 1:
            prog_df = pd.DataFrame(progression_data, columns=['timestamp', 'role', 'experience_years', 'experience_level'])
            prog_df['timestamp'] = pd.to_datetime(prog_df['timestamp'])
            
            # Career Level Mapping
            level_mapping = {
                'Fresher': 1,
                'Junior': 2,
                'Beginner': 2,
                'Intermediate': 3,
                'Mid': 4,
                'Expert': 5,
                'Senior': 6
            }
            
            prog_df['level_score'] = prog_df['experience_level'].map(level_mapping)
            
            # Plot career progression
            fig_career = go.Figure()
            
            fig_career.add_trace(go.Scatter(
                x=prog_df['timestamp'],
                y=prog_df['level_score'],
                mode='lines+markers',
                name='Career Level',
                line=dict(color='#667eea', width=3),
                marker=dict(size=10),
                hovertemplate='<b>%{text}</b><br>Date: %{x}<br>Level: %{y}<extra></extra>',
                text=prog_df['experience_level']
            ))
            
            fig_career.update_layout(
                title='Career Level Progression',
                xaxis_title='Timeline',
                yaxis_title='Career Level',
                height=400,
                yaxis=dict(
                    tickmode='array',
                    tickvals=[1, 2, 3, 4, 5, 6],
                    ticktext=['Fresher', 'Junior', 'Intermediate', 'Mid', 'Expert', 'Senior']
                ),
                hovermode='x unified'
            )
            
            st.plotly_chart(fig_career, use_container_width=True)
            
            # Experience Growth Chart
            st.markdown("#### 💼 Experience Growth")
            
            fig_exp = px.area(prog_df, x='timestamp', y='experience_years',
                             title='Years of Experience Over Time',
                             labels={'experience_years': 'Years', 'timestamp': 'Date'},
                             color_discrete_sequence=['#764ba2'])
            fig_exp.update_layout(height=350)
            st.plotly_chart(fig_exp, use_container_width=True)
            
            # Role Changes Timeline
            st.markdown("#### 🎯 Predicted Role Changes")
            
            role_changes = prog_df[['timestamp', 'role']].copy()
            role_changes['role_change'] = role_changes['role'] != role_changes['role'].shift(1)
            
            changes = role_changes[role_changes['role_change']].copy()
            
            if len(changes) > 1:
                st.markdown(f"**You've explored {len(changes)} different career paths:**")
                for idx, row in changes.iterrows():
                    st.markdown(f"- {row['timestamp'].strftime('%Y-%m-%d')}: **{row['role']}**")
            else:
                st.info("Your predictions have been consistent - great focus! 🎯")
        else:
            st.info("📊 Make more predictions over time to see your career trajectory!")
    
    # ============================================
    # TAB 2: PREDICTIONS
    # ============================================
    with tab2:
        st.markdown("### 🎯 Prediction History")
        
        daily_counts = df.groupby(df['timestamp'].dt.date).size().reset_index(name='count')
        daily_counts['timestamp'] = pd.to_datetime(daily_counts['timestamp'])
        
        fig_trend = px.line(daily_counts, x='timestamp', y='count',
                           title='Predictions Over Time',
                           labels={'timestamp': 'Date', 'count': 'Number of Predictions'},
                           markers=True)
        fig_trend.update_layout(hovermode='x unified', height=400)
        st.plotly_chart(fig_trend, use_container_width=True)
        
        st.markdown("#### 🏆 Top 3 Job Role Distribution")
        
        # Combine all top 3 predictions
        all_roles = pd.concat([
            df[['predicted_label_1']].rename(columns={'predicted_label_1': 'role'}),
            df[['predicted_label_2']].rename(columns={'predicted_label_2': 'role'}),
            df[['predicted_label_3']].rename(columns={'predicted_label_3': 'role'})
        ])
        
        role_counts = all_roles['role'].value_counts().reset_index()
        role_counts.columns = ['Role', 'Count']
        
        fig_roles = px.bar(role_counts.head(10), x='Role', y='Count',
                          title='Most Common Job Roles (All Predictions)',
                          labels={'Count': 'Number of Predictions'},
                          color='Count',
                          color_continuous_scale='Viridis')
        fig_roles.update_layout(height=400)
        st.plotly_chart(fig_roles, use_container_width=True)
    
    # ============================================
    # TAB 3: SKILLS
    # ============================================
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
        
        st.markdown("#### 📜 Certifications Trend")
        cert_counts = df['certification'].value_counts().reset_index()
        cert_counts.columns = ['Certification', 'Count']
        
        fig_cert = px.bar(cert_counts, y='Certification', x='Count',
                         orientation='h',
                         title='Certifications Distribution',
                         color='Count',
                         color_continuous_scale='Blues')
        fig_cert.update_layout(height=300)
        st.plotly_chart(fig_cert, use_container_width=True)
    
    # ============================================
    # TAB 4: EDUCATION
    # ============================================
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
    
    # ============================================
    # TAB 5: GAPS ANALYSIS
    # ============================================
    with tab5:
        st.markdown("### 📊 Educational & Career Gap Analysis")
        
        # Educational Gaps
        edu_gap_count = len(df[df['educational_gap'] == 'Yes'])
        career_gap_count = len(df[df['career_gap'] == 'Yes'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Educational Gaps", edu_gap_count)
            if edu_gap_count > 0:
                gap_reasons = df[df['educational_gap'] == 'Yes']['educational_gap_reason'].value_counts()
                st.markdown("**Reasons:**")
                for reason, count in gap_reasons.items():
                    st.markdown(f"- {reason}: {count}")
        
        with col2:
            st.metric("Career Gaps", career_gap_count)
            if career_gap_count > 0:
                gap_reasons = df[df['career_gap'] == 'Yes']['career_gap_reason'].value_counts()
                st.markdown("**Reasons:**")
                for reason, count in gap_reasons.items():
                    st.markdown(f"- {reason}: {count}")
        
        if career_gap_count > 0:
            avg_gap = df[df['career_gap'] == 'Yes']['career_gap_years'].mean()
            st.info(f"📊 Average career gap duration: **{avg_gap:.1f} years**")
    
    # ============================================
    # TAB 6: EXPORT
    # ============================================
    with tab6:
        st.markdown("### 📥 Export Your Data")
        
        export_df = df.copy()
        export_df['timestamp'] = export_df['timestamp'].astype(str)
        
        csv_data = export_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Full Data as CSV",
            data=csv_data,
            file_name=f"career_analytics_{user['username']}_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        st.markdown("---")
        
        st.markdown("### 📊 Summary Report")
        
        summary_stats = {
            'Metric': [
                'Total Predictions',
                'Date Range',
                'Average Experience',
                'Average Projects',
                'Most Common Role',
                'Career Trajectory',
                'Educational Gaps',
                'Career Gaps'
            ],
            'Value': [
                len(df),
                f"{df['timestamp'].min().date()} to {df['timestamp'].max().date()}",
                f"{df['experience_years'].mean():.2f} years",
                f"{df['project_count'].mean():.2f}",
                df['predicted_label_1'].value_counts().index[0],
                f"Trending toward {role_trends[0][0]}" if role_trends else "N/A",
                edu_gap_count,
                career_gap_count
            ]
        }
        
        summary_df = pd.DataFrame(summary_stats)
        st.dataframe(summary_df, use_container_width=True, hide_index=True)

if __name__ == "__main__":
    main()