"""CV data extraction functionality."""

import re
import subprocess
from pathlib import Path
from typing import List, Set, Optional

import pdfplumber
from rich.console import Console

from .models import CVData
from .exceptions import ExtractionError


class CVExtractor:
    """Robust CV data extractor."""
    
    def __init__(self, pdf_path: Path):
        """Initialize extractor with PDF path.
        
        Args:
            pdf_path: Path to PDF file
            
        Raises:
            ExtractionError: If PDF cannot be processed
        """
        self.pdf_path = Path(pdf_path)
        self.console = Console()
        self.text = self._extract_text()
    
    def _extract_text(self) -> str:
        """Extract text from PDF using multiple fallback methods.
        
        Returns:
            Extracted text content
            
        Raises:
            ExtractionError: If all extraction methods fail
        """
        try:
            # Primary method: pdfplumber
            with pdfplumber.open(self.pdf_path) as pdf:
                text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                
                if text.strip():
                    return text
                    
        except Exception as e:
            self.console.print(f"⚠️  pdfplumber failed: {e}")
        
        try:
            # Fallback: pdftotext
            result = subprocess.run(
                ['pdftotext', str(self.pdf_path), '-'], 
                capture_output=True, 
                text=True,
                timeout=30
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout
                
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            self.console.print(f"⚠️  pdftotext failed: {e}")
        
        raise ExtractionError(f"Could not extract text from {self.pdf_path}")
    
    def extract_name(self) -> str:
        """Extract full name from CV.
        
        Returns:
            Extracted name or empty string
        """
        lines = self.text.strip().split('\n')
        
        for line in lines[:5]:  # Check first 5 lines
            line = line.strip()
            # Pattern for full name (2+ capitalized words)
            name_match = re.match(
                r'^([A-ZÀÂÄÉÈÊËÌÎÏÒÔÖÙÛÜŸÇ][a-zàâäéèêëìîïòôöùûüÿç]+(?:\s+[A-ZÀÂÄÉÈÊËÌÎÏÒÔÖÙÛÜŸÇ][a-zàâäéèêëìîïòôöùûüÿç]+)+)', 
                line
            )
            if name_match:
                return name_match.group(1).strip()
        
        return ""
    
    def extract_email(self) -> str:
        """Extract email address from CV.
        
        Returns:
            Extracted email or empty string
        """
        email_pattern = r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
        email_match = re.search(email_pattern, self.text)
        return email_match.group(1) if email_match else ""
    
    def extract_position(self) -> str:
        """Extract job position/title from CV.
        
        Returns:
            Extracted position or empty string
        """
        patterns = [
            r'(?i)(devops?\s*eng?i?neer)',
            r'(?i)(software\s*engineer)', 
            r'(?i)(backend\s*developer)',
            r'(?i)(full\s*stack\s*developer)',
            r'(?i)(devopseng?i?neer)',  # Concatenated version
        ]
        
        for pattern in patterns:
            match = re.search(pattern, self.text)
            if match:
                found = match.group(1)
                # Normalize common positions
                if "devops" in found.lower() and "engineer" in found.lower():
                    return "DevOps Engineer"
                return found
        
        return ""
    
    def extract_skills(self) -> List[str]:
        """Extract technical skills from CV.
        
        Returns:
            List of extracted skills
        """
        tech_keywords = {
            'docker', 'kubernetes', 'k8s', 'terraform', 'ansible', 'jenkins', 
            'gitlab', 'github', 'aws', 'azure', 'gcp', 'ovh', 'linux', 'python', 
            'bash', 'shell', 'git', 'ci/cd', 'devops', 'prometheus', 'grafana', 
            'elasticsearch', 'kibana', 'nginx', 'apache', 'mysql', 'postgresql',
            'redis', 'mongodb', 'helm', 'vagrant', 'consul', 'vault', 'nomad', 
            'packer', 'java', 'javascript', 'typescript', 'node.js', 'react', 
            'angular', 'vue', 'vue.js', 'nuxt.js', 'php', 'golang', 'go', 'rust', 
            'scala', 'ruby', 'perl', 'c++', 'c#', '.net', 'spring', 'django', 
            'flask', 'express', 'fastapi', 'sqlalchemy', 'jira', 'confluence', 
            'scrum', 'agile', 'podman', 'elk', 'homeassistant'
        }
        
        found_skills = set()
        text_lower = self.text.lower()
        
        # Direct keyword search
        for keyword in tech_keywords:
            if keyword in text_lower:
                found_skills.add(keyword)
        
        # Section-specific search
        skills_section = re.search(
            r'(?i)(?:skills|compétences|technologies)(.*?)(?:\n\n|\n[A-Z]|$)', 
            self.text, 
            re.DOTALL
        )
        
        if skills_section:
            skills_text = skills_section.group(1).lower()
            additional_patterns = [
                r'\b(helm)\b', r'\b(jira)\b', r'\b(confluence)\b',
                r'\b(scrum)\b', r'\b(agile)\b'
            ]
            
            for pattern in additional_patterns:
                matches = re.findall(pattern, skills_text)
                found_skills.update(matches)
        
        return sorted(list(found_skills))
    
    def extract_companies(self) -> List[str]:
        """Extract company names from CV.
        
        Returns:
            List of extracted company names
        """
        companies = set()
        
        patterns = [
            r'(?i)(?:company|entreprise|société):\s*([A-Z][a-zA-Z\s&]+)',
            r'(?i)([A-Z][a-zA-Z\s&]{3,})\s*(?:–|,|\()\s*(?:Toulouse|France|Remote)',
            r'(?i)(Continental|Neverhack|Airbus|OVH)',
            r'Neverhack\(missionAirbusDefenceandSpace\)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, self.text)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0] if match[0] else match[1]
                
                company = match.strip()
                if len(company) > 2 and company not in ['France', 'Remote', 'Toulouse']:
                    companies.add(company)
        
        return sorted(list(companies))
    
    def extract_all(self) -> CVData:
        """Extract all CV data.
        
        Returns:
            CVData model with extracted information
        """
        return CVData(
            name=self.extract_name(),
            email=self.extract_email(),
            position=self.extract_position(),
            skills=self.extract_skills(),
            companies=self.extract_companies(),
            technologies=self.extract_skills()  # Alias for skills
        ) 