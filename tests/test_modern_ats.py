"""Modern ATS compatibility tests using the new package structure."""

import pytest
import yaml
from pathlib import Path
from typing import Dict

from resume_ats import ResumeBuilder, CVExtractor
from resume_ats.models import BuildConfig, ResumeData
from resume_ats.exceptions import ExtractionError


class TestResumeBuilder:
    """Tests for the ResumeBuilder class."""
    
    @pytest.fixture
    def sample_yaml_data(self) -> Dict:
        """Sample resume data for testing."""
        return {
            'basics': {
                'name': 'Test User',
                'email': 'test@example.com',
                'label': 'DevOps Engineer',
                'location': 'Test City',
            },
            'work': [],
            'skills': ['Python', 'Docker', 'Kubernetes'],
        }
    
    @pytest.fixture
    def temp_yaml_file(self, tmp_path: Path, sample_yaml_data: Dict) -> Path:
        """Create a temporary YAML file for testing."""
        yaml_file = tmp_path / "test_resume.yml"
        with yaml_file.open('w', encoding='utf-8') as f:
            yaml.dump(sample_yaml_data, f)
        return yaml_file
    
    def test_load_data_valid_yaml(self, temp_yaml_file: Path):
        """Test loading valid YAML data."""
        builder = ResumeBuilder()
        builder.load_data(temp_yaml_file)
        
        assert builder.data.basics.name == "Test User"
        assert builder.data.basics.email == "test@example.com"
        assert len(builder.data.skills) == 3
    
    def test_from_yaml_class_method(self, temp_yaml_file: Path):
        """Test creating builder from YAML file."""
        builder = ResumeBuilder.from_yaml(temp_yaml_file)
        
        assert isinstance(builder.data, ResumeData)
        assert builder.data.basics.name == "Test User"
    
    def test_render_template_basic(self, temp_yaml_file: Path, tmp_path: Path):
        """Test basic template rendering."""
        # Create a simple template
        template_dir = tmp_path / "templates"
        template_dir.mkdir()
        
        template_file = template_dir / "test.txt"
        template_file.write_text("Hello {{ basics.name }}!")
        
        config = BuildConfig(template_dir=template_dir)
        builder = ResumeBuilder.from_yaml(temp_yaml_file, config)
        
        result = builder.render_template("test.txt")
        assert result == "Hello Test User!"


