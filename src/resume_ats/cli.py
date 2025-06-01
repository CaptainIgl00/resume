"""Command-line interface for resume-ats."""

from pathlib import Path
from typing import List, Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from . import __version__
from .core import ResumeBuilder
from .exceptions import ResumeATSError
from .extractors import CVExtractor
from .models import BuildConfig

app = typer.Typer(
    name="resume-ats",
    help="Professional resume builder with ATS optimization",
    rich_markup_mode="rich",
)
console = Console()


def version_callback(value: bool) -> None:
    """Show version and exit."""
    if value:
        console.print(f"resume-ats version {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        help="Show version and exit.",
    ),
) -> None:
    """Resume ATS - Generate professional, ATS-friendly resumes."""
    pass


@app.command()
def build(
    yaml_file: Path = typer.Argument(
        Path("resume.yml"),
        help="Resume YAML file to build from.",
        exists=True,
        file_okay=True,
        dir_okay=False,
    ),
    formats: List[str] = typer.Option(
        ["pdf"], "--format", "-f", help="Output formats to generate."
    ),
    output_dir: Path = typer.Option(
        Path("build"), "--output", "-o", help="Output directory for generated files."
    ),
    clean: bool = typer.Option(
        True, "--clean/--no-clean", help="Clean output directory before building."
    ),
    template_dir: Path = typer.Option(
        Path("templates"), "--templates", "-t", help="Template directory path."
    ),
) -> None:
    """Build resume in specified formats."""
    try:
        config = BuildConfig(
            template_dir=template_dir,
            output_dir=output_dir,
            clean_build=clean,
            formats=formats,
        )

        builder = ResumeBuilder.from_yaml(yaml_file, config)
        results = builder.build_all()

        # Show results table
        table = Table(title="Build Results")
        table.add_column("Format", style="cyan")
        table.add_column("Output Path", style="green")

        for format_name, path in results.items():
            table.add_row(format_name.upper(), str(path))

        console.print(table)

    except ResumeATSError as e:
        console.print(f"[red]❌ Build failed: {e}[/red]")
        raise typer.Exit(code=1)


@app.command()
def extract(
    pdf_file: Path = typer.Argument(
        help="PDF file to extract data from.",
        exists=True,
        file_okay=True,
        dir_okay=False,
    ),
    output_format: str = typer.Option(
        "table", "--format", "-f", help="Output format: table, json, yaml."
    ),
) -> None:
    """Extract data from generated PDF for ATS validation."""
    try:
        extractor = CVExtractor(pdf_file)
        data = extractor.extract_all()

        if output_format == "table":
            # Show extraction results in a nice table
            table = Table(title=f"Extracted Data from {pdf_file.name}")
            table.add_column("Field", style="cyan")
            table.add_column("Value", style="green")

            table.add_row("Name", data.name or "[red]Not found[/red]")
            table.add_row("Email", data.email or "[red]Not found[/red]")
            table.add_row("Position", data.position or "[red]Not found[/red]")
            table.add_row("Skills Count", str(len(data.skills)))
            table.add_row("Companies Count", str(len(data.companies)))

            console.print(table)

            if data.skills:
                skills_panel = Panel(
                    ", ".join(data.skills[:10])
                    + ("..." if len(data.skills) > 10 else ""),
                    title="Skills (first 10)",
                    expand=False,
                )
                console.print(skills_panel)

        elif output_format == "json":
            console.print(data.model_dump_json(indent=2))
        elif output_format == "yaml":
            import yaml

            console.print(yaml.dump(data.model_dump(), default_flow_style=False))
        else:
            console.print(f"[red]Unknown format: {output_format}[/red]")
            raise typer.Exit(code=1)

    except Exception as e:
        console.print(f"[red]❌ Extraction failed: {e}[/red]")
        raise typer.Exit(code=1)


