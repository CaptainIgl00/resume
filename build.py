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
import subprocess
import sys
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).resolve().parent
TEMPLATES = ROOT / "templates"
BUILD_DIR = ROOT / "build"
BUILD_DIR.mkdir(exist_ok=True)


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
    """Render LaTeX and compile it to PDF using latexmk."""
    tex_source = render_template("awesomecv.tex.j2", data)
    tex_path = BUILD_DIR / "resume.tex"
    tex_path.write_text(tex_source, encoding="utf-8")

    # Compile with latexmk (fallback to xelatex if latexmk unavailable)
    print("[+] Compiling PDF…")
    try:
        subprocess.run([
            "latexmk",
            "-quiet",
            "-xelatex",
            tex_path.name,
        ], cwd=BUILD_DIR, check=True)
    except FileNotFoundError:
        subprocess.run([
            "xelatex",
            tex_path.name,
        ], cwd=BUILD_DIR, check=True)

    pdf_path = BUILD_DIR / "resume.pdf"
    # Rename with candidate name for convenience
    target = BUILD_DIR / f"{data['basics']['name'].replace(' ', '_')}_CV.pdf"
    target.write_bytes(pdf_path.read_bytes())
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
    args = parser.parse_args()

    data = load_data()

    if args.target in ("pdf", "all"):
        build_pdf(data)

    if args.target in ("html", "all"):
        build_html(data)

    if args.target in ("txt", "all"):
        build_txt(data)


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        print("[!] Build failed:", exc, file=sys.stderr)
        sys.exit(1)
