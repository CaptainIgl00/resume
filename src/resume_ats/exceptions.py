"""Custom exceptions for resume-ats package."""


class ResumeATSError(Exception):
    """Base exception for resume-ats package."""
    pass


class BuildError(ResumeATSError):
    """Raised when build process fails."""
    pass


class TemplateError(ResumeATSError):
    """Raised when template rendering fails."""
    pass


class CompilationError(ResumeATSError):
    """Raised when LaTeX compilation fails."""
    pass


class ExtractionError(ResumeATSError):
    """Raised when CV data extraction fails."""
    pass


class ValidationError(ResumeATSError):
    """Raised when ATS validation fails."""
    pass 