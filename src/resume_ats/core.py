"""Core resume building functionality."""

import json
import shutil
import subprocess
import re
from pathlib import Path
from typing import Dict, Any, Optional

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from .models import ResumeData, BuildConfig
from .exceptions import BuildError, TemplateError, CompilationError


def process_bold_markdown(text: str) -> str:
    """Convert **text** markdown to LaTeX bold format and escape special chars.
    
    Args:
        text: Input text with **bold** markdown
        
    Returns:
        Text with LaTeX bold formatting and escaped special characters
    """
    if not isinstance(text, str):
        return text
    
    # First, escape special LaTeX characters
    text = text.replace('~', '\\textasciitilde{}')
    text = text.replace('&', '\\&')
    text = text.replace('%', '\\%')
    text = text.replace('$', '\\$')
    text = text.replace('#', '\\#')
    text = text.replace('^', '\\textasciicircum{}')
    text = text.replace('_', '\\_')
    text = text.replace('{', '\\{')
    text = text.replace('}', '\\}')
    
    # Then convert **text** to \textbf{text}
    return re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', text)


def process_links(text: str) -> str:
    r"""Convert URLs to clickable LaTeX href links.
    
    Args:
        text: Input text that may contain URLs
        
    Returns:
        Text with URLs converted to LaTeX \href{}{} format
    """
    if not isinstance(text, str):
        return text
    
    # Pattern to match http:// and https:// URLs
    url_pattern = r'(https?://[^\s]+)'
    
    def make_link(match):
        url = match.group(1)
        # Remove trailing punctuation that might not be part of the URL
        if url.endswith(('.', ',', ')', ']', '}', '!')):
            url = url[:-1]
        return f'\\href{{{url}}}{{{url}}}'
    
    return re.sub(url_pattern, make_link, text)


def process_bold_and_links(text: str) -> str:
    """Apply both bold markdown and link processing.
    
    Args:
        text: Input text with markdown and URLs
        
    Returns:
        Text with both bold formatting and clickable links
    """
    if not isinstance(text, str):
        return text
    
    # First, convert URLs to \href{}{} (before escaping special chars)
    url_pattern = r'(https?://[^\s]+)'
    
    def make_link(match):
        url = match.group(1)
        # Remove trailing punctuation that might not be part of the URL
        if url.endswith(('.', ',', ')', ']', '}', '!')):
            url = url[:-1]
        return f'\\href{{{url}}}{{{url}}}'
    
    text = re.sub(url_pattern, make_link, text)
    
    # Then escape special LaTeX characters (but preserve our \href commands)
    # We need to be careful not to escape the \ in \href
    text = text.replace('~', '\\textasciitilde{}')
    text = text.replace('&', '\\&')
    text = text.replace('%', '\\%')
    text = text.replace('$', '\\$')
    text = text.replace('#', '\\#')
    text = text.replace('^', '\\textasciicircum{}')
    text = text.replace('_', '\\_')
    
    # For { and }, we need to be careful not to break \href{url}{text}
    # Split on \href commands and process non-href parts separately
    parts = re.split(r'(\\href\{[^}]+\}\{[^}]+\})', text)
    processed_parts = []
    
    for i, part in enumerate(parts):
        if part.startswith('\\href{'):
            # This is an href command, don't escape it
            processed_parts.append(part)
        else:
            # This is regular text, escape { and }
            part = part.replace('{', '\\{')
            part = part.replace('}', '\\}')
            processed_parts.append(part)
    
    text = ''.join(processed_parts)
    
    # Finally convert **text** to \textbf{text}
    text = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', text)
    
    return text


