"""Resume ATS - Generate ATS-friendly resumes from YAML data.

A modern Python package for generating professional, ATS-compatible resumes
from YAML configuration files with automated validation.
"""

__version__ = "0.1.0"
__author__ = "Mathéo Guilloux"
__email__ = "matheo.guilloux@gmail.com"

from .core import ResumeBuilder
from .extractors import CVExtractor  
from .models import ResumeData, CVData

__all__ = [
    "ResumeBuilder",
    "CVExtractor", 
    "ResumeData",
    "CVData",
] 