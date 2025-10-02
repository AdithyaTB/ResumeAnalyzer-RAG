import re
from typing import Dict, List, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from backend.skill_extractor import SkillExtractor

class ScoringEngine:
    def __init__(self):
        self.weights = {
            'skills': 0.50,
            'experience': 0.20,
            'education': 0.15,
            'projects_certifications': 0.15
        }
    
    def calculate_score(self, resume_data: Dict, job_description: str = "") -> Dict[str, Any]:
        """Calculate comprehensive resume score"""
        if job_description:
            return self._calculate_job_specific_score(resume_data, job_description)
        else:
            return self._calculate_general_score(resume_data)
    
    def _calculate_job_specific_score(self, resume_data: Dict, job_description: str) -> Dict[str, Any]:
        """Calculate score specific to job description"""
        # Extract keywords from job description
        jd_skills = self._extract_skills_from_text(job_description)
        jd_keywords = self._extract_keywords(job_description)
        
        resume_skills = set(resume_data.get('skills', []))
        resume_text = resume_data.get('text', '')
        
        # Skill matching
        skill_match = self._calculate_skill_match(resume_skills, jd_skills)
        
        # Keyword matching using TF-IDF
        keyword_similarity = self._calculate_keyword_similarity(resume_text, job_description)
        
        # Experience matching
        experience_score = self._calculate_experience_score(resume_data, job_description)
        
        # Education matching
        education_score = self._calculate_education_score(resume_data, job_description)
        
        # Projects and certifications
        projects_cert_score = self._calculate_projects_certifications_score(resume_data, job_description)
        
        # Calculate weighted score
        category_scores = {
            'skills': skill_match * 100,
            'experience': experience_score * 100,
            'education': education_score * 100,
            'projects_certifications': projects_cert_score * 100,
            'keyword_similarity': keyword_similarity * 100
        }
        
        overall_score = (
            category_scores['skills'] * self.weights['skills'] +
            category_scores['experience'] * self.weights['experience'] +
            category_scores['education'] * self.weights['education'] +
            category_scores['projects_certifications'] * self.weights['projects_certifications']
        )
        
        return {
            'overall_score': round(overall_score, 2),
            'category_scores': category_scores,
            'breakdown': self._generate_score_breakdown(resume_data, jd_skills, jd_keywords),
            'matched_skills': list(resume_skills.intersection(jd_skills)),
            'missing_skills': list(jd_skills - resume_skills)
        }
    
    def _calculate_general_score(self, resume_data: Dict) -> Dict[str, Any]:
        """Calculate general resume quality score"""
        score = 50  # Base score
        
        # Skills diversity
        skills = resume_data.get('skills', [])
        if len(skills) >= 10:
            score += 15
        elif len(skills) >= 5:
            score += 10
        
        # Experience
        experience_years = resume_data.get('experience_years', 0)
        if experience_years >= 5:
            score += 15
        elif experience_years >= 2:
            score += 10
        
        # Education
        education = resume_data.get('education', [])
        if education:
            score += 10
        
        # Projects
        projects = resume_data.get('projects', [])
        if len(projects) >= 2:
            score += 10
        
        # Certifications
        certifications = resume_data.get('certifications', [])
        if certifications:
            score += 5
        
        return {
            'overall_score': min(100, score),
            'category_scores': {
                'skills': len(skills) * 2,
                'experience': min(experience_years * 10, 100),
                'education': len(education) * 20,
                'projects_certifications': (len(projects) + len(certifications)) * 10
            },
            'breakdown': "General quality assessment based on resume completeness"
        }
    
    def _extract_skills_from_text(self, text: str) -> set:
        """Extract skills from text using simple pattern matching"""
        skills_db = SkillExtractor().skills_db
        found_skills = set()
        
        for skill in skills_db:
            if skill in text.lower():
                found_skills.add(skill)
        
        return found_skills
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from text"""
        # Remove common words and get meaningful terms
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        stop_words = {'the', 'and', 'for', 'with', 'this', 'that', 'have', 'has', 'had', 'are', 'were'}
        keywords = [word for word in words if word not in stop_words]
        
        return keywords
    
    def _calculate_skill_match(self, resume_skills: set, jd_skills: set) -> float:
        """Calculate skill matching score"""
        if not jd_skills:
            return 0.5  # Neutral score if no JD skills
        
        if not resume_skills:
            return 0.0
        
        intersection = resume_skills.intersection(jd_skills)
        return len(intersection) / len(jd_skills)
    
    def _calculate_keyword_similarity(self, resume_text: str, jd_text: str) -> float:
        """Calculate text similarity using TF-IDF and cosine similarity"""
        if not jd_text.strip():
            return 0.5
        
        documents = [resume_text, jd_text]
        vectorizer = TfidfVectorizer(stop_words='english')
        
        try:
            tfidf_matrix = vectorizer.fit_transform(documents)
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
            return similarity[0][0]
        except:
            return 0.0
    
    def _calculate_experience_score(self, resume_data: Dict, job_description: str) -> float:
        """Calculate experience matching score"""
        experience_years = resume_data.get('experience_years', 0)
        
        # Extract required experience from JD
        jd_experience = self._extract_experience_from_jd(job_description)
        
        if jd_experprise == 0:
            return min(experience_years / 10, 1.0)  # Normalize to 0-1
        
        if experience_years >= jd_experience:
            return 1.0
        else:
            return experience_years / jd_experience
    
    def _extract_experience_from_jd(self, job_description: str) -> int:
        """Extract required years of experience from job description"""
        patterns = [
            r'(\d+)\s*[+]?\s*years?\s*experience',
            r'experience\s*:\s*(\d+)\s*[+]?\s*years?',
            r'(\d+)\s*[+]?\s*years?\s*in\s*.*industry'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, job_description.lower())
            if matches:
                return int(matches[0])
        
        return 0  # Default if no experience requirement found
    
    def _calculate_education_score(self, resume_data: Dict, job_description: str) -> float:
        """Calculate education matching score"""
        education = resume_data.get('education', [])
        
        # Check for degree requirements in JD
        jd_degrees = self._extract_degrees_from_jd(job_description)
        
        if not jd_degrees:
            return 0.7 if education else 0.3
        
        # Check if resume has required degrees
        resume_degrees = [edu.get('degree', '').lower() for edu in education]
        
        for jd_degree in jd_degrees:
            if any(jd_degree in degree for degree in resume_degrees):
                return 1.0
        
        return 0.3
    
    def _extract_degrees_from_jd(self, job_description: str) -> List[str]:
        """Extract required degrees from job description"""
        degree_patterns = [
            r'bachelor[\'s]*\s*degree',
            r'master[\'s]*\s*degree',
            r'phd|ph\.d|doctorate',
            r'b\.s|b\.a|m\.s|m\.a'
        ]
        
        found_degrees = []
        for pattern in degree_patterns:
            if re.search(pattern, job_description.lower()):
                found_degrees.append(pattern.split('\\')[-1])  # Get the degree name
        
        return found_degrees
    
    def _calculate_projects_certifications_score(self, resume_data: Dict, job_description: str) -> float:
        """Calculate projects and certifications score"""
        projects = resume_data.get('projects', [])
        certifications = resume_data.get('certifications', [])
        
        # Simple scoring based on quantity and relevance
        base_score = min((len(projects) * 0.1 + len(certifications) * 0.1), 0.5)
        
        # Check relevance to job description
        relevance_bonus = 0
        if job_description:
            jd_tech = self._extract_skills_from_text(job_description)
            
            # Check project technologies
            for project in projects:
                project_tech = set(project.get('technologies', []))
                if project_tech.intersection(jd_tech):
                    relevance_bonus += 0.1
            
            # Check certifications relevance
            for cert in certifications:
                if any(tech in cert.lower() for tech in jd_tech):
                    relevance_bonus += 0.05
        
        return min(base_score + relevance_bonus, 1.0)
    
    def _generate_score_breakdown(self, resume_data: Dict, jd_skills: set, jd_keywords: List[str]) -> str:
        """Generate detailed explanation of the score"""
        breakdown = []
        
        skills_match = len(resume_data.get('skills', []).intersection(jd_skills))
        breakdown.append(f"Skills Match: {skills_match}/{len(jd_skills)} relevant skills")
        
        experience = resume_data.get('experience_years', 0)
        breakdown.append(f"Experience: {experience} years of relevant experience")
        
        education = len(resume_data.get('education', []))
        breakdown.append(f"Education: {education} degree(s) listed")
        
        projects = len(resume_data.get('projects', []))
        certifications = len(resume_data.get('certifications', []))
        breakdown.append(f"Projects & Certifications: {projects} projects, {certifications} certifications")
        
        return "; ".join(breakdown)