class ResumeBuilder:
    """Main resume builder class."""
    
    def __init__(self, config: Optional[BuildConfig] = None):
        """Initialize the resume builder.
        
        Args:
            config: Build configuration. Uses defaults if None.
        """
        self.config = config or BuildConfig()
        self.console = Console()
        self._setup_jinja_env()
    
    def _setup_jinja_env(self) -> None:
        """Setup Jinja2 environment with custom filters."""
        self.jinja_env = Environment(
            loader=FileSystemLoader(str(self.config.template_dir)),
            autoescape=select_autoescape(["html", "xml"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        
        # Add custom filter for bold markdown processing
        self.jinja_env.filters['bold'] = process_bold_markdown
        self.jinja_env.filters['links'] = process_links
        self.jinja_env.filters['bold_and_links'] = process_bold_and_links
    
    @classmethod
    def from_yaml(cls, yaml_path: Path, config: Optional[BuildConfig] = None) -> 'ResumeBuilder':
        """Create builder from YAML file.
        
        Args:
            yaml_path: Path to resume YAML file
            config: Build configuration
            
        Returns:
            Configured ResumeBuilder instance
        """
        builder = cls(config)
        builder.load_data(yaml_path)
        return builder
    
    def load_data(self, yaml_path: Path) -> None:
        """Load resume data from YAML file.
        
        Args:
            yaml_path: Path to YAML file
            
        Raises:
            BuildError: If YAML cannot be loaded or validated
        """
        try:
            with yaml_path.open("r", encoding="utf-8") as f:
                raw_data = yaml.safe_load(f)
            
            # Validate with Pydantic
            self.data = ResumeData(**raw_data)
            self.console.print(f"✅ Loaded resume data from {yaml_path}")
            
        except Exception as e:
            raise BuildError(f"Failed to load resume data: {e}") from e
    
    def _prepare_build_dir(self) -> None:
        """Prepare build directory."""
        if self.config.clean_build and self.config.output_dir.exists():
            shutil.rmtree(self.config.output_dir)
        
        self.config.output_dir.mkdir(exist_ok=True)
        
        # Copy required assets
        self._copy_assets()
    
    def _copy_assets(self) -> None:
        """Copy required assets to build directory."""
        awesome_cv_cls = self.config.template_dir / "awesome-cv.cls"
        if awesome_cv_cls.exists():
            shutil.copy2(awesome_cv_cls, self.config.output_dir / "awesome-cv.cls")
        
        # Copy logos directory if it exists
        logos_dir = Path("logos")
        if logos_dir.exists():
            build_logos_dir = self.config.output_dir / "logos"
            if build_logos_dir.exists():
                shutil.rmtree(build_logos_dir)
            shutil.copytree(logos_dir, build_logos_dir)
    
    def render_template(self, template_name: str, **extra_context) -> str:
        """Render template with resume data.
        
        Args:
            template_name: Name of template file
            **extra_context: Additional context variables
            
        Returns:
            Rendered template content
            
        Raises:
            TemplateError: If template rendering fails
        """
        try:
            template = self.jinja_env.get_template(template_name)
            context = self.data.model_dump()
            context.update(extra_context)
            return template.render(**context)
        except Exception as e:
            raise TemplateError(f"Failed to render template {template_name}: {e}") from e
    
    def build_pdf(self) -> Path:
        """Build PDF resume.
        
        Returns:
            Path to generated PDF
            
        Raises:
            CompilationError: If LaTeX compilation fails
        """
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
        ) as progress:
            task = progress.add_task("Generating PDF...", total=None)
            
            try:
                # Render LaTeX
                tex_content = self.render_template("awesomecv.tex.j2")
                tex_path = self.config.output_dir / "resume.tex"
                tex_path.write_text(tex_content, encoding="utf-8")
                
                progress.update(task, description="Compiling LaTeX...")
                
                # Compile directly to PDF with XeLaTeX
                result = subprocess.run([
                    "xelatex",
                    "-interaction=nonstopmode", 
                    "-halt-on-error",
                    tex_path.name,
                ], cwd=self.config.output_dir, capture_output=True, text=True)
                
                if result.returncode != 0:
                    error_msg = f"XeLaTeX compilation failed (exit code {result.returncode})"
                    if result.stderr.strip():
                        error_msg += f"\nSTDERR:\n{result.stderr}"
                    if result.stdout.strip():
                        error_msg += f"\nSTDOUT:\n{result.stdout}"
                    
                    # Check for common errors
                    log_file = self.config.output_dir / "resume.log"
                    if log_file.exists():
                        log_content = log_file.read_text(encoding="utf-8", errors="ignore")
                        if "! Font" in log_content:
                            error_msg += "\n\nFont error detected. Make sure required fonts are installed."
                        elif "! LaTeX Error:" in log_content:
                            # Extract LaTeX error
                            lines = log_content.split('\n')
                            for i, line in enumerate(lines):
                                if "! LaTeX Error:" in line:
                                    error_msg += f"\n\nLaTeX Error: {line}"
                                    if i + 1 < len(lines):
                                        error_msg += f"\n{lines[i + 1]}"
                                    break
                    
                    raise CompilationError(error_msg)
                
                # Check if PDF was generated
                pdf_path = self.config.output_dir / "resume.pdf"
                if not pdf_path.exists():
                    raise CompilationError("PDF file was not generated by XeLaTeX")
                
                # Create final PDF with name
                final_name = f"{self.data.basics.name.replace(' ', '_')}_CV.pdf"
                final_path = self.config.output_dir / final_name
                shutil.copy2(pdf_path, final_path)
                
                progress.update(task, description="✅ PDF generated successfully")
                self.console.print(f"📄 PDF saved to: {final_path}")
                return final_path
                
            except FileNotFoundError as e:
                raise CompilationError(f"LaTeX tools not found: {e}") from e
            except Exception as e:
                raise CompilationError(f"PDF generation failed: {e}") from e
    
    def build_html(self) -> Path:
        """Build HTML resume.
        
        Returns:
            Path to generated HTML file
        """
        html_content = self.render_template("simple.html.j2")
        html_path = self.config.output_dir / "index.html"
        html_path.write_text(html_content, encoding="utf-8")
        
        self.console.print(f"🌐 HTML saved to: {html_path}")
        return html_path
    
    def build_json(self) -> Path:
        """Build JSON export of resume data.
        
        Returns:
            Path to generated JSON file
        """
        json_path = self.config.output_dir / "resume.json"
        json_content = self.data.model_dump_json(indent=2)
        json_path.write_text(json_content, encoding="utf-8")
        
        self.console.print(f"📋 JSON saved to: {json_path}")
        return json_path
    
    def build_all(self) -> Dict[str, Path]:
        """Build all configured formats.
        
        Returns:
            Dictionary mapping format names to output paths
        """
        self._prepare_build_dir()
        
        results = {}
        
        for format_name in self.config.formats:
            if format_name == "pdf":
                results["pdf"] = self.build_pdf()
            elif format_name == "html":
                results["html"] = self.build_html()
            elif format_name == "json":
                results["json"] = self.build_json()
            else:
                self.console.print(f"⚠️  Unknown format: {format_name}")
        
        self.console.print("🎉 Build completed successfully!")
        return results 