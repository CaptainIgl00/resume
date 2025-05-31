#!/usr/bin/env python3
"""build.py – Single-source CV generator

Convert resume.yml + Jinja2 templates into PDF (LaTeX) and HTML
Usage examples
--------------
$ python build.py pdf      # build build/Mathéo_Guilloux_CV.pdf
$ python build.py html     # build/build/index.html
$ python build.py all      # build everything

Dependencies:
  pip install pyyaml jinja2
  # For PDF generation, make sure xelatex or latexmk is installed.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).resolve().parent
TEMPLATES = ROOT / "templates"
BUILD_DIR = ROOT / "build"


def clean_build_dir():
    """Clean the build directory completely for a fresh start."""
    if BUILD_DIR.exists():
        print("[+] Cleaning build directory...")
        shutil.rmtree(BUILD_DIR)
    BUILD_DIR.mkdir(exist_ok=True)
    print("[✓] Build directory cleaned")


def copy_required_assets():
    """Copy required assets like awesome-cv.cls to build directory."""
    # Copy awesome-cv.cls if it exists in templates
    awesome_cv_cls = TEMPLATES / "awesome-cv.cls"
    if awesome_cv_cls.exists():
        shutil.copy2(awesome_cv_cls, BUILD_DIR / "awesome-cv.cls")
        print("[✓] Copied awesome-cv.cls to build directory")


def load_data(yaml_path: Path = ROOT / "resume.yml") -> dict:
    """Load resume data from YAML and return a python dict."""
    with yaml_path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    return data


def render_template(template_name: str, context: dict) -> str:
    """Render `template_name` located in ./templates using Jinja2."""
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES)),
        autoescape=select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template(template_name)
    return template.render(**context)


def build_pdf(data: dict) -> Path:
    """Render LaTeX and compile it to PDF using XeLaTeX."""
    tex_source = render_template("awesomecv.tex.j2", data)
    tex_path = BUILD_DIR / "resume.tex"
    tex_path.write_text(tex_source, encoding="utf-8")

    print("[+] Compiling PDF with XeLaTeX...")
    
    # Use XeLaTeX directly for better control and cleaner output
    try:
        # Run XeLaTeX to generate XDV
        result = subprocess.run([
            "xelatex",
            "-interaction=nonstopmode",
            "-no-pdf",
            "-halt-on-error",
            tex_path.name,
        ], cwd=BUILD_DIR, capture_output=True, text=True)
        
        # Check if XDV was created
        xdv_path = BUILD_DIR / "resume.xdv"
        if not xdv_path.exists() or result.returncode != 0:
            print(f"[!] XeLaTeX compilation failed.")
            print(f"[!] Exit code: {result.returncode}")
            if result.stderr.strip():
                print(f"[!] Error output:\n{result.stderr}")
            # Show relevant lines from log if available
            log_path = BUILD_DIR / "resume.log"
            if log_path.exists():
                print(f"[!] Check {log_path} for detailed error information")
            raise subprocess.CalledProcessError(result.returncode, "xelatex")
        
        # Convert XDV to PDF
        print("[+] Converting XDV to PDF...")
        result = subprocess.run([
            "xdvipdfmx",
            "-q",  # Quiet mode
            "resume.xdv"
        ], cwd=BUILD_DIR, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"[!] xdvipdfmx conversion failed.")
            print(f"[!] Exit code: {result.returncode}")
            if result.stderr.strip():
                print(f"[!] Error output:\n{result.stderr}")
            raise subprocess.CalledProcessError(result.returncode, "xdvipdfmx")
        
        pdf_path = BUILD_DIR / "resume.pdf"
        if not pdf_path.exists():
            raise RuntimeError("PDF conversion completed but no PDF file was generated")
            
    except FileNotFoundError as e:
        print(f"[!] Required tool not found: {e}")
        print("[!] Make sure XeLaTeX and xdvipdfmx are installed:")
        print("    sudo apt install texlive-xetex texlive-latex-extra texlive-fonts-extra")
        raise

    # Rename with candidate name for convenience
    target = BUILD_DIR / f"{data['basics']['name'].replace(' ', '_')}_CV.pdf"
    shutil.copy2(pdf_path, target)
    print(f"[✓] PDF written to {target.relative_to(ROOT)}")
    return target


def build_html(data: dict) -> Path:
    """Render a simple HTML version of the resume."""
    html_source = render_template("simple.html.j2", data)
    html_path = BUILD_DIR / "index.html"
    html_path.write_text(html_source, encoding="utf-8")
    print(f"[✓] HTML written to {html_path.relative_to(ROOT)}")
    return html_path


def build_txt(data: dict) -> Path:
    """Dump JSON (or TXT) for ATS fallback."""
    txt_path = BUILD_DIR / "resume.json"
    txt_path.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    print(f"[✓] JSON written to {txt_path.relative_to(ROOT)}")
    return txt_path


def main() -> None:
    parser = argparse.ArgumentParser(description="CV generator")
    parser.add_argument(
        "target",
        choices=["pdf", "html", "txt", "all"],
        nargs="?",
        default="all",
        help="What to build (default: all)",
    )
    parser.add_argument(
        "--no-clean",
        action="store_true",
        help="Skip cleaning the build directory (for debugging)",
    )
    args = parser.parse_args()

    # Clean build directory unless --no-clean is specified
    if not args.no_clean:
        clean_build_dir()
        copy_required_assets()

    try:
        data = load_data()
    except Exception as e:
        print(f"[!] Failed to load resume data: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        if args.target in ("pdf", "all"):
            build_pdf(data)

        if args.target in ("html", "all"):
            build_html(data)

        if args.target in ("txt", "all"):
            build_txt(data)
            
        print("\n[🎉] Build completed successfully!")
        
    except Exception as e:
        print(f"\n[!] Build failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
