import streamlit as st
import requests
import json
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime
import time
import base64
from streamlit_lottie import st_lottie
import json

# Page configuration with premium settings
st.set_page_config(
    page_title="ResumeVision AI | Smart Resume Analyzer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/your-repo',
        'Report a bug': "https://github.com/your-repo/issues",
        'About': "# ResumeVision AI - Next Generation Resume Analysis"
    }
)

# 🔥 PREMIUM CUSTOM CSS - Glass morphism, gradients, animations
st.markdown("""
<style>
    /* Main theme variables */
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --success-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --warning-gradient: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        --dark-gradient: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
        --glass-bg: rgba(255, 255, 255, 0.1);
        --glass-border: rgba(255, 255, 255, 0.2);
        --shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    /* Main header with animated gradient */
    .main-header {
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea, #764ba2, #f093fb, #f5576c);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 1rem;
        animation: gradientShift 6s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Glass morphism cards */
    .glass-card {
        background: var(--glass-bg);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: var(--shadow);
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.5);
    }
    
    /* Score cards with animated borders */
    .score-card {
        background: var(--primary-gradient);
        color: white;
        padding: 3rem 2rem;
        border-radius: 25px;
        text-align: center;
        margin: 1.5rem 0;
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        border: 2px solid transparent;
        animation: borderGlow 3s ease-in-out infinite alternate;
    }
    
    @keyframes borderGlow {
        from { border-color: rgba(255, 255, 255, 0.3); }
        to { border-color: rgba(255, 255, 255, 0.8); }
    }
    
    .score-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        transform: rotate(45deg);
        animation: shine 3s infinite;
    }
    
    @keyframes shine {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    /* Animated suggestion cards */
    .suggestion-card {
        background: var(--glass-bg);
        backdrop-filter: blur(10px);
        border-left: 6px solid;
        padding: 2rem;
        margin: 1.5rem 0;
        border-radius: 15px;
        transition: all 0.3s ease;
        animation: slideIn 0.6s ease-out;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    
    @keyframes slideIn {
        from { transform: translateX(-20px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    .suggestion-card.primary { border-left-color: #667eea; }
    .suggestion-card.success { border-left-color: #4facfe; }
    .suggestion-card.warning { border-left-color: #f5576c; }
    .suggestion-card.info { border-left-color: #43e97b; }
    
    .suggestion-card:hover {
        transform: translateX(10px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.15);
    }
    
    /* Comparison items with rank badges */
    .comparison-item {
        background: var(--glass-bg);
        backdrop-filter: blur(10px);
        padding: 2rem;
        margin: 1.5rem 0;
        border-radius: 20px;
        border-left: 6px solid #667eea;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .comparison-item::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--primary-gradient);
    }
    
    .rank-badge {
        position: absolute;
        top: 1rem;
        right: 1rem;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 1.2rem;
        color: white;
    }
    
    .rank-1 { background: linear-gradient(135deg, #FFD700, #FFA500); }
    .rank-2 { background: linear-gradient(135deg, #C0C0C0, #A9A9A9); }
    .rank-3 { background: linear-gradient(135deg, #CD7F32, #8B4513); }
    .rank-other { background: var(--dark-gradient); }
    
    /* Custom buttons */
    .stButton>button {
        background: var(--primary-gradient);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 50px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* File upload area styling */
    .upload-area {
        border: 3px dashed #667eea;
        border-radius: 20px;
        padding: 3rem;
        text-align: center;
        background: rgba(102, 126, 234, 0.05);
        transition: all 0.3s ease;
        margin: 1rem 0;
    }
    
    .upload-area:hover {
        background: rgba(102, 126, 234, 0.1);
        border-color: #764ba2;
    }
    
    /* Progress bars */
    .progress-container {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .progress-bar {
        height: 8px;
        background: var(--primary-gradient);
        border-radius: 10px;
        transition: width 0.5s ease;
    }
    
    /* Custom metrics */
    .custom-metric {
        background: var(--glass-bg);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        border: 1px solid var(--glass-border);
    }
    
    /* Sidebar enhancements */
    .css-1d391kg {
        background: var(--dark-gradient) !important;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: var(--glass-bg);
        backdrop-filter: blur(10px);
        border-radius: 15px 15px 0 0;
        padding: 1rem 2rem;
        border: 1px solid var(--glass-border);
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

class ResumeAnalyzerApp:
    def __init__(self):
        self.base_url = "http://localhost:5000"
        self.session = requests.Session()
        
    def check_server_health(self):
        """Check if the backend server is running"""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200, response.json() if response.status_code == 200 else None
        except requests.exceptions.RequestException as e:
            return False, None

    def analyze_resume(self, file, job_description=""):
        """Send resume for analysis to backend"""
        try:
            files = {'resume': file}
            data = {'job_description': job_description}
            
            response = self.session.post(
                f"{self.base_url}/analyze",
                files=files,
                data=data,
                timeout=30
            )
            
            if response.status_code == 200:
                return True, response.json()
            else:
                return False, f"Server error: {response.status_code} - {response.text}"
                
        except requests.exceptions.RequestException as e:
            return False, f"Connection error: {str(e)}"

    def compare_resumes(self, files, job_description=""):
        """Send multiple resumes for comparison"""
        try:
            files_list = [('resumes', file) for file in files]
            data = {'job_description': job_description}
            
            response = self.session.post(
                f"{self.base_url}/compare",
                files=files_list,
                data=data,
                timeout=30
            )
            
            if response.status_code == 200:
                return True, response.json()
            else:
                return False, f"Server error: {response.status_code} - {response.text}"
                
        except requests.exceptions.RequestException as e:
            return False, f"Connection error: {str(e)}"

def load_lottie_animation():
    """Load Lottie animation data"""
    return {
        "animation": "https://assets1.lottiefiles.com/packages/lf20_vybwn7df.json"
    }

def main():
    # Initialize the app
    app = ResumeAnalyzerApp()
    
    # 🌟 HERO SECTION
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<h1 class="main-header">ResumeVision AI</h1>', unsafe_allow_html=True)
        st.markdown("""
        <div style='text-align: center; margin-bottom: 3rem;'>
            <h3 style='color: #666; font-weight: 300;'>
            🤖 Next-Generation Resume Analysis Powered by Advanced AI & RAG Technology
            </h3>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # You can add a Lottie animation here if you install streamlit-lottie
        st.markdown("""
        <div style='text-align: center;'>
            <div style='font-size: 4rem; margin-bottom: 1rem;'>🚀</div>
            <div style='font-size: 0.9rem; color: #666;'>AI-Powered Insights</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 🔧 ENHANCED SIDEBAR
    with st.sidebar:
        st.markdown("""
        <div class='glass-card' style='text-align: center;'>
            <h3>🔮 ResumeVision AI</h3>
            <p>Smart Resume Analysis Platform</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Server Status with enhanced UI
        st.markdown("### 🖥️ System Status")
        server_healthy, health_data = app.check_server_health()
        
        status_card = st.container()
        with status_card:
            if server_healthy:
                st.success("""
                🟢 **Server Connected**  
                *Backend system is operational*
                """)
            else:
                st.error("""
                🔴 **Server Offline**  
                *Please start the backend server*
                """)
        
        # Quick Stats
        st.markdown("### 📊 Quick Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Analyses", "12", "+3")
        with col2:
            st.metric("Comparisons", "8", "+2")
        
        # Feature Highlights
        st.markdown("### ✨ Features")
        features = [
            "🎯 Smart Scoring Algorithm",
            "🤖 RAG-Powered Insights", 
            "📊 Interactive Visualizations",
            "🔍 Skill Gap Analysis",
            "🏆 Candidate Ranking",
            "💡 AI Recommendations"
        ]
        
        for feature in features:
            st.markdown(f"• {feature}")
        
        # Quick Actions
        st.markdown("### ⚡ Quick Actions")
        if st.button("🔄 Refresh Dashboard", use_container_width=True):
            st.rerun()
        
        if st.button("📋 View Sample Report", use_container_width=True):
            if 'analysis_result' not in st.session_state:
                st.session_state['analysis_result'] = get_sample_data()
    
    # 🎯 MAIN CONTENT TABS
    tab1, tab2, tab3 = st.tabs(["🔍 Analyze Resume", "⚖️ Compare Resumes", "📈 Insights Dashboard"])
    
    with tab1:
        render_analyze_tab(app)
    
    with tab2:
        render_compare_tab(app)
    
    with tab3:
        render_dashboard_tab()

def render_analyze_tab(app):
    """Render the enhanced resume analysis tab"""
    st.markdown("## 🔍 Deep Resume Analysis")
    st.markdown("*Upload a resume and let our AI provide comprehensive insights*")
    
    # Two-column layout with improved spacing
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Enhanced file upload area
        st.markdown("""
        <div class='upload-area'>
            <div style='font-size: 3rem; margin-bottom: 1rem;'>📄</div>
            <h3>Upload Your Resume</h3>
            <p>Drag & drop or click to browse files</p>
            <p style='color: #666; font-size: 0.9rem;'>Supported: PDF, DOCX, TXT</p>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            " ",
            type=["pdf", "docx", "txt"],
            help="Upload your resume for AI-powered analysis",
            label_visibility="collapsed"
        )
        
        # Job description with character counter
        st.markdown("### 🎯 Target Job Description")
        job_description = st.text_area(
            "Paste the job description for targeted analysis...",
            height=200,
            placeholder="Enter the job description to get personalized recommendations and score based on specific requirements...",
            help="Adding a job description enables targeted analysis and better matching"
        )
        
        if job_description:
            char_count = len(job_description)
            word_count = len(job_description.split())
            st.caption(f"📝 {char_count} characters • {word_count} words")
    
    with col2:
        # Analysis tips in glass card
        st.markdown("""
        <div class='glass-card'>
            <h4>💡 Pro Tips</h4>
            <p><strong>• Quality Matters:</strong> Use well-formatted resumes</p>
            <p><strong>• Be Specific:</strong> Include detailed job descriptions</p>
            <p><strong>• Recent Files:</strong> Upload updated resumes</p>
            <p><strong>• File Types:</strong> PDF works best for parsing</p>
        </div>
        """, unsafe_allow_html=True)
        
        # File info card
        if uploaded_file:
            file_size = len(uploaded_file.getvalue()) / 1024
            st.markdown(f"""
            <div class='suggestion-card success'>
                <h4>✅ File Ready</h4>
                <p><strong>Name:</strong> {uploaded_file.name}</p>
                <p><strong>Size:</strong> {file_size:.1f} KB</p>
                <p><strong>Type:</strong> {uploaded_file.type}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Analysis button with enhanced styling
    analyze_col1, analyze_col2, analyze_col3 = st.columns([1, 2, 1])
    with analyze_col2:
        if st.button("🚀 Launch AI Analysis", type="primary", use_container_width=True):
            if not uploaded_file:
                st.error("""
                ❌ Please upload a resume file to begin analysis.
                *Supported formats: PDF, DOCX, TXT*
                """)
                return
            
            # Progress animation
            with st.spinner("""
            🤖 **AI Analysis in Progress...**  
            *Parsing resume • Extracting skills • Generating insights • Creating visualizations*
            """):
                success, result = app.analyze_resume(uploaded_file, job_description)
                
                if success:
                    st.session_state['analysis_result'] = result
                    st.session_state['last_analysis_time'] = datetime.now()
                    st.balloons()
                    st.success("""
                    ✅ **Analysis Complete!**  
                    *Your resume has been successfully analyzed with AI-powered insights*
                    """)
                    st.rerun()
                else:
                    st.error(f"""
                    ❌ **Analysis Failed**  
                    *Error: {result}*
                    """)

def render_compare_tab(app):
    """Render the enhanced resume comparison tab"""
    st.markdown("## ⚖️ Multi-Resume Comparison")
    st.markdown("*Compare multiple candidates and identify the best fit*")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Multi-file upload
        st.markdown("### 📁 Upload Resumes")
        uploaded_files = st.file_uploader(
            "Select multiple resumes for comparison",
            type=["pdf", "docx", "txt"],
            accept_multiple_files=True,
            help="Choose 2 or more resumes to compare candidates"
        )
        
        # Comparison job description
        st.markdown("### 🎯 Comparison Criteria")
        compare_job_description = st.text_area(
            "Job description for comparison...",
            height=150,
            placeholder="Enter the target job description to compare candidates against specific requirements...",
            key="compare_jd"
        )
    
    with col2:
        # Comparison features
        st.markdown("""
        <div class='glass-card'>
            <h4>🏆 Comparison Features</h4>
            <p>• **Smart Ranking**: AI-powered candidate scoring</p>
            <p>• **Skill Analysis**: Technical competency comparison</p>
            <p>• **Experience Match**: Relevance to job requirements</p>
            <p>• **Gap Identification**: Areas for improvement</p>
            <p>• **Visual Reports**: Interactive comparison charts</p>
        </div>
        """, unsafe_allow_html=True)
        
        # File list with badges
        if uploaded_files:
            st.markdown(f"""
            <div class='suggestion-card info'>
                <h4>📋 Selected Files</h4>
                <p><strong>Total:</strong> {len(uploaded_files)} resumes</p>
            </div>
            """, unsafe_allow_html=True)
            
            for i, file in enumerate(uploaded_files[:3]):  # Show first 3
                file_size = len(file.getvalue()) / 1024
                st.write(f"• **{file.name}** ({file_size:.1f} KB)")
            
            if len(uploaded_files) > 3:
                st.write(f"*... and {len(uploaded_files) - 3} more*")
    
    # Comparison button
    if st.button("📊 Generate Comparison Report", type="primary", use_container_width=True):
        if not uploaded_files or len(uploaded_files) < 2:
            st.error("""
            ❌ Please upload at least 2 resumes for comparison.
            *Multiple files required for meaningful comparison*
            """)
            return
        
        with st.spinner("""
        🔄 **Comparing Resumes...**  
        *Analyzing multiple candidates • Calculating scores • Generating rankings • Creating reports*
        """):
            success, result = app.compare_resumes(uploaded_files, compare_job_description)
            
            if success:
                st.session_state['comparison_result'] = result
                st.session_state['last_comparison_time'] = datetime.now()
                st.success(f"""
                ✅ **Comparison Complete!**  
                *Successfully analyzed {len(result.get('comparisons', []))} resumes*
                """)
                st.rerun()
            else:
                st.error(f"""
                ❌ **Comparison Failed**  
                *Error: {result}*
                """)

def render_dashboard_tab():
    """Render the enhanced results dashboard"""
    st.markdown("## 📈 AI Insights Dashboard")
    st.markdown("*Comprehensive analysis results and interactive visualizations*")
    
    # Show analysis results if available
    if 'analysis_result' in st.session_state:
        display_enhanced_analysis_results(st.session_state['analysis_result'])
    
    # Show comparison results if available
    if 'comparison_result' in st.session_state:
        display_enhanced_comparison_results(st.session_state['comparison_result'])
    
    # Empty state with call to action
    if 'analysis_result' not in st.session_state and 'comparison_result' not in st.session_state:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div class='glass-card' style='text-align: center; padding: 4rem;'>
                <div style='font-size: 4rem; margin-bottom: 2rem;'>🔍</div>
                <h3>Ready for Insights?</h3>
                <p>Upload a resume for AI-powered analysis or compare multiple candidates to see detailed insights here.</p>
                <br>
                <p><strong>Get started with:</strong></p>
                <p>• Single resume analysis</p>
                <p>• Multi-candidate comparison</p>
                <p>• Skill gap identification</p>
                <p>• AI improvement suggestions</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Sample data toggle
        if st.button("🎭 View Sample Analysis", use_container_width=True):
            st.session_state['analysis_result'] = get_sample_data()
            st.rerun()

def display_enhanced_analysis_results(result):
    """Display enhanced analysis results with premium UI"""
    st.success("""
    🎉 **AI Analysis Complete!**  
    *Your resume has been thoroughly analyzed with advanced AI algorithms*
    """)
    
    if 'last_analysis_time' in st.session_state:
        st.caption(f"⏰ Analysis performed on: {st.session_state['last_analysis_time'].strftime('%B %d, %Y at %H:%M:%S')}")
    
    # 🌟 ENHANCED SCORE CARD
    score = result.get('score', {})
    overall_score = score.get('overall_score', 0)
    
    # Determine score color and message
    if overall_score >= 90:
        score_color = "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)"
        score_message = "Exceptional! 🏆"
    elif overall_score >= 75:
        score_color = "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)"
        score_message = "Strong Match! 👍"
    elif overall_score >= 60:
        score_color = "linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%)"
        score_message = "Good Potential 💪"
    else:
        score_color = "linear-gradient(135deg, #fd746c 0%, #ff9068 100%)"
        score_message = "Needs Improvement 📈"
    
    st.markdown(f"""
    <div class='score-card' style='background: {score_color}'>
        <h2 style='margin: 0; font-size: 4rem; font-weight: 800;'>{overall_score}%</h2>
        <p style='margin: 0; font-size: 1.5rem;'>{score_message}</p>
        <p style='margin: 0.5rem 0 0 0; opacity: 0.9;'>Overall Resume Score</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 📊 SCORE BREAKDOWN WITH CUSTOM METRICS
    st.markdown("### 📊 Detailed Score Breakdown")
    category_scores = score.get('category_scores', {})
    
    cols = st.columns(4)
    categories = [
        ('🛠️', 'Skills', category_scores.get('skills', 0)),
        ('💼', 'Experience', category_scores.get('experience', 0)),
        ('🎓', 'Education', category_scores.get('education', 0)),
        ('🚀', 'Projects', category_scores.get('projects_certifications', 0))
    ]
    
    for idx, (icon, name, score_val) in enumerate(categories):
        with cols[idx]:
            st.markdown(f"""
            <div class='custom-metric'>
                <div style='font-size: 2rem; margin-bottom: 0.5rem;'>{icon}</div>
                <h3 style='margin: 0;'>{score_val}%</h3>
                <p style='margin: 0; color: #666;'>{name}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # 🎯 ENHANCED TABS
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Deep Analysis", "💡 AI Suggestions", "📈 Visual Analytics", "🔍 Raw Insights"])
    
    with tab1:
        display_enhanced_detailed_analysis(result)
    
    with tab2:
        display_enhanced_suggestions(result)
    
    with tab3:
        display_enhanced_visualizations(result)
    
    with tab4:
        display_enhanced_raw_data(result)

def display_enhanced_detailed_analysis(result):
    """Display enhanced detailed analysis"""
    parsed_data = result.get('parsed_data', {})
    job_analysis = result.get('job_analysis', {})
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Personal Information in glass card
        st.markdown("### 👤 Personal Profile")
        personal_info = parsed_data.get('personal_info', {})
        
        st.markdown("""
        <div class='glass-card'>
        """, unsafe_allow_html=True)
        
        info_col1, info_col2 = st.columns(2)
        with info_col1:
            st.metric("👤 Name", personal_info.get('name', 'Not detected'))
            st.metric("📧 Email", personal_info.get('email', 'Not detected'))
        with info_col2:
            st.metric("📞 Phone", personal_info.get('phone', 'Not detected'))
            st.metric("📧 Alt Emails", len(personal_info.get('emails', [])))
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Skills with progress bars
        st.markdown("### 🛠️ Technical Skills")
        skills = parsed_data.get('skills', [])
        if skills:
            st.markdown(f"""
            <div class='glass-card'>
                <p><strong>Total Skills Detected:</strong> {len(skills)}</p>
                <div style='margin-top: 1rem;'>
            """, unsafe_allow_html=True)
            
            # Display skills in a nice format
            skill_groups = [skills[i:i+3] for i in range(0, len(skills), 3)]
            for group in skill_groups:
                st.write(" • " + " • ".join(group))
            
            st.markdown("</div></div>", unsafe_allow_html=True)
        else:
            st.info("No skills detected in the resume")
    
    with col2:
        # Job Match Analysis with enhanced cards
        st.markdown("### 🎯 Job Match Analysis")
        
        # Strengths
        strengths = job_analysis.get('strengths', [])
        if strengths:
            st.markdown('<div class="suggestion-card success">', unsafe_allow_html=True)
            st.markdown("### ✅ Key Strengths")
            for i, strength in enumerate(strengths, 1):
                st.write(f"{i}. {strength}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Areas for Improvement
        gaps = job_analysis.get('gaps', [])
        if gaps:
            st.markdown('<div class="suggestion-card warning">', unsafe_allow_html=True)
            st.markdown("### 📈 Improvement Areas")
            for i, gap in enumerate(gaps, 1):
                st.write(f"{i}. {gap}")
            st.markdown('</div>', unsafe_allow_html=True)

def display_enhanced_suggestions(result):
    """Display enhanced AI suggestions"""
    suggestions = result.get('suggestions', {})
    
    col1, col2 = st.columns(2)
    
    with col1:
        # RAG Suggestions
        rag_suggestions = suggestions.get('rag', {})
        
        st.markdown("### 🤖 AI-Powered Recommendations")
        
        text_improvements = rag_suggestions.get('text_improvements', [])
        if text_improvements:
            st.markdown('<div class="suggestion-card primary">', unsafe_allow_html=True)
            st.markdown("### ✍️ Writing Enhancements")
            for i, improvement in enumerate(text_improvements, 1):
                st.write(f"**{i}.** {improvement}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        missing_skills = rag_suggestions.get('missing_skills', [])
        if missing_skills:
            st.markdown('<div class="suggestion-card warning">', unsafe_allow_html=True)
            st.markdown("### 🎯 Recommended Skills")
            st.write("Consider adding these skills to improve your profile:")
            skill_cols = st.columns(2)
            for idx, skill in enumerate(missing_skills):
                with skill_cols[idx % 2]:
                    st.write(f"• {skill}")
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Association Rule Suggestions
        association_rules = suggestions.get('association_rules', {})
        
        st.markdown("### 🔗 Smart Skill Combinations")
        
        suggested_skills = association_rules.get('suggested_skills', [])
        if suggested_skills:
            for i, rule in enumerate(suggested_skills):
                confidence = rule.get('confidence', 0) * 100
                st.markdown(f"""
                <div class="suggestion-card info">
                    <h4>💡 Recommendation #{i+1}</h4>
                    <p><strong>Based on your skills in:</strong> {', '.join(rule.get('based_on', []))}</p>
                    <p><strong>Consider learning:</strong> {', '.join(rule.get('recommend', []))}</p>
                    <div class='progress-container'>
                        <div class='progress-bar' style='width: {confidence}%'></div>
                    </div>
                    <p><strong>AI Confidence:</strong> {confidence:.1f}%</p>
                </div>
                """, unsafe_allow_html=True)

def display_enhanced_visualizations(result):
    """Display enhanced visualizations"""
    visualizations = result.get('visualizations', {})
    
    if not visualizations:
        st.info("""
        📊 **Visualizations Coming Soon**  
        *Interactive charts and graphs will appear here for your analysis*
        """)
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'skill_gap_chart' in visualizations:
            try:
                chart_data = json.loads(visualizations['skill_gap_chart'])
                st.plotly_chart(chart_data, use_container_width=True)
            except:
                st.error("Could not display skill gap visualization")
        
        if 'score_breakdown_chart' in visualizations:
            try:
                chart_data = json.loads(visualizations['score_breakdown_chart'])
                st.plotly_chart(chart_data, use_container_width=True)
            except:
                st.error("Could not display score breakdown visualization")
    
    with col2:
        if 'keyword_match_chart' in visualizations:
            try:
                chart_data = json.loads(visualizations['keyword_match_chart'])
                st.plotly_chart(chart_data, use_container_width=True)
            except:
                st.error("Could not display keyword match visualization")

def display_enhanced_raw_data(result):
    """Display enhanced raw data view"""
    st.markdown("### 🔍 Raw Analysis Data")
    st.markdown("*Technical details and complete analysis output*")
    
    with st.expander("📋 View Complete Analysis Data", expanded=False):
        st.json(result)

def display_enhanced_comparison_results(result):
    """Display enhanced comparison results"""
    st.success("""
    🏆 **Comparison Analysis Complete!**  
    *Multiple candidates have been evaluated and ranked based on the job requirements*
    """)
    
    if 'last_comparison_time' in st.session_state:
        st.caption(f"⏰ Comparison performed on: {st.session_state['last_comparison_time'].strftime('%B %d, %Y at %H:%M:%S')}")
    
    comparisons = result.get('comparisons', [])
    
    if not comparisons:
        st.error("No comparison results available.")
        return
    
    # 🏅 CANDIDATE RANKING TABLE
    st.markdown("### 🏅 Candidate Ranking Summary")
    
    ranking_data = []
    for i, comparison in enumerate(comparisons):
        ranking_data.append({
            'Rank': i + 1,
            'Candidate': comparison['filename'],
            'Overall Score': f"{comparison['score']}%",
            'Skills': f"{comparison['skills_match']}%",
            'Experience': f"{comparison['experience_match']}%",
            'Education': f"{comparison.get('education_match', 0)}%"
        })
    
    df = pd.DataFrame(ranking_data)
    st.dataframe(df, use_container_width=True)
    
    # 📊 DETAILED COMPARISON CARDS
    st.markdown("### 📋 Detailed Candidate Analysis")
    
    for i, comparison in enumerate(comparisons):
        rank = i + 1
        medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"{rank}."
        
        st.markdown(f"""
        <div class='comparison-item'>
            <div class='rank-badge rank-{rank if rank <= 3 else "other"}'>
                {medal}
            </div>
            <h3>{comparison['filename']}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Metrics in columns
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🎯 Overall Score", f"{comparison['score']}%")
        with col2:
            st.metric("🛠️ Skills Match", f"{comparison['skills_match']}%")
        with col3:
            st.metric("💼 Experience", f"{comparison['experience_match']}%")
        with col4:
            st.metric("🎓 Education", f"{comparison.get('education_match', 0)}%")
        
        # Summary
        st.write(f"**📝 AI Summary:** {comparison.get('summary', 'No summary available')}")
        st.write("---")

def get_sample_data():
    """Get sample data for demonstration"""
    return {
        'score': {
            'overall_score': 87,
            'category_scores': {
                'skills': 92,
                'experience': 85,
                'education': 78,
                'projects_certifications': 82
            },
            'breakdown': 'Exceptional technical skills with strong project experience',
            'matched_skills': ['python', 'sql', 'aws', 'docker', 'machine learning'],
            'missing_skills': ['kubernetes', 'terraform', 'jenkins']
        },
        'parsed_data': {
            'personal_info': {
                'name': 'Alex Johnson',
                'email': 'alex.johnson@email.com',
                'phone': '+1-555-0123',
                'emails': ['alex.johnson@email.com'],
                'phones': ['+1-555-0123']
            },
            'skills': ['python', 'sql', 'machine learning', 'aws', 'docker', 'git', 'rest api', 'pandas', 'numpy'],
            'experience_years': 6,
            'experience': [
                {
                    'dates': '2019-2024',
                    'description': 'Senior Data Scientist at Tech Innovations Inc.'
                },
                {
                    'dates': '2017-2019', 
                    'description': 'Data Analyst at Data Systems Corp'
                }
            ]
        },
        'job_analysis': {
            'overall_match': 85,
            'strengths': [
                'Strong Python and machine learning expertise',
                'Relevant cloud experience with AWS',
                'Excellent years of industry experience',
                'Good project portfolio with measurable results'
            ],
            'gaps': [
                'Limited container orchestration knowledge',
                'Missing infrastructure as code experience',
                'Could benefit from more leadership examples'
            ],
            'keyword_analysis': {
                'total_keywords': 25,
                'present_keywords': ['python', 'sql', 'aws', 'machine learning', 'docker'],
                'missing_keywords': ['kubernetes', 'terraform', 'jenkins', 'ci/cd'],
                'coverage_percentage': 72
            }
        },
        'suggestions': {
            'rag': {
                'text_improvements': [
                    'Add quantifiable achievements with specific metrics',
                    'Use stronger action verbs in experience descriptions',
                    'Include project impact and business outcomes',
                    'Highlight leadership and collaboration experiences'
                ],
                'missing_skills': ['kubernetes', 'terraform', 'jenkins', 'ci/cd pipelines'],
                'formatting_suggestions': ['Improve section organization', 'Add a professional summary'],
                'role_specific_advice': ['Emphasize cloud architecture experience', 'Showcase end-to-end project ownership']
            },
            'association_rules': {
                'suggested_skills': [
                    {
                        'based_on': ['python', 'sql', 'aws'],
                        'recommend': ['pandas', 'numpy', 'scikit-learn'],
                        'confidence': 0.88,
                        'support': 0.75
                    },
                    {
                        'based_on': ['docker', 'aws'],
                        'recommend': ['kubernetes', 'terraform', 'jenkins'],
                        'confidence': 0.82,
                        'support': 0.68
                    }
                ]
            }
        }
    }

if __name__ == "__main__":
    main()