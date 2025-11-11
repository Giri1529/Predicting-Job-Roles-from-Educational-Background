# File name: global_css.py
# Location: Put this file in your project root (same folder as app.py)

GLOBAL_CSS = """
<style>
/* ============================================
   GLOBAL ANIMATIONS
   ============================================ */

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}

@keyframes glow {
    0%, 100% { box-shadow: 0 0 20px rgba(102, 126, 234, 0.3); }
    50% { box-shadow: 0 0 40px rgba(102, 126, 234, 0.6); }
}

@keyframes slideInLeft {
    from { opacity: 0; transform: translateX(-50px); }
    to { opacity: 1; transform: translateX(0); }
}

@keyframes slideInRight {
    from { opacity: 0; transform: translateX(50px); }
    to { opacity: 1; transform: translateX(0); }
}

@keyframes slideInUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes slideInDown {
    from { opacity: 0; transform: translateY(-20px); }
    to { opacity: 1; transform: translateY(0); }
}

/* ============================================
   HERO SECTION
   ============================================ */

.hero-section {
    background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #667eea);
    background-size: 400% 400%;
    animation: gradientShift 15s ease infinite;
    padding: 4rem 2rem;
    border-radius: 25px;
    color: white;
    text-align: center;
    margin-bottom: 3rem;
    position: relative;
    overflow: hidden;
    border: 2px solid rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
}

.hero-section h1 {
    font-size: 3.5rem !important;
    font-weight: 900 !important;
    text-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    margin: 0;
    animation: float 3s ease-in-out infinite;
}

.hero-section h3 {
    font-size: 1.5rem !important;
    font-weight: 300 !important;
    letter-spacing: 2px;
    opacity: 0.95;
    margin-top: 1rem;
}

/* ============================================
   METRIC CARDS
   ============================================ */

.metric-card {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
    backdrop-filter: blur(10px);
    border: 2px solid rgba(102, 126, 234, 0.3);
    padding: 2rem;
    border-radius: 20px;
    color: white;
    text-align: center;
    margin: 1rem 0;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
    cursor: pointer;
}

.metric-card:hover {
    transform: translateY(-8px) scale(1.02);
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.2), rgba(118, 75, 162, 0.2));
    border-color: rgba(240, 147, 251, 0.6);
    animation: glow 2s ease-in-out infinite;
}

.metric-card h2 {
    color: #00d4ff !important;
    font-size: 2.5rem !important;
    margin: 0 0 0.5rem 0;
}

.metric-card p {
    font-size: 1rem;
    opacity: 0.9;
    margin: 0;
}

/* ============================================
   INFO BOXES
   ============================================ */

.info-box {
    background: linear-gradient(135deg, rgba(240, 243, 246, 0.1), rgba(226, 232, 240, 0.1));
    backdrop-filter: blur(10px);
    padding: 2rem;
    border-radius: 20px;
    margin: 1.5rem 0;
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: all 0.3s ease;
}

.info-box:hover {
    border-color: rgba(102, 126, 234, 0.3);
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.05), rgba(118, 75, 162, 0.05));
}

.info-box h3 {
    color: #667eea !important;
    font-size: 1.5rem !important;
    font-weight: 700 !important;
    margin-bottom: 1rem;
}

.info-box h4 {
    color: #667eea !important;
    font-size: 1.3rem !important;
    font-weight: 600 !important;
}

.info-box ul {
    list-style: none;
    padding: 0;
}

.info-box li {
    padding: 0.5rem 0;
    color: #718096;
}

.info-box li:before {
    content: '✨ ';
    margin-right: 0.75rem;
    font-size: 1rem;
}

/* ============================================
   FEATURE GRID
   ============================================ */

.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}

.feature-item {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.08), rgba(118, 75, 162, 0.08));
    border: 1px solid rgba(102, 126, 234, 0.2);
    padding: 2rem;
    border-radius: 20px;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.feature-item:hover {
    transform: translateY(-10px);
    border-color: rgba(240, 147, 251, 0.4);
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.12), rgba(118, 75, 162, 0.12));
}

.feature-item h4 {
    color: #667eea !important;
    font-size: 1.3rem !important;
    font-weight: 700 !important;
    margin: 0 0 1rem 0;
}

.feature-item p {
    color: #718096;
    line-height: 1.6;
    margin: 0;
    font-size: 0.95rem;
}

/* ============================================
   FORM ELEMENTS
   ============================================ */

.form-card {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.08), rgba(118, 75, 162, 0.08));
    border: 1px solid rgba(240, 147, 251, 0.2);
    border-radius: 20px;
    padding: 2rem;
    backdrop-filter: blur(10px);
    margin-bottom: 1.5rem;
}

/* ============================================
   PREDICTION RESULTS
   ============================================ */

.prediction-box {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 3rem 2rem;
    border-radius: 25px;
    color: white;
    text-align: center;
    margin: 2rem 0;
    position: relative;
    overflow: hidden;
    border: 2px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
    animation: slideInDown 0.6s ease-out;
}

.prediction-box h2 {
    color: white !important;
    font-size: 2rem !important;
    margin-bottom: 1rem;
}

.prediction-box h1 {
    color: white !important;
    font-size: 3.5rem !important;
    margin: 1rem 0;
    text-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

/* ============================================
   CONFIDENCE BAR
   ============================================ */

.confidence-bar {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 15px;
    overflow: hidden;
    height: 35px;
    margin: 1rem 0;
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.confidence-fill {
    background: linear-gradient(90deg, #00d4ff, #667eea);
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: bold;
    font-size: 1rem;
    transition: width 0.5s ease;
}

/* ============================================
   INSIGHT BOX
   ============================================ */

.insight-box {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.05));
    border-left: 4px solid #667eea;
    padding: 1.5rem;
    margin: 1.5rem 0;
    border-radius: 12px;
}

.insight-box h4 {
    color: #667eea !important;
    font-size: 1.2rem !important;
    margin: 0 0 1rem 0;
}

/* ============================================
   SKILL ITEMS
   ============================================ */

.skill-item {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(102, 126, 234, 0.2);
    border-radius: 12px;
    padding: 1rem;
    margin-bottom: 0.75rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: all 0.3s ease;
}

.skill-item:hover {
    background: rgba(102, 126, 234, 0.12);
    border-color: rgba(240, 147, 251, 0.3);
    transform: translateX(5px);
}

.skill-have {
    color: #10b981;
    font-weight: 600;
}

.skill-missing {
    color: #ef4444;
    font-weight: 600;
}

/* ============================================
   FILTER CHIPS
   ============================================ */

.filter-chip {
    background: rgba(102, 126, 234, 0.2);
    border: 1px solid rgba(102, 126, 234, 0.3);
    border-radius: 20px;
    padding: 0.5rem 1rem;
    cursor: pointer;
    transition: all 0.2s ease;
    display: inline-block;
    margin-right: 0.5rem;
    margin-bottom: 0.5rem;
}

.filter-chip:hover {
    background: rgba(102, 126, 234, 0.3);
    border-color: rgba(240, 147, 251, 0.4);
}

/* ============================================
   RESULT CARDS
   ============================================ */

.result-card {
    background: rgba(102, 126, 234, 0.1);
    border: 1px solid rgba(102, 126, 234, 0.2);
    border-radius: 15px;
    padding: 1.5rem;
    transition: all 0.3s ease;
    margin-bottom: 1rem;
}

.result-card:hover {
    transform: translateX(5px);
    border-color: rgba(240, 147, 251, 0.4);
    background: rgba(102, 126, 234, 0.15);
}

/* ============================================
   PROFILE
   ============================================ */

.profile-header {
    display: flex;
    align-items: center;
    margin-bottom: 2rem;
    padding: 1.5rem;
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.08), rgba(118, 75, 162, 0.08));
    border-radius: 20px;
}

.profile-avatar {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    background: linear-gradient(135deg, #667eea, #764ba2);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2.5rem;
    margin-right: 1.5rem;
    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
}

.profile-section {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.08), rgba(118, 75, 162, 0.08));
    border: 1px solid rgba(102, 126, 234, 0.2);
    border-radius: 20px;
    padding: 2rem;
    margin-bottom: 1.5rem;
}

/* ============================================
   ADMIN ELEMENTS
   ============================================ */

.admin-stat-card {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
    border: 1px solid rgba(240, 147, 251, 0.2);
    border-radius: 15px;
    padding: 1.5rem;
    transition: all 0.3s ease;
}

.admin-stat-card:hover {
    transform: translateY(-5px);
    border-color: rgba(240, 147, 251, 0.4);
}

/* ============================================
   ANALYTICS
   ============================================ */

.analytics-header {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
    border-left: 4px solid #667eea;
    padding: 1.5rem;
    border-radius: 10px;
    margin-bottom: 1.5rem;
}

.tab-content {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(102, 126, 234, 0.1);
    border-radius: 15px;
    padding: 1.5rem;
    animation: slideInUp 0.4s ease-out;
}

/* ============================================
   BUTTONS
   ============================================ */

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    box-shadow: 0 10px 25px rgba(102, 126, 234, 0.2) !important;
    transition: all 0.3s ease !important;
}

.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4) !important;
}

/* ============================================
   ROADMAP
   ============================================ */

.roadmap-section {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), transparent);
    border-left: 4px solid #10b981;
    padding: 1.5rem;
    border-radius: 10px;
    margin-top: 2rem;
}

.recommendation-card {
    background: rgba(102, 126, 234, 0.1);
    border-left: 3px solid #667eea;
    padding: 1rem;
    margin-bottom: 1rem;
    border-radius: 8px;
}

/* ============================================
   DIVIDER
   ============================================ */

.premium-divider {
    height: 2px;
    background: linear-gradient(90deg, transparent, #667eea, #764ba2, transparent);
    margin: 3rem 0;
}

/* ============================================
   RESPONSIVE
   ============================================ */

@media (max-width: 768px) {
    .hero-section h1 {
        font-size: 2.5rem !important;
    }
    
    .profile-header {
        flex-direction: column;
    }
    
    .profile-avatar {
        margin-right: 0;
        margin-bottom: 1rem;
    }
}

</style>
"""