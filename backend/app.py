from flask import Flask, request, jsonify, render_template
import os
import json
from datetime import datetime
import traceback
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
app.config['UPLOAD_FOLDER'] = '../frontend/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Create upload directory
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Mock classes for testing (replace with actual imports when ready)
class MockResumeParser:
    def parse_resume(self, filepath):
        return {
            'text': 'Sample resume text with skills like python, sql, machine learning',
            'sections': {'experience': '5 years at Tech Company', 'education': 'BS in Computer Science'},
            'personal_info': {'name': 'John Doe', 'email': 'john@email.com', 'phone': '123-456-7890'},
            'experience': [{'dates': '2020-2024', 'description': 'Software Engineer at Tech Co'}],
            'education': [{'degree': 'BS', 'institution': 'University'}]
        }

class MockSkillExtractor:
    def extract_skills(self, text):
        return {
            'skills': ['python', 'sql', 'machine learning', 'aws', 'docker'],
            'experience_years': 5,
            'certifications': ['AWS Certified'],
            'projects': [{'title': 'ML Project', 'technologies': ['python', 'scikit-learn']}]
        }

class MockScoringEngine:
    def calculate_score(self, resume_data, job_description):
        return {
            'overall_score': 85,
            'category_scores': {
                'skills': 90,
                'experience': 80,
                'education': 85,
                'projects_certifications': 75
            },
            'breakdown': 'Strong skills match, good experience',
            'matched_skills': ['python', 'sql'],
            'missing_skills': ['kubernetes']
        }

class MockRAGEngine:
    def get_suggestions(self, resume_data, job_description):
        return {
            'text_improvements': ['Add more quantifiable achievements', 'Use stronger action verbs'],
            'missing_skills': ['kubernetes', 'terraform'],
            'formatting_suggestions': ['Improve section organization'],
            'role_specific_advice': ['Focus on cloud technologies'],
            'rag_personalized': ['Consider adding more project details']
        }

class MockAssociationMiner:
    def get_recommendations(self, skills, experience):
        return {
            'frequent_combinations': [{'skills': ['python', 'sql', 'pandas'], 'frequency': 0.8}],
            'suggested_skills': [
                {'based_on': ['python', 'sql'], 'recommend': ['pandas', 'numpy'], 'confidence': 0.85, 'support': 0.7}
            ],
            'role_based_suggestions': {'inferred_role': 'data_scientist', 'commonly_missing': ['docker', 'aws']}
        }

class MockJobMatcher:
    def analyze_match(self, resume_data, job_description):
        return {
            'overall_match': 78,
            'strengths': ['Strong Python skills', 'Relevant experience'],
            'gaps': ['Missing cloud experience', 'Need more leadership examples'],
            'keyword_analysis': {
                'total_keywords': 20,
                'present_keywords': 15,
                'missing_keywords': ['kubernetes', 'terraform'],
                'coverage_percentage': 75
            },
            'section_analysis': {
                'experience': {'present': True, 'completeness': 'Good', 'word_count': 150},
                'education': {'present': True, 'completeness': 'Good', 'word_count': 100}
            },
            'improvement_suggestions': ['Add missing keywords', 'Expand experience section']
        }

class MockVisualizationEngine:
    def generate_visualizations(self, resume_data, score_results, job_analysis):
        # Return mock visualization data
        skill_gap_data = {
            'data': [
                {
                    'type': 'bar',
                    'x': [1, 1, 1, 1, 1],
                    'y': ['Python', 'SQL', 'AWS', 'Docker', 'Kubernetes'],
                    'orientation': 'h',
                    'name': 'Skills Required',
                    'marker': {'color': '#ff7f0e', 'opacity': 0.3}
                },
                {
                    'type': 'bar',
                    'x': [1, 1, 1, 0, 0],
                    'y': ['Python', 'SQL', 'AWS', 'Docker', 'Kubernetes'],
                    'orientation': 'h',
                    'name': 'Skills Present',
                    'marker': {'color': '#1f77b4'}
                }
            ],
            'layout': {
                'title': 'Skill Gap Analysis',
                'barmode': 'overlay',
                'height': 400
            }
        }
        
        score_radar_data = {
            'data': [{
                'type': 'scatterpolar',
                'r': [90, 80, 85, 75, 90],
                'theta': ['Skills', 'Experience', 'Education', 'Projects', 'Overall'],
                'fill': 'toself',
                'name': 'Score Breakdown'
            }],
            'layout': {
                'polar': {'radialaxis': {'visible': True, 'range': [0, 100]}},
                'showlegend': False,
                'height': 400
            }
        }
        
        return {
            'skill_gap_chart': json.dumps(skill_gap_data),
            'score_breakdown_chart': json.dumps(score_radar_data)
        }

# Initialize mock components
resume_parser = MockResumeParser()
skill_extractor = MockSkillExtractor()
scoring_engine = MockScoringEngine()
rag_engine = MockRAGEngine()
association_miner = MockAssociationMiner()
job_matcher = MockJobMatcher()
viz_engine = MockVisualizationEngine()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Server is running properly',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    """Main endpoint for resume analysis"""
    try:
        logger.info("Analyze endpoint called")
        
        # Check if file was uploaded
        if 'resume' not in request.files:
            return jsonify({'error': 'No resume file provided'}), 400
        
        file = request.files['resume']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Validate file type
        allowed_extensions = {'pdf', 'docx', 'txt'}
        file_extension = file.filename.lower().split('.')[-1] if '.' in file.filename else ''
        if file_extension not in allowed_extensions:
            return jsonify({'error': f'Unsupported file type: {file_extension}. Please upload PDF, DOCX, or TXT.'}), 400
        
        # Save file
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        logger.info(f"File saved: {filename}")
        
        # Get job description
        job_description = request.form.get('job_description', '')
        
        # Process resume with mock data
        parsed_data = resume_parser.parse_resume(filepath)
        skills_data = skill_extractor.extract_skills(parsed_data['text'])
        parsed_data.update(skills_data)
        
        # Generate scores and analysis
        score_results = scoring_engine.calculate_score(parsed_data, job_description)
        rag_suggestions = rag_engine.get_suggestions(parsed_data, job_description)
        association_recs = association_miner.get_recommendations(skills_data['skills'], parsed_data.get('experience', []))
        job_analysis = job_matcher.analyze_match(parsed_data, job_description)
        visualizations = viz_engine.generate_visualizations(parsed_data, score_results, job_analysis)
        
        # Compile results
        results = {
            'parsed_data': parsed_data,
            'score': score_results,
            'suggestions': {
                'rag': rag_suggestions,
                'association_rules': association_recs
            },
            'job_analysis': job_analysis,
            'visualizations': visualizations,
            'status': 'success',
            'message': 'Resume analyzed successfully'
        }
        
        logger.info("Analysis completed successfully")
        return jsonify(results)
        
    except Exception as e:
        error_msg = f"Error in analyze_resume: {str(e)}"
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        return jsonify({
            'error': error_msg,
            'status': 'error'
        }), 500

@app.route('/compare', methods=['POST'])
def compare_resumes():
    """Compare multiple resumes"""
    try:
        logger.info("Compare endpoint called")
        
        resumes = request.files.getlist('resumes')
        job_description = request.form.get('job_description', '')
        
        if len(resumes) < 2:
            return jsonify({'error': 'Please select at least 2 resumes for comparison'}), 400
        
        comparisons = []
        for resume in resumes:
            if resume.filename:
                # Validate file type
                file_extension = resume.filename.lower().split('.')[-1] if '.' in resume.filename else ''
                if file_extension not in {'pdf', 'docx', 'txt'}:
                    continue
                
                # Save file
                filename = f"compare_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{resume.filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                resume.save(filepath)
                
                # Process each resume
                parsed_data = resume_parser.parse_resume(filepath)
                skills_data = skill_extractor.extract_skills(parsed_data['text'])
                parsed_data.update(skills_data)
                
                score = scoring_engine.calculate_score(parsed_data, job_description)
                
                comparisons.append({
                    'filename': resume.filename,
                    'score': score['overall_score'],
                    'skills_match': score['category_scores']['skills'],
                    'experience_match': score['category_scores']['experience'],
                    'education_match': score['category_scores']['education'],
                    'summary': score['breakdown']
                })
        
        if not comparisons:
            return jsonify({'error': 'No valid resumes found for comparison'}), 400
        
        # Sort by score
        comparisons.sort(key=lambda x: x['score'], reverse=True)
        
        logger.info(f"Comparison completed for {len(comparisons)} resumes")
        return jsonify({
            'comparisons': comparisons,
            'status': 'success',
            'message': f'Compared {len(comparisons)} resumes successfully'
        })
        
    except Exception as e:
        error_msg = f"Error in compare_resumes: {str(e)}"
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        return jsonify({
            'error': error_msg,
            'status': 'error'
        }), 500

@app.route('/test')
def test_endpoint():
    """Test endpoint with sample data"""
    return jsonify({
        'message': 'Server is working!',
        'timestamp': datetime.now().isoformat(),
        'endpoints': {
            '/health': 'Server health check',
            '/analyze': 'Analyze a single resume',
            '/compare': 'Compare multiple resumes',
            '/test': 'This test endpoint'
        }
    })

if __name__ == '__main__':
    print("🚀 Starting Resume Analyzer Server...")
    print("📁 Upload folder:", app.config['UPLOAD_FOLDER'])
    print("📁 Template folder:", app.template_folder)
    print("📁 Static folder:", app.static_folder)
    print("🌐 Server will run on: http://localhost:5000")
    print("✅ Health check: http://localhost:5000/health")
    print("🧪 Test endpoint: http://localhost:5000/test")
    print("")
    print("📝 Available endpoints:")
    print("   POST /analyze   - Analyze a single resume")
    print("   POST /compare   - Compare multiple resumes") 
    print("   GET  /health    - Health check")
    print("   GET  /test      - Test endpoint")
    
    # Create necessary directories
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # 🔥 FIX: Disable debug mode to prevent automatic reloading
    app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)