import re
from typing import Dict, List, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class JobMatcher:
    def __init__(self):
        self.required_sections = ['experience', 'education', 'skills']
    
    def analyze_match(self, resume_data: Dict, job_description: str) -> Dict[str, Any]:
        """Analyze match between resume and job description"""
        if not job_description.strip():
            return {"error": "No job description provided"}
        
        analysis = {
            "overall_match": 0,
            "strengths": [],
            "gaps": [],
            "keyword_analysis": {},
            "section_analysis": {},
            "improvement_suggestions": []
        }
        
        # Calculate overall match score
        analysis["overall_match"] = self._calculate_overall_match(resume_data, job_description)
        
        # Identify strengths and gaps
        analysis.update(self._identify_strengths_gaps(resume_data, job_description))
        
        # Keyword analysis
        analysis["keyword_analysis"] = self._analyze_keywords(resume_data, job_description)
        
        # Section completeness analysis
        analysis["section_analysis"] = self._analyze_sections(resume_data, job_description)
        
        # Improvement suggestions
        analysis["improvement_suggestions"] = self._generate_improvement_suggestions(
            resume_data, job_description, analysis
        )
        
        return analysis
    
    def _calculate_overall_match(self, resume_data: Dict, job_description: str) -> float:
        """Calculate overall match score between resume and JD"""
        resume_text = resume_data.get('text', '')
        
        # TF-IDF similarity
        vectorizer = TfidfVectorizer(stop_words='english')
        try:
            tfidf_matrix = vectorizer.fit_transform([resume_text, job_description])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
            tfidf_score = similarity[0][0]
        except:
            tfidf_score = 0
        
        # Skill matching score
        resume_skills = set(resume_data.get('skills', []))
        jd_skills = self._extract_skills_from_jd(job_description)
        skill_score = len(resume_skills.intersection(jd_skills)) / max(len(jd_skills), 1)
        
        # Experience matching
        experience_score = self._calculate_experience_match(resume_data, job_description)
        
        # Weighted overall score
        overall_score = (
            tfidf_score * 0.3 +
            skill_score * 0.4 +
            experience_score * 0.3
        )
        
        return round(overall_score * 100, 2)
    
    def _identify_strengths_gaps(self, resume_data: Dict, job_description: str) -> Dict[str, List]:
        """Identify strengths and gaps in the resume compared to JD"""
        strengths = []
        gaps = []
        
        resume_skills = set(resume_data.get('skills', []))
        jd_skills = self._extract_skills_from_jd(job_description)
        
        # Skills analysis
        matching_skills = resume_skills.intersection(jd_skills)
        missing_skills = jd_skills - resume_skills
        
        if matching_skills:
            strengths.append(f"Strong skills match: {', '.join(list(matching_skills)[:5])}")
        
        if missing_skills:
            gaps.append(f"Missing key skills: {', '.join(list(missing_skills)[:5])}")
        
        # Experience analysis
        resume_experience = resume_data.get('experience_years', 0)
        jd_experience = self._extract_experience_requirement(job_description)
        
        if resume_experience >= jd_experience:
            strengths.append(f"Meets experience requirement: {resume_experience} years")
        else:
            gaps.append(f"Experience gap: {resume_experience} years vs required {jd_experience} years")
        
        # Education analysis
        education_match = self._check_education_match(resume_data, job_description)
        if education_match:
            strengths.append("Education requirements met")
        else:
            gaps.append("Education requirements may not be fully met")
        
        return {
            "strengths": strengths,
            "gaps": gaps
        }
    
    def _analyze_keywords(self, resume_data: Dict, job_description: str) -> Dict[str, Any]:
        """Analyze keyword presence and frequency"""
        resume_text = resume_data.get('text', '').lower()
        jd_text = job_description.lower()
        
        # Extract important keywords from JD
        jd_keywords = self._extract_important_keywords(jd_text)
        
        # Check presence in resume
        present_keywords = []
        missing_keywords = []
        
        for keyword in jd_keywords:
            if keyword in resume_text:
                present_keywords.append(keyword)
            else:
                missing_keywords.append(keyword)
        
        return {
            "total_keywords": len(jd_keywords),
            "present_keywords": present_keywords,
            "missing_keywords": missing_keywords,
            "coverage_percentage": len(present_keywords) / max(len(jd_keywords), 1) * 100
        }
    
    def _analyze_sections(self, resume_data: Dict, job_description: str) -> Dict[str, Any]:
        """Analyze resume section completeness and relevance"""
        sections = resume_data.get('sections', {})
        analysis = {}
        
        for section in self.required_sections:
            has_section = section in sections
            section_content = sections.get(section, '')
            section_length = len(section_content.strip())
            
            analysis[section] = {
                "present": has_section,
                "completeness": "Good" if section_length > 100 else "Needs improvement",
                "word_count": section_length
            }
        
        return analysis
    
    def _generate_improvement_suggestions(self, resume_data: Dict, job_description: str, analysis: Dict) -> List[str]:
        """Generate specific improvement suggestions"""
        suggestions = []
        
        # Keyword suggestions
        keyword_analysis = analysis.get('keyword_analysis', {})
        missing_keywords = keyword_analysis.get('missing_keywords', [])
        
        if missing_keywords:
            suggestions.append(f"Add missing keywords: {', '.join(missing_keywords[:3])}")
        
        # Skill suggestions
        gaps = analysis.get('gaps', [])
        for gap in gaps:
            if "Missing key skills" in gap:
                suggestions.append("Consider acquiring or highlighting missing skills in projects")
        
        # Experience suggestions
        resume_experience = resume_data.get('experience_years', 0)
        jd_experience = self._extract_experience_requirement(job_description)
        
        if resume_experience < jd_experience:
            suggestions.append("Highlight transferable skills and project experience to compensate for experience gap")
        
        # Section suggestions
        section_analysis = analysis.get('section_analysis', {})
        for section, info in section_analysis.items():
            if not info['present']:
                suggestions.append(f"Add a dedicated {section.title()} section")
            elif info['completeness'] == "Needs improvement":
                suggestions.append(f"Expand the {section.title()} section with more details")
        
        return suggestions[:5]  # Limit to top 5 suggestions
    
    def _extract_skills_from_jd(self, job_description: str) -> set:
        """Extract skills from job description"""
        from skill_extractor import SkillExtractor
        extractor = SkillExtractor()
        skills_data = extractor.extract_skills(job_description)
        return set(skills_data.get('skills', []))
    
    def _extract_experience_requirement(self, job_description: str) -> int:
        """Extract required years of experience from JD"""
        patterns = [
            r'(\d+)\s*[+]?\s*years?\s*experience',
            r'experience\s*:\s*(\d+)\s*[+]?\s*years?',
            r'(\d+)\s*[+]?\s*years?\s*in\s*.*industry'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, job_description.lower())
            if matches:
                return int(matches[0])
        
        return 2  # Default experience requirement
    
    def _extract_important_keywords(self, text: str, top_n: int = 15) -> List[str]:
        """Extract important keywords using TF-IDF"""
        # Simple implementation - in production, use more sophisticated keyword extraction
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
        
        # Remove common stop words
        stop_words = {
            'this', 'that', 'with', 'have', 'from', 'they', 'what', 'were', 'when',
            'which', 'would', 'there', 'their', 'about', 'should', 'could', 'more'
        }
        
        filtered_words = [word for word in words if word not in stop_words]
        
        # Get most frequent words
        from collections import Counter
        word_freq = Counter(filtered_words)
        
        return [word for word, _ in word_freq.most_common(top_n)]
    
    def _calculate_experience_match(self, resume_data: Dict, job_description: str) -> float:
        """Calculate experience matching score"""
        resume_experience = resume_data.get('experience_years', 0)
        jd_experience = self._extract_experience_requirement(job_description)
        
        if jd_experience == 0:
            return 0.7  # Neutral score if no experience requirement
        
        if resume_experience >= jd_experience:
            return 1.0
        else:
            return resume_experience / jd_experience
    
    def _check_education_match(self, resume_data: Dict, job_description: str) -> bool:
        """Check if education requirements are met"""
        education = resume_data.get('education', [])
        
        # Look for degree requirements in JD
        degree_requirements = [
            'bachelor', 'master', 'phd', 'b.s', 'b.a', 'm.s', 'm.a'
        ]
        
        jd_lower = job_description.lower()
        has_degree_requirement = any(degree in jd_lower for degree in degree_requirements)
        
        if not has_degree_requirement:
            return True  # No specific requirement
        
        if not education:
            return False  # Requirement but no education listed
        
        # Check if any education matches requirements
        for edu in education:
            edu_text = edu.get('description', '').lower()
            if any(degree in edu_text for degree in degree_requirements):
                return True
        
        return False