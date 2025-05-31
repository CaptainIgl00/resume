# ATS-Friendly Resume Generator

A modern, automated resume generation system that creates ATS (Applicant Tracking System) optimized resumes in multiple formats from a single YAML source file.

## 🚀 Features

- **Multi-format Output**: Generate PDF, HTML, and JSON versions of your resume
- **ATS Optimization**: Clean, structured output that ATS systems can easily parse
- **Single Source of Truth**: Maintain all resume data in one YAML file
- **Professional Templates**: Beautiful, modern design using the Awesome CV LaTeX class
- **Automated Build**: Simple Python script to generate all formats at once
- **Version Control Friendly**: Track changes to your resume over time

## 📋 Prerequisites

### Required Software

- **Python 3.x** with the following packages:
  ```bash
  pip install pyyaml jinja2
  ```

- **LaTeX Distribution** (for PDF generation):
  ```bash
  # Ubuntu/Debian
  sudo apt update
  sudo apt install texlive-xetex texlive-latex-extra texlive-fonts-recommended texlive-fonts-extra latexmk

  # macOS (with Homebrew)
  brew install --cask mactex

  # Windows
  # Download and install MikTeX or TeX Live
  ```

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd resume
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   # or create a virtual environment:
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install pyyaml jinja2
   ```

3. **Verify LaTeX installation**:
   ```bash
   xelatex --version
   latexmk --version
   ```

## 📝 Usage

### Basic Commands

Generate all formats:
```bash
python3 build.py
# or
python3 build.py all
```

Generate specific formats:
```bash
python3 build.py pdf    # PDF only
python3 build.py html   # HTML only
python3 build.py txt    # JSON only
```

Using Make (if available):
```bash
make all    # Generate all formats
make pdf    # PDF only
make html   # HTML only
make clean  # Clean build directory
```

### Customizing Your Resume

1. **Edit the resume data** in `resume.yml`:
   ```yaml
   basics:
     name: "Your Name"
     label: "Your Job Title"
     email: "your.email@example.com"
     # ... more fields
   ```

2. **Run the build script**:
   ```bash
   python3 build.py
   ```

3. **Find your generated files** in the `build/` directory:
   - `YourName_CV.pdf` - Professional PDF resume
   - `index.html` - Web-friendly HTML version
   - `resume.json` - Structured JSON for ATS systems

## 📁 Project Structure

```
resume/
├── build.py              # Main build script
├── resume.yml            # Resume data (YAML format)
├── templates/            # Jinja2 templates
│   ├── awesomecv.tex.j2 # LaTeX template for PDF
│   ├── simple.html.j2   # HTML template
│   └── awesome-cv.cls   # Awesome CV LaTeX class
├── build/               # Generated output files
├── Makefile            # Alternative build commands
└── README.md           # This file
```

## 🎯 ATS Optimization Features

This generator creates ATS-friendly resumes by:

- **Clean Structure**: Using semantic sections and consistent formatting
- **Standard Fonts**: Professional, widely-supported typefaces
- **Logical Order**: Following conventional resume section ordering
- **Keyword Optimization**: Easy to add relevant keywords in YAML format
- **Multiple Formats**: Providing JSON backup for maximum compatibility
- **No Complex Graphics**: Avoiding elements that confuse ATS parsers

## 🔧 Customization

### Templates

- **PDF Template**: Modify `templates/awesomecv.tex.j2` for LaTeX/PDF output
- **HTML Template**: Edit `templates/simple.html.j2` for web version
- **Add New Templates**: Create additional `.j2` files and update `build.py`

### Styling

- **Colors**: Modify the `\definecolor{awesome}{HTML}{007ACC}` line in the LaTeX template
- **Fonts**: Change `\setmainfont{Helvetica Neue}` to your preferred font
- **Layout**: Adjust spacing and sections in the template files

### Data Schema

The `resume.yml` file follows the [JSON Resume](https://jsonresume.org/) schema for compatibility:

- `basics`: Personal information and contact details
- `work`: Professional experience
- `education`: Academic background
- `skills`: Technical and soft skills
- `projects`: Personal or professional projects
- `languages`: Language proficiencies
- `references`: Professional references

## 🚨 Troubleshooting

### Common Issues

1. **LaTeX compilation errors**:
   - Ensure all LaTeX packages are installed
   - Check that fonts are available on your system
   - Run `python3 build.py html` to test non-LaTeX functionality

2. **Font not found errors**:
   - Install the required fonts or modify the template to use system fonts
   - Common alternatives: Arial, Calibri, or system defaults

3. **Permission errors**:
   - Ensure you have write permissions in the project directory
   - Check that the `build/` directory exists and is writable

### Getting Help

- Check the build logs in `build/resume.log` for detailed error messages
- Verify your YAML syntax with an online YAML validator
- Test with minimal data first, then gradually add content

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- [Awesome CV](https://github.com/posquit0/Awesome-CV) - LaTeX template for beautiful resumes
- [JSON Resume](https://jsonresume.org/) - Standard schema for resume data
- [Jinja2](https://jinja.palletsprojects.com/) - Template engine for Python

---

**Note**: This generator creates professional resumes optimized for both human recruiters and ATS systems. Always review the generated output and customize the content to match your specific experience and target roles. 