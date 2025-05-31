# Resume ATS - Générateur de CV optimisé ATS

🎯 **Générateur de CV professionnel optimisé pour les systèmes de suivi des candidatures (ATS)**

## ✨ Optimisations ATS Récentes

### 🔧 Améliorations du Template LaTeX
- **Polices compatibles** : Utilisation des polices système standard pour une compatibilité maximale
- **Marges optimisées** : Marges plus larges (2.2cm) pour une meilleure analyse du texte
- **Tailles de police** : Polices plus grandes et plus claires pour un meilleur parsing ATS
- **Couleurs simplifiées** : Schéma de couleurs professionnel avec bleu foncé (#1F4788)
- **Espacement amélioré** : Espacement optimisé pour la lisibilité et l'analyse automatique

### 📝 Gestion du Markdown Gras
- **Support `**texte**`** : Conversion automatique du markdown gras vers LaTeX `\textbf{}`
- **Échappement des caractères spéciaux** : Protection automatique des caractères LaTeX spéciaux
- **Filtre Jinja2 personnalisé** : Traitement intelligent du texte avec le filtre `| bold`

### 🎨 Structure ATS-Friendly
- **En-tête centré** : Meilleure détection des informations personnelles
- **Sections claires** : Séparateurs de section simplifiés pour l'ATS
- **Format d'entrée optimisé** : Structure `\cventry` adaptée pour l'extraction automatique
- **Listes propres** : Puces simples et espacement cohérent

### 📊 Résultats de Validation ATS
```
✅ Nom : Parfaitement extrait
✅ Email : Parfaitement extrait  
✅ Position : Parfaitement extrait
✅ Compétences : 36 compétences extraites (excellent score)
✅ Entreprises : 12 entreprises détectées
```

## 🚀 Utilisation

### Markdown Gras dans resume.yml
```yaml
basics:
  summary: |
    DevOps engineer with **3 years' experience** helping ESNs and startups...
    
work:
  - highlights:
      - "Developed services in **Python**, **Golang** and **Java**"
      - "Built **Vue.js + Grafana** monitoring dashboards"
      
skills:
  - name: "Programming Languages"
    keywords: ["**Python**", "**Go**", "**Java**"]
```

### Génération du CV
```bash
# Générer le CV optimisé ATS
python -m src.resume_ats.cli build

# Valider la compatibilité ATS
python -m src.resume_ats.cli validate resume.yml build/CV.pdf

# Extraire les données pour vérification
python -m src.resume_ats.cli extract build/CV.pdf
```

## 📋 Fonctionnalités

### Interface en Ligne de Commande Moderne

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
- 🚀 **CI/CD Integration**: Automated validation and release workflows

## 🔄 CI/CD Workflows

### 🤖 Automatic ATS Validation
Every push to `main` triggers:
- ✅ CV build and validation
- ✅ ATS compatibility testing
- ✅ Comprehensive test suite
- ✅ Artifact upload (PDF + reports)

### 🚀 Automated Releases
Create a tag to trigger automatic release:
```bash
git tag v1.0.0
git push origin v1.0.0
```

**Generated files in release:**
- `Mathéo_Guilloux_CV_v1.0.0.pdf`
- `resume_v1.0.0.html`
- `resume_v1.0.0.json`
- `ats-report_v1.0.0.json`
- `resume_complete_v1.0.0.zip`

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
├── .github/workflows/       # CI/CD workflows
│   ├── ats-validation.yml  # ATS validation on main
│   ├── release.yml         # Automated releases
│   └── test.yml            # Multi-platform testing
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

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

**Key Improvement**: This is now a proper Python package with modern tooling, type safety, comprehensive testing, a beautiful CLI interface, and full CI/CD automation while maintaining all original functionality.

## ✨ Modern Two-Column Design

The `awesomecv.tex.j2` template has been enhanced with a modern two-column layout that maintains full ATS compatibility:

### 🎨 Design Features

- **Two-Column Layout**: 25% left column for contact info, skills, languages, and references; 75% right column for main content
- **Professional Color Scheme**: 
  - `ats-blue` (#1F4788) for accents and name highlighting
  - `ats-lightblue` (#4A90E2) for clickable links
  - Clean gray dividers for section separation
- **Modern Typography**:
  - Roboto font for headers and titles
  - Source Sans Pro for body text
  - Optimized font sizes and spacing

### 🔧 Technical Improvements

- **ATS-Optimized**: Maintains 84%+ skills extraction coverage
- **Lightweight**: PDF output < 25KB (well under 500KB limit)
- **Font Embedding**: All fonts properly embedded for universal compatibility
- **Clean LaTeX**: Simplified template structure for better maintainability

### 📊 ATS Validation Results

All critical ATS tests pass:
- ✅ Name extraction: 100%
- ✅ Email extraction: 100% 
- ✅ Position extraction: 100%
- ✅ Company extraction: 100%
- ✅ Skills coverage: 84% (target: 30%+)

The new design successfully balances modern aesthetics with ATS parsing requirements. 