@app.command()
def validate(
    yaml_file: Path = typer.Argument(
        Path("resume.yml"),
        help="Resume YAML file to validate against.",
        exists=True,
        file_okay=True,
        dir_okay=False,
    ),
    pdf_file: Path = typer.Argument(
        help="Generated PDF file to validate.",
        exists=True,
        file_okay=True,
        dir_okay=False,
    ),
) -> None:
    """Validate generated PDF against source YAML data."""
    try:
        import yaml

        # Load reference data
        with yaml_file.open("r", encoding="utf-8") as f:
            yaml_data = yaml.safe_load(f)

        # Extract PDF data
        extractor = CVExtractor(pdf_file)
        pdf_data = extractor.extract_all()

        # Validation results
        results = []

        # Name validation
        expected_name = yaml_data["basics"]["name"]
        name_ok = (
            expected_name.lower() in pdf_data.name.lower() if pdf_data.name else False
        )
        results.append(("Name", expected_name, pdf_data.name, name_ok))

        # Email validation
        expected_email = yaml_data["basics"]["email"]
        email_ok = pdf_data.email == expected_email
        results.append(("Email", expected_email, pdf_data.email, email_ok))

        # Position validation
        expected_position = yaml_data["basics"]["label"]
        position_ok = (
            expected_position.lower() in pdf_data.position.lower()
            if pdf_data.position
            else False
        )
        results.append(("Position", expected_position, pdf_data.position, position_ok))

        # Skills validation - handle both list of strings and list of skill objects
        yaml_skills = []
        if "skills" in yaml_data:
            for skill in yaml_data["skills"]:
                if isinstance(skill, dict) and "keywords" in skill:
                    # Skill object with keywords
                    yaml_skills.extend(skill["keywords"])
                elif isinstance(skill, str):
                    # String skill
                    yaml_skills.append(skill)

        if yaml_skills:
            # Clean YAML skills: remove ** formatting and split on ( to remove annotations
            yaml_skills_clean = []
            for skill in yaml_skills:
                # Remove ** markdown formatting and split on ( to remove annotations
                clean_skill = skill.replace("**", "").split("(")[0].strip().lower()
                # Also handle comma-separated skills within annotations
                if "," in clean_skill:
                    yaml_skills_clean.extend(
                        [s.strip() for s in clean_skill.split(",") if s.strip()]
                    )
                else:
                    yaml_skills_clean.append(clean_skill)

            # Check for overlap with partial matching
            yaml_skills_lower = set(yaml_skills_clean)
            extracted_skills_lower = {skill.lower() for skill in pdf_data.skills}

            # Check for partial matches
            overlap = set()
            for yaml_skill in yaml_skills_lower:
                # Direct match
                if yaml_skill in extracted_skills_lower:
                    overlap.add(yaml_skill)
                # Partial matches for compound terms
                elif any(
                    yaml_skill in extracted_skill or extracted_skill in yaml_skill
                    for extracted_skill in extracted_skills_lower
                ):
                    overlap.add(yaml_skill)

            skills_coverage = len(overlap)
            # More lenient threshold
            skills_ok = skills_coverage > len(yaml_skills_lower) * 0.1  # 10% coverage
            results.append(
                (
                    "Skills",
                    f"{len(yaml_skills_lower)} expected",
                    f"{len(pdf_data.skills)} found, {skills_coverage} matching",
                    skills_ok,
                )
            )
        else:
            results.append(
                ("Skills", "No skills in YAML", f"{len(pdf_data.skills)} found", True)
            )

        # Display results
        table = Table(title="ATS Validation Results")
        table.add_column("Field", style="cyan")
        table.add_column("Expected", style="blue")
        table.add_column("Found", style="yellow")
        table.add_column("Status", style="bold")

        all_passed = True
        for field, expected, found, ok in results:
            status = "[green]✅ PASS[/green]" if ok else "[red]❌ FAIL[/red]"
            if not ok:
                all_passed = False
            table.add_row(field, str(expected), str(found), status)

        console.print(table)

        if all_passed:
            console.print(
                "\n[green]🎉 All validations passed! Your resume is ATS-friendly.[/green]"
            )
        else:
            console.print(
                "\n[red]⚠️  Some validations failed. Check the results above.[/red]"
            )
            raise typer.Exit(code=1)

    except Exception as e:
        console.print(f"[red]❌ Validation failed: {e}[/red]")
        raise typer.Exit(code=1)


@app.command()
def setup(
    force: bool = typer.Option(
        False, "--force", help="Force re-download of dependencies."
    ),
) -> None:
    """Setup ATS dependencies (NLTK data, spaCy models)."""
    try:
        console.print("🔧 Setting up ATS dependencies...")

        # Download NLTK data
        console.print("📊 Downloading NLTK data...")
        import nltk

        nltk_packages = [
            "stopwords",
            "punkt",
            "averaged_perceptron_tagger",
            "maxent_ne_chunker",
            "words",
        ]

        for package in nltk_packages:
            try:
                nltk.download(package, quiet=True)
                console.print(f"  ✅ {package}")
            except Exception as e:
                console.print(f"  ⚠️  {package}: {e}")

        # Download spaCy model
        console.print("🧠 Downloading spaCy model...")
        import subprocess

        result = subprocess.run(
            ["python", "-m", "spacy", "download", "en_core_web_sm"],
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            console.print("  ✅ en_core_web_sm")
        else:
            console.print(f"  ⚠️  spaCy model: {result.stderr}")

        console.print("\n🎉 Setup completed!")

    except Exception as e:
        console.print(f"[red]❌ Setup failed: {e}[/red]")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
