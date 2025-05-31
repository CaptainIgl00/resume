"""Data models for resume generation and validation."""

from datetime import date
from typing import List, Optional, Dict, Any, Union
from pathlib import Path

from pydantic import BaseModel, validator, ConfigDict


class Location(BaseModel):
    """Location model."""
    city: Optional[str] = None
    countryCode: Optional[str] = None


class Profile(BaseModel):
    """Social profile model."""
    network: str
    username: str
    url: str


class ContactInfo(BaseModel):
    """Contact information model."""
    name: str
    email: str
    label: Optional[str] = None
    location: Optional[Union[Location, str]] = None  # Can be Location object or string
    summary: Optional[str] = None
    profiles: List[Profile] = []


class WorkExperience(BaseModel):
    """Work experience model."""
    company: str
    position: str
    location: Optional[str] = None
    startDate: str  # Keep as string to match YAML format
    endDate: Optional[str] = None
    highlights: List[str] = []
    summary: Optional[str] = None


class Education(BaseModel):
    """Education model."""
    institution: str
    area: str
    studyType: str
    startDate: Optional[str] = None  # Keep as string
    endDate: Optional[str] = None
    location: Optional[str] = None
    notes: Optional[str] = None


class Project(BaseModel):
    """Project model."""
    name: str
    description: str
    highlights: List[str] = []
    keywords: List[str] = []
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    url: Optional[str] = None


class Skill(BaseModel):
    """Skill category model."""
    name: str
    keywords: List[str] = []


class Language(BaseModel):
    """Language proficiency model."""
    language: str
    fluency: str


class Reference(BaseModel):
    """Reference model."""
    name: str
    reference: str  # Email or contact info


class ResumeData(BaseModel):
    """Complete resume data model."""
    basics: ContactInfo
    work: List[WorkExperience] = []
    education: List[Education] = []
    projects: List[Project] = []
    skills: List[Union[Skill, str]] = []  # Can be Skill objects or strings
    languages: List[Union[Language, str]] = []  # Can be Language objects or strings
    references: List[Reference] = []
    interests: List[str] = []


class CVData(BaseModel):
    """Extracted CV data for ATS validation."""
    name: str
    email: str
    position: str
    skills: List[str] = []
    companies: List[str] = []
    technologies: List[str] = []


class BuildConfig(BaseModel):
    """Build configuration model."""
    model_config = ConfigDict(arbitrary_types_allowed=True)  # Updated config
    
    template_dir: Path = Path("templates")
    output_dir: Path = Path("build") 
    clean_build: bool = True
    formats: List[str] = ["pdf"] 