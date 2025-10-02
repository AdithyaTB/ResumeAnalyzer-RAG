import re
import spacy
from typing import Dict, List, Set
import json

class SkillExtractor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.skills_db = self._load_skills_database()
        
    def _load_skills_database(self) -> Set[str]:
        """Load comprehensive skills database"""
        skills = set()
        
        # Technical skills
        technical_skills = {
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust', 'swift',
            'sql', 'nosql', 'mongodb', 'postgresql', 'mysql', 'redis',
            'django', 'flask', 'fastapi', 'spring', 'react', 'angular', 'vue', 'node.js',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'jenkins',
            'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'keras',
            'git', 'github', 'gitlab', 'jira', 'confluence',
            'linux', 'unix', 'windows', 'macos',
            'html', 'css', 'sass', 'bootstrap', 'tailwind',
            'rest', 'graphql', 'soap', 'microservices', 'api'
        }
        
        # Soft skills
        soft_skills = {
            'leadership', 'communication', 'teamwork', 'problem solving', 'critical thinking',
            'adaptability', 'creativity', 'time management', 'project management',
            'agile', 'scrum', 'kanban', 'waterfall', 'devops'
        }
        
        skills.update(technical_skills)
        skills.update(soft_skills)
        
        return skills
    
    def extract_skills(self, text: str) -> Dict[str, List]:
        """Extract skills from resume text"""
        doc = self.nlp(text.lower())
        
        # Extract using dictionary matching
        found_skills = set()
        for skill in self.skills_db:
            if skill in text.lower():
                found_skills.add(skill)
        
        # Extract using NER
        for ent in doc.ents:
            if ent.label_ in ["SKILL", "PRODUCT", "ORG"]:
                # Clean and check if it's a skill
                skill_text = ent.text.lower().strip()
                if any(char.isalpha() for char in skill_text) and len(skill_text) > 2:
                    found_skills.add(skill_text)
        
        # Extract experience years
        experience_years = self._extract_experience_years(text)
        
        # Extract certifications
        certifications = self._extract_certifications(text)
        
        # Extract projects
        projects = self._extract_projects(text)
        
        return {
            'skills': list(found_skills),
            'experience_years': experience_years,
            'certifications': certifications,
            'projects': projects
        }
    
    def _extract_experience_years(self, text: str) -> float:
        """Extract total years of experience"""
        # Patterns for experience
        patterns = [
            r'(\d+)\s*years?\s*experience',
            r'experience\s*:\s*(\d+)\s*years?',
            r'(\d+)\s*years?\s*in\s*.*experience',
            r'(\d+)\+?\s*years?'
        ]
        
        total_years = 0
        for pattern in patterns:
            matches = re.findall(pattern, text.lower())
            for match in matches:
                if match.isdigit():
                    total_years = max(total_years, int(match))
        
        # If no explicit years found, estimate from dates
        if total_years == 0:
            total_years = self._estimate_experience_from_dates(text)
        
        return total_years
    
    def _estimate_experience_from_dates(self, text: str) -> float:
        """Estimate experience from date ranges"""
        # Simple date pattern matching
        date_pattern = r'(\d{4})\s*[-–]\s*(\d{4}|present|now)'
        matches = re.findall(date_pattern, text, re.IGNORECASE)
        
        if not matches:
            return 0
        
        # Calculate total years (simplified)
        current_year = 2024
        total_years = 0
        
        for start, end in matches:
            try:
                start_year = int(start)
                if end.lower() in ['present', 'now']:
                    end_year = current_year
                else:
                    end_year = int(end)
                
                total_years += (end_year - start_year)
            except ValueError:
                continue
        
        return max(1, total_years)  # Minimum 1 year
    
    def _extract_certifications(self, text: str) -> List[str]:
        """Extract certifications from text"""
        certifications = []
        
        # Common certification patterns
        cert_patterns = [
            r'([A-Z]+-[A-Z0-9]+)',  # AWS-SAA, PMP-001, etc.
            r'(AWS Certified [^,\n]+)',
            r'(Microsoft Certified [^,\n]+)',
            r'(Google Cloud [^,\n]+)',
            r'(PMP|CISSP|CEH|CCNA|CCNP|CompTIA [^,\n]+)',
        ]
        
        for pattern in cert_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            certifications.extend(matches)
        
        return list(set(certifications))
    
    def _extract_projects(self, text: str) -> List[Dict]:
        """Extract project information"""
        projects = []
        lines = text.split('\n')
        
        current_project = {}
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            # Look for project indicators
            project_indicators = ['project:', 'developed', 'built', 'created', 'implemented']
            if any(indicator in line.lower() for indicator in project_indicators):
                if current_project:
                    projects.append(current_project)
                
                current_project = {
                    'title': line,
                    'description': line,
                    'technologies': self._extract_technologies_from_line(line)
                }
            elif current_project:
                current_project['description'] += " " + line
        
        if current_project:
            projects.append(current_project)
        
        return projects
    
    def _extract_technologies_from_line(self, line: str) -> List[str]:
        """Extract technologies mentioned in a line"""
        technologies = []
        for skill in self.skills_db:
            if skill in line.lower():
                technologies.append(skill)
        return technologies