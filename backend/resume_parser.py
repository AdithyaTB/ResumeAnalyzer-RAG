import re
import pdfplumber
from docx import Document
import spacy
from typing import Dict, List, Any
import nltk
from nltk.tokenize import sent_tokenize

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

class ResumeParser:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.section_patterns = {
            'contact': r'(contact|email|phone|address)',
            'education': r'(education|academic|qualification)',
            'experience': r'(experience|work\s+history|employment)',
            'skills': r'(skills|technical\s+skills|competencies)',
            'projects': r'(projects|portfolio|work\s+samples)',
            'certifications': r'(certifications|certificate|licenses)'
        }
    
    def parse_resume(self, file_path: str) -> Dict[str, Any]:
        """Parse resume file and extract structured information"""
        text = self._extract_text(file_path)
        sections = self._extract_sections(text)
        personal_info = self._extract_personal_info(text)
        experience = self._extract_experience(sections.get('experience', ''))
        education = self._extract_education(sections.get('education', ''))
        
        return {
            'text': text,
            'sections': sections,
            'personal_info': personal_info,
            'experience': experience,
            'education': education,
            'raw_text': text
        }
    
    def _extract_text(self, file_path: str) -> str:
        """Extract text from PDF or DOCX files"""
        if file_path.lower().endswith('.pdf'):
            return self._extract_from_pdf(file_path)
        elif file_path.lower().endswith(('.docx', '.doc')):
            return self._extract_from_docx(file_path)
        else:
            raise ValueError("Unsupported file format")
    
    def _extract_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF using pdfplumber"""
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text
    
    def _extract_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX file"""
        doc = Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    
    def _extract_sections(self, text: str) -> Dict[str, str]:
        """Extract resume sections using regex patterns"""
        lines = text.split('\n')
        sections = {}
        current_section = 'header'
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if line matches any section header
            for section, pattern in self.section_patterns.items():
                if re.search(pattern, line.lower()):
                    current_section = section
                    sections[current_section] = ""
                    continue
            
            # Add content to current section
            if current_section not in sections:
                sections[current_section] = ""
            sections[current_section] += line + "\n"
        
        return sections
    
    def _extract_personal_info(self, text: str) -> Dict[str, str]:
        """Extract personal information using regex and NER"""
        # Email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        
        # Phone numbers
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phones = re.findall(phone_pattern, text)
        
        # Name (first line usually contains name)
        lines = text.split('\n')
        name = lines[0].strip() if lines else ""
        
        return {
            'name': name,
            'email': emails[0] if emails else "",
            'phone': phones[0] if phones else "",
            'emails': emails,
            'phones': phones
        }
    
    def _extract_experience(self, experience_text: str) -> List[Dict]:
        """Extract work experience with dates and roles"""
        experiences = []
        lines = experience_text.split('\n')
        
        current_exp = {}
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Look for date patterns
            date_pattern = r'(\d{4}\s*[-–]\s*\d{4}|(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}\s*[-–]\s*(present|now|(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}))'
            dates = re.findall(date_pattern, line, re.IGNORECASE)
            
            if dates:
                if current_exp:
                    experiences.append(current_exp)
                current_exp = {
                    'dates': dates[0][0],
                    'description': line
                }
            elif current_exp:
                current_exp['description'] += " " + line
        
        if current_exp:
            experiences.append(current_exp)
        
        return experiences
    
    def _extract_education(self, education_text: str) -> List[Dict]:
        """Extract education information"""
        educations = []
        lines = education_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Look for degree patterns
            degree_pattern = r'(B\.?S\.?|B\.?A\.?|M\.?S\.?|M\.?A\.?|Ph\.?D\.?|Bachelor|Master|Doctorate)'
            degrees = re.findall(degree_pattern, line, re.IGNORECASE)
            
            if degrees:
                educations.append({
                    'degree': degrees[0],
                    'institution': line,
                    'description': line
                })
        
        return educations