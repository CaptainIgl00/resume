# Resume ATS - Modern Python Resume Generator

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Generate professional, ATS-friendly resumes from YAML data with automated validation using modern Python tooling.

## 🚀 Quick Start

```bash
# Setup
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[ats]"

# Build and validate
make build
make validate
```

## ✨ Features

- 🏗️ **Modern Python Package**: Clean architecture with Pydantic models and type hints
- 🎨 **Beautiful CLI**: Rich terminal interface with progress bars and colored output
- 📄 **Multiple Formats**: Generate PDF, HTML, and JSON from the same YAML source
- 🤖 **ATS Validation**: Automated testing to ensure your resume is ATS-compatible
- 🧪 **Comprehensive Testing**: Unit, integration, and ATS compatibility tests
- 📦 **Easy Installation**: Modern `pyproject.toml` with optional dependencies

## 📋 Usage

### Command Line Interface

```bash
# Build resume (PDF by default)
resume-build build

# Build all formats
resume-build build --format pdf --format html --format json

# Extract data from PDF for validation
resume-build extract build/Your_Name_CV.pdf

# Validate ATS compatibility
resume-build validate resume.yml build/Your_Name_CV.pdf

# Setup ATS dependencies
resume-build setup

# Show help
resume-build --help
```

### Makefile Commands

```bash
make help           # Show all available commands
make build          # Build PDF resume
make build-all      # Build all formats (PDF, HTML, JSON)
make validate       # Validate ATS compatibility
make test           # Run all tests
make test-ats       # Run ATS tests only
make extract        # Extract data from PDF
make clean          # Clean build artifacts
make status         # Show project status
```

## 📁 Project Structure

```
resume-ats/
├── src/resume_ats/          # Main package
│   ├── __init__.py         # Package exports
│   ├── cli.py              # Modern CLI with Typer
│   ├── core.py             # ResumeBuilder class
│   ├── models.py           # Pydantic data models
│   ├── extractors.py       # CV data extraction
│   └── exceptions.py       # Custom exceptions
├── tests/                   # Modern test suite
│   └── test_modern_ats.py  # Comprehensive tests
├── templates/               # Jinja2 templates
│   ├── awesomecv.tex.j2    # LaTeX template
│   └── simple.html.j2      # HTML template
├── build/                   # Generated files
├── resume.yml              # Your resume data
├── pyproject.toml          # Modern Python config
└── Makefile               # Build automation
```

## 🔧 Installation

### Development Installation

```bash
# Clone and setup
git clone <your-repo>
cd resume-ats
python3 -m venv .venv
source .venv/bin/activate

# Install with all dependencies
pip install -e ".[dev,test,ats]"

# Setup ATS dependencies
make setup
```

### Dependencies

- **Core**: PyYAML, Jinja2, Pydantic, Rich, Typer
- **ATS**: pdfplumber, pyresparser, NLTK, spaCy
- **Dev**: black, ruff, mypy, pre-commit
- **Test**: pytest, pytest-cov, pytest-mock

## 🧪 Testing

The project includes comprehensive testing with pytest:

```bash
# Run all tests
make test

# Run specific test categories
make test-ats           # ATS compatibility tests
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only

# Verbose testing
make test-verbose
```

### Test Categories

- **Unit Tests**: Test individual components
- **Integration Tests**: Test complete workflows
- **ATS Tests**: Validate resume extraction and compatibility

## 📊 ATS Validation

Automated validation ensures your resume is ATS-compatible:

```bash
✅ Name: Mathéo Guilloux (complete extraction)
✅ Email: matheo.guilloux@gmail.com (exact match)  
✅ Position: DevOps Engineer (normalized)
✅ Skills: 36 detected (76% coverage vs resume.yml)
✅ Companies: 12 detected including major ones
```

## 🎯 Modern Python Features

- **Type Safety**: Full type hints with Pydantic models
- **Error Handling**: Custom exceptions with clear messages
- **Configuration**: Modern `pyproject.toml` with optional dependencies
- **CLI**: Rich terminal interface with Typer
- **Testing**: Comprehensive pytest suite with fixtures and markers
- **Code Quality**: Black formatting, Ruff linting, mypy type checking

## 📝 Configuration

Edit `resume.yml` with your information:

```yaml
basics:
  name: "Your Name"
  label: "Your Title"
  email: "your.email@example.com"
  location:
    city: "Your City"
    countryCode: "FR"

work:
  - company: "Company Name"
    position: "Your Position"
    startDate: "2023-01"
    endDate: "Present"
    highlights:
      - "Achievement 1"
      - "Achievement 2"

skills:
  - name: "Technical Skills"
    keywords: ["Python", "Docker", "Kubernetes"]
```

## 🔧 Prerequisites

**LaTeX** (for PDF generation):
```bash
# Ubuntu/Debian
sudo apt install texlive-xetex texlive-latex-extra texlive-fonts-recommended

# macOS
brew install --cask mactex
```

**Python 3.9+** with pip and venv support.

## 🛠️ Development

```bash
# Code formatting
make format

# Linting
make lint

# Type checking
make type-check

# All quality checks
make check

# Watch for changes
make watch
```

## 📦 Distribution

```bash
# Build distribution
make dist

# Publish to test PyPI
make publish-test

# Publish to PyPI
make publish
```

## 🆚 Migration from Legacy

The new system replaces:
- ❌ `build.py` → ✅ `resume-build` CLI
- ❌ `setup_ats_deps.sh` → ✅ `resume-build setup`
- ❌ `test_ats_friendly.sh` → ✅ `pytest` with markers
- ❌ `requirements.txt` → ✅ `pyproject.toml`

All functionality is preserved with improved UX and maintainability.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

**Key Improvement**: This is now a proper Python package with modern tooling, type safety, comprehensive testing, and a beautiful CLI interface while maintaining all original functionality. 