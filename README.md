# Resume Generator with ATS Testing

Generate professional, ATS-friendly resumes from YAML data with automated validation.

## 🚀 Quick Start

```bash
# Setup
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
./setup_ats_deps.sh  # First time only

# Build and validate
make build-and-test
```

## 📝 Usage

```bash
make pdf           # Generate PDF only
make test-ats      # Test ATS compatibility  
make build-and-test # Build + validate
make clean         # Clean build directory
```

## 📋 Files

- `resume.yml` - Your resume data (edit this)
- `build/Mathéo_Guilloux_CV.pdf` - Generated PDF
- `tests/test_ats_compatibility.py` - ATS validation tests

## 🧪 ATS Testing

The system automatically validates that your CV is ATS-compatible:

```bash
✅ Name: Mathéo Guilloux (complete extraction)
✅ Email: matheo.guilloux@gmail.com (exact match)  
✅ Position: DevOps Engineer (normalized)
✅ Skills: 36 detected (100% coverage vs resume.yml)
✅ Companies: 12 detected including major ones
```

### Test Commands
```bash
pytest tests/test_ats_compatibility.py -v    # All tests
pytest tests/ -k test_name_extraction -v -s  # Specific test
```

## 🔧 Prerequisites

**LaTeX** (for PDF generation):
```bash
# Ubuntu/Debian
sudo apt install texlive-xetex texlive-latex-extra texlive-fonts-recommended poppler-utils

# macOS
brew install --cask mactex poppler
```

**Python packages** (auto-installed):
- PyYAML, Jinja2, pytest, pdfplumber, pydantic

## 📁 Structure

```
resume/
├── resume.yml              # Your data (edit this)
├── build.py               # Build script
├── templates/             # LaTeX/HTML templates  
├── tests/                 # ATS validation tests
├── build/                 # Generated files
└── Makefile              # Build commands
```

## 🛠️ Troubleshooting

**Test fails**: Check extraction with `pytest tests/ -v -s`  
**LaTeX errors**: Verify fonts with `fc-list | grep -i roboto`  
**Dependencies**: Run `./setup_ats_deps.sh` again

---

**Key Feature**: Automatic validation ensures your resume stays ATS-compatible when you modify `resume.yml` or templates. 