@pytest.mark.ats
class TestATSCompatibility:
    """ATS compatibility tests using the new extractor."""
    
    @pytest.fixture
    def resume_data(self) -> Dict:
        """Load resume data from the actual YAML file."""
        resume_path = Path(__file__).parent.parent / "resume.yml"
        if not resume_path.exists():
            pytest.skip("resume.yml not found")
        
        with resume_path.open('r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    @pytest.fixture
    def cv_extractor(self) -> CVExtractor:
        """Create extractor for the generated PDF."""
        pdf_path = Path(__file__).parent.parent / "build" / "Mathéo_Guilloux_CV.pdf"
        if not pdf_path.exists():
            pytest.skip(f"PDF not found: {pdf_path}")
        
        return CVExtractor(pdf_path)
    
    def test_pdf_exists(self):
        """Verify the PDF exists."""
        pdf_path = Path(__file__).parent.parent / "build" / "Mathéo_Guilloux_CV.pdf"
        assert pdf_path.exists(), f"PDF not found: {pdf_path}"
    
    def test_text_extraction(self, cv_extractor: CVExtractor):
        """Verify text can be extracted."""
        assert len(cv_extractor.text) > 100, "Extracted text too short"
        assert "devops" in cv_extractor.text.lower(), "DevOps term not found"
    
    def test_name_extraction(self, cv_extractor: CVExtractor, resume_data: Dict):
        """Test name extraction accuracy."""
        expected_name = resume_data['basics']['name']
        extracted_data = cv_extractor.extract_all()
        
        assert extracted_data.name, "Name not extracted"
        assert expected_name.lower() in extracted_data.name.lower(), \
            f"Expected '{expected_name}' not found in '{extracted_data.name}'"
    
    def test_email_extraction(self, cv_extractor: CVExtractor, resume_data: Dict):
        """Test email extraction accuracy."""
        expected_email = resume_data['basics']['email']
        extracted_data = cv_extractor.extract_all()
        
        assert extracted_data.email == expected_email, \
            f"Expected '{expected_email}', got '{extracted_data.email}'"
    
    def test_position_extraction(self, cv_extractor: CVExtractor, resume_data: Dict):
        """Test position extraction accuracy."""
        expected_position = resume_data['basics']['label']
        extracted_data = cv_extractor.extract_all()
        
        assert extracted_data.position, "Position not extracted"
        assert expected_position.lower() in extracted_data.position.lower(), \
            f"Expected '{expected_position}' not found in '{extracted_data.position}'"
    
    def test_skills_coverage(self, cv_extractor: CVExtractor, resume_data: Dict):
        """Test skills extraction coverage."""
        yaml_skills = resume_data.get('skills', [])
        extracted_data = cv_extractor.extract_all()
        
        if not yaml_skills:
            pytest.skip("No skills defined in YAML")
        
        # Extract all skills from the YAML structure
        all_yaml_skills = []
        for skill in yaml_skills:
            if isinstance(skill, dict) and 'keywords' in skill:
                # Skill object with keywords
                all_yaml_skills.extend(skill['keywords'])
            elif isinstance(skill, str):
                # String skill
                all_yaml_skills.append(skill)
        
        # Check for significant overlap
        yaml_skills_lower = {skill.lower() for skill in all_yaml_skills}
        extracted_skills_lower = {skill.lower() for skill in extracted_data.skills}
        
        overlap = yaml_skills_lower & extracted_skills_lower
        coverage = len(overlap) / len(yaml_skills_lower) if yaml_skills_lower else 0
        
        assert coverage >= 0.3, \
            f"Low skills coverage: {coverage:.1%} ({len(overlap)}/{len(yaml_skills_lower)})"
    
    def test_companies_extraction(self, cv_extractor: CVExtractor):
        """Test company extraction."""
        extracted_data = cv_extractor.extract_all()
        
        # Should find at least some companies
        assert len(extracted_data.companies) > 0, "No companies extracted"
        
        # Check for known companies (if they exist in your CV)
        known_companies = ['Continental', 'Airbus', 'OVH', 'Neverhack']
        found_companies = [c for c in known_companies 
                          if any(c.lower() in comp.lower() for comp in extracted_data.companies)]
        
        # At least one known company should be found
        assert len(found_companies) > 0, f"No known companies found in {extracted_data.companies}"


@pytest.mark.unit
class TestCVExtractor:
    """Unit tests for CVExtractor functionality."""
    
    def test_extractor_initialization_nonexistent_file(self):
        """Test extractor with non-existent file."""
        with pytest.raises(ExtractionError):
            CVExtractor(Path("nonexistent.pdf"))
    
    def test_email_pattern_matching(self):
        """Test email pattern matching logic."""
        # This would require a mock or test PDF, skipping for now
        pytest.skip("Requires test PDF file")


@pytest.mark.integration
class TestEndToEnd:
    """End-to-end integration tests."""
    
    def test_full_build_and_validation_pipeline(self, tmp_path: Path):
        """Test complete build and validation pipeline."""
        # Create test resume data
        resume_data = {
            'basics': {
                'name': 'Integration Test',
                'email': 'test@integration.com',
                'label': 'Test Engineer',
            },
            'skills': ['Python', 'Testing'],
        }
        
        # Write to temp YAML
        yaml_file = tmp_path / "test_resume.yml"
        with yaml_file.open('w', encoding='utf-8') as f:
            yaml.dump(resume_data, f)
        
        # Setup build configuration
        config = BuildConfig(
            output_dir=tmp_path / "output",
            formats=["json"]  # Use JSON for easier testing
        )
        
        # Build
        builder = ResumeBuilder.from_yaml(yaml_file, config)
        results = builder.build_all()
        
        # Verify output
        assert "json" in results
        json_path = results["json"]
        assert json_path.exists()
        
        # Verify content
        import json
        with json_path.open('r', encoding='utf-8') as f:
            output_data = json.load(f)
        
        assert output_data['basics']['name'] == 'Integration Test'
        assert output_data['basics']['email'] == 'test@integration.com' 