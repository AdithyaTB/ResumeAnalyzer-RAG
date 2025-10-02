import json
import os
import re
from typing import Dict, List, Any
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import openai
from datetime import datetime

class RAGEngine:
    def __init__(self, knowledge_base_path: str = "knowledge_base/"):
        self.knowledge_base_path = knowledge_base_path
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = None
        self.knowledge_data = []
        
        # Initialize knowledge base
        self._initialize_knowledge_base()
        self._build_search_index()
    
    def _initialize_knowledge_base(self):
        """Initialize the resume best practices knowledge base"""
        best_practices = [
            {
                "category": "achievement_phrasing",
                "content": "Use action verbs and quantify achievements: 'Increased efficiency by 25% through process optimization'",
                "tags": ["achievements", "quantification", "action_verbs"]
            },
            {
                "category": "achievement_phrasing",
                "content": "Start bullet points with strong action verbs: Developed, Implemented, Led, Managed, Optimized",
                "tags": ["action_verbs", "bullet_points"]
            },
            {
                "category": "ats_optimization",
                "content": "Include relevant keywords from job description to pass Applicant Tracking Systems",
                "tags": ["ats", "keywords", "optimization"]
            },
            {
                "category": "ats_optimization",
                "content": "Use standard section headings: Experience, Education, Skills, Projects",
                "tags": ["ats", "formatting", "sections"]
            },
            {
                "category": "technical_skills",
                "content": "Group technical skills by category: Programming Languages, Frameworks, Tools",
                "tags": ["skills", "organization", "technical"]
            },
            {
                "category": "experience_description",
                "content": "Follow STAR method: Situation, Task, Action, Result for experience descriptions",
                "tags": ["star", "experience", "storytelling"]
            },
            {
                "category": "role_specific",
                "content": "Data Science roles should emphasize: Python, SQL, Machine Learning, Data Visualization",
                "tags": ["data_science", "skills", "technical"]
            },
            {
                "category": "role_specific",
                "content": "Software Engineering roles should emphasize: Algorithms, System Design, Code Quality",
                "tags": ["software_engineering", "skills", "technical"]
            },
            {
                "category": "formatting",
                "content": "Keep resume to 1-2 pages maximum, use consistent formatting and fonts",
                "tags": ["formatting", "length", "design"]
            }
        ]
        
        # Save knowledge base
        os.makedirs(self.knowledge_base_path, exist_ok=True)
        with open(os.path.join(self.knowledge_base_path, "best_practices.json"), "w") as f:
            json.dump(best_practices, f, indent=2)
        
        self.knowledge_data = best_practices
    
    def _build_search_index(self):
        """Build FAISS index for efficient similarity search"""
        if not self.knowledge_data:
            return
        
        # Encode all knowledge base content
        texts = [item["content"] + " " + " ".join(item["tags"]) for item in self.knowledge_data]
        embeddings = self.model.encode(texts)
        
        # Create FAISS index
        self.index = faiss.IndexFlatIP(embeddings.shape[1])
        self.index.add(embeddings.astype('float32'))
    
    def get_suggestions(self, resume_data: Dict, job_description: str = "") -> Dict[str, Any]:
        """Get RAG-based suggestions for resume improvement"""
        suggestions = {
            "text_improvements": [],
            "missing_skills": [],
            "formatting_suggestions": [],
            "role_specific_advice": []
        }
        
        # Analyze resume text for improvements
        suggestions["text_improvements"] = self._analyze_text_improvements(resume_data)
        
        # Suggest missing skills based on job description
        if job_description:
            suggestions["missing_skills"] = self._suggest_missing_skills(resume_data, job_description)
        
        # Formatting suggestions
        suggestions["formatting_suggestions"] = self._get_formatting_suggestions(resume_data)
        
        # Role-specific advice
        suggestions["role_specific_advice"] = self._get_role_specific_advice(resume_data, job_description)
        
        # RAG-based personalized suggestions
        rag_suggestions = self._get_rag_based_suggestions(resume_data, job_description)
        suggestions["rag_personalized"] = rag_suggestions
        
        return suggestions
    
    def _analyze_text_improvements(self, resume_data: Dict) -> List[str]:
        """Analyze text for improvement opportunities using RAG"""
        improvements = []
        text = resume_data.get('text', '')
        
        # Search for relevant best practices
        query = "improve resume text achievements quantification action verbs"
        relevant_practices = self._search_knowledge_base(query, top_k=3)
        
        # Check for achievement quantification
        if not self._has_quantified_achievements(text):
            improvements.append("Add quantifiable achievements to demonstrate impact")
        
        # Check for action verbs
        if not self._has_strong_action_verbs(text):
            improvements.append("Use stronger action verbs to start bullet points")
        
        # Add RAG-based suggestions
        for practice in relevant_practices:
            improvements.append(practice['content'])
        
        return improvements
    
    def _suggest_missing_skills(self, resume_data: Dict, job_description: str) -> List[str]:
        """Suggest missing skills based on job description and common patterns"""
        resume_skills = set(resume_data.get('skills', []))
        jd_skills = self._extract_skills_from_jd(job_description)
        
        missing_skills = jd_skills - resume_skills
        
        # Use RAG to suggest commonly associated skills
        suggestions = []
        for skill in list(missing_skills)[:5]:  # Limit to top 5
            query = f"skills commonly associated with {skill}"
            associated_skills = self._search_knowledge_base(query, top_k=2)
            
            for assoc_skill in associated_skills:
                if "should emphasize" in assoc_skill['content']:
                    suggestions.append(assoc_skill['content'])
        
        return list(missing_skills)[:10] + suggestions[:3]  # Return top missing skills + RAG suggestions
    
    def _get_formatting_suggestions(self, resume_data: Dict) -> List[str]:
        """Get formatting suggestions using RAG"""
        suggestions = []
        
        # Check resume length
        text = resume_data.get('text', '')
        word_count = len(text.split())
        if word_count > 800:  # Approximate 2-page limit
            suggestions.append("Consider shortening resume to 1-2 pages for better readability")
        
        # Check section organization
        sections = resume_data.get('sections', {})
        required_sections = {'experience', 'education', 'skills'}
        missing_sections = required_sections - set(sections.keys())
        
        if missing_sections:
            suggestions.append(f"Add missing sections: {', '.join(missing_sections)}")
        
        # RAG-based formatting advice
        formatting_advice = self._search_knowledge_base("resume formatting best practices", top_k=2)
        for advice in formatting_advice:
            suggestions.append(advice['content'])
        
        return suggestions
    
    def _get_role_specific_advice(self, resume_data: Dict, job_description: str) -> List[str]:
        """Get role-specific advice using RAG"""
        # Determine role from job description or resume
        role_keywords = {
            'data_science': ['data scientist', 'machine learning', 'data analysis'],
            'software_engineer': ['software engineer', 'developer', 'programming'],
            'project_manager': ['project manager', 'pm', 'scrum master']
        }
        
        detected_role = None
        text_to_analyze = job_description + " " + resume_data.get('text', '')
        
        for role, keywords in role_keywords.items():
            if any(keyword in text_to_analyze.lower() for keyword in keywords):
                detected_role = role
                break
        
        if detected_role:
            query = f"resume advice for {detected_role} role"
            role_advice = self._search_knowledge_base(query, top_k=3)
            return [advice['content'] for advice in role_advice]
        
        return []
    
    def _get_rag_based_suggestions(self, resume_data: Dict, job_description: str) -> List[str]:
        """Get personalized RAG suggestions based on resume content"""
        # Create a comprehensive query based on resume analysis
        skills = resume_data.get('skills', [])
        experience = resume_data.get('experience_years', 0)
        
        query = f"""
        Resume with skills: {', '.join(skills[:10])}
        Experience: {experience} years
        Job description: {job_description[:200]}
        Provide specific improvement suggestions
        """
        
        relevant_suggestions = self._search_knowledge_base(query, top_k=5)
        return [suggestion['content'] for suggestion in relevant_suggestions]
    
    def _search_knowledge_base(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search knowledge base using semantic similarity"""
        if not self.index:
            return []
        
        # Encode query
        query_embedding = self.model.encode([query])
        
        # Search
        scores, indices = self.index.search(query_embedding.astype('float32'), top_k)
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < len(self.knowledge_data):
                results.append({
                    **self.knowledge_data[idx],
                    'relevance_score': float(score)
                })
        
        return results
    
    def _extract_skills_from_jd(self, job_description: str) -> set:
        """Extract skills from job description"""
        from skill_extractor import SkillExtractor
        extractor = SkillExtractor()
        skills_data = extractor.extract_skills(job_description)
        return set(skills_data.get('skills', []))
    
    def _has_quantified_achievements(self, text: str) -> bool:
        """Check if text has quantified achievements"""
        quant_patterns = [
            r'\d+%', r'\$\d+', r'\d+\s*(x|times)', r'increased by', r'reduced by', r'saved\s*\$\d+'
        ]
        return any(re.search(pattern, text.lower()) for pattern in quant_patterns)
    
    def _has_strong_action_verbs(self, text: str) -> bool:
        """Check if text uses strong action verbs"""
        action_verbs = [
            'developed', 'implemented', 'led', 'managed', 'created', 'built',
            'optimized', 'improved', 'increased', 'reduced', 'saved'
        ]
        return any(verb in text.lower() for verb in action_verbs)