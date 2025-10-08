# Resume ATS - Professional Resume Builder

🎯 **Professional resume generator optimized for Applicant Tracking Systems (ATS)**

## ✨ Features

- 🏗️ **Modern Python Package**: Clean architecture with Pydantic models and type hints
- 🎨 **Beautiful CLI**: Rich terminal interface with progress bars and colored output
- 📄 **Multiple Formats**: Generate PDF, HTML, and JSON from the same YAML source
- 🤖 **ATS Validation**: Automated testing to ensure your resume is ATS-compatible
- 🧪 **Comprehensive Testing**: Unit, integration, and ATS compatibility tests
- 📦 **Easy Installation**: Modern `pyproject.toml` with optional dependencies
- 🚀 **CI/CD Integration**: Automated validation and release workflows

## 🚀 Quick Start

```bash
# Setup
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[ats]"

# Build and validate
make build
make validate
```

### Markdown Bold in resume.yml
```yaml
basics:
  summary: |
    DevOps engineer with **3 years' experience** helping companies...
    
work:
  - highlights:
      - "Developed services in **Python**, **Golang** and **Java**"
      - "Built **Vue.js + Grafana** monitoring dashboards"
      
skills:
  - name: "Programming Languages"
    keywords: ["**Python**", "**Go**", "**Java**"]
```

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
```

### Makefile Commands

```bash
make build          # Build PDF resume
make build-all      # Build all formats (PDF, HTML, JSON)
make validate       # Validate ATS compatibility
make test           # Run all tests
make test-ats       # Run ATS tests only
make extract        # Extract data from PDF
make clean          # Clean build artifacts
```

## 🔧 Installation

```bash
# Clone and setup
git clone <your-repo>
cd resume-ats
python3 -m venv .venv
source .venv/bin/activate

# Install with dependencies
pip install -e ".[ats]"

# Setup ATS dependencies
make setup
```

## 📊 ATS Validation

Automated validation ensures your resume is ATS-compatible:

```bash
✅ Name: Complete extraction
✅ Email: Exact match  
✅ Position: Normalized
✅ Skills: 84%+ coverage
✅ Companies: Detected
```

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

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details. 