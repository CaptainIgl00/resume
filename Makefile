# Modern Python-based Makefile for resume-ats

.PHONY: help install install-dev build test validate clean setup lint format type-check docs

# Default Python and package manager
PYTHON ?= python3
PIP ?= pip
PACKAGE = resume-ats

# Colors for output
CYAN = \033[0;36m
GREEN = \033[0;32m
YELLOW = \033[0;33m
RED = \033[0;31m
NC = \033[0m # No Color

help: ## Show this help message
	@echo "$(CYAN)Available commands:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2}'

install: ## Install package in development mode
	@echo "$(CYAN)📦 Installing package in development mode...$(NC)"
	$(PIP) install -e .

install-dev: ## Install with development dependencies
	@echo "$(CYAN)🔧 Installing development dependencies...$(NC)"
	$(PIP) install -e ".[dev,test,ats]"

install-ats: ## Install ATS dependencies only
	@echo "$(CYAN)🤖 Installing ATS dependencies...$(NC)"
	$(PIP) install -e ".[ats]"

setup: install-ats ## Setup ATS dependencies (NLTK, spaCy)
	@echo "$(CYAN)⚙️  Setting up ATS dependencies...$(NC)"
	$(PYTHON) -m resume_ats.cli setup

# Building
build: ## Build resume (PDF by default)
	@echo "$(CYAN)🏗️  Building resume...$(NC)"
	$(PYTHON) -m resume_ats.cli build

build-all: ## Build all formats (PDF, HTML, JSON)
	@echo "$(CYAN)📄 Building all formats...$(NC)"
	$(PYTHON) -m resume_ats.cli build --format pdf --format html --format json

# Testing and validation
test: ## Run all tests
	@echo "$(CYAN)🧪 Running tests...$(NC)"
	pytest

test-verbose: ## Run tests with verbose output
	@echo "$(CYAN)🔍 Running tests (verbose)...$(NC)"
	pytest -v -s

test-ats: ## Run ATS compatibility tests only
	@echo "$(CYAN)🤖 Running ATS tests...$(NC)"
	pytest -m ats -v

validate: ## Validate generated PDF against YAML
	@echo "$(CYAN)✅ Validating ATS compatibility...$(NC)"
	$(PYTHON) -m resume_ats.cli validate resume.yml build/Mathéo_Guilloux_CV.pdf

extract: ## Extract data from generated PDF
	@echo "$(CYAN)📊 Extracting PDF data...$(NC)"
	$(PYTHON) -m resume_ats.cli extract build/Mathéo_Guilloux_CV.pdf

# Development tools
lint: ## Run linting (ruff)
	@echo "$(CYAN)🔍 Running linter...$(NC)"
	ruff check src/ tests/

format: ## Format code (black + ruff)
	@echo "$(CYAN)🎨 Formatting code...$(NC)"
	black src/ tests/
	ruff check --fix src/ tests/

type-check: ## Run type checking (mypy)
	@echo "$(CYAN)🔍 Type checking...$(NC)"
	mypy src/resume_ats/

# Quality checks
check: lint type-check test ## Run all quality checks

# Utility
clean: ## Clean build artifacts
	@echo "$(CYAN)🧹 Cleaning build artifacts...$(NC)"
	rm -rf build/ dist/ *.egg-info/ .pytest_cache/ .coverage htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

clean-all: clean ## Clean everything including venv
	@echo "$(CYAN)🗑️  Cleaning everything...$(NC)"
	rm -rf .venv/

# Watch for changes (requires entr)
watch: ## Auto-rebuild on file changes
	@echo "$(CYAN)👀 Watching for changes...$(NC)"
	find . -name '*.yml' -o -name '*.yaml' -o -name '*.j2' | entr -c make build

# Docker support (optional)
docker-build: ## Build Docker image
	@echo "$(CYAN)🐳 Building Docker image...$(NC)"
	docker build -t $(PACKAGE) .

docker-run: ## Run in Docker container
	@echo "$(CYAN)🐳 Running in Docker...$(NC)"
	docker run --rm -v $(PWD):/workspace $(PACKAGE)

# Package management
dist: ## Build distribution packages
	@echo "$(CYAN)📦 Building distribution...$(NC)"
	$(PYTHON) -m build

publish-test: dist ## Publish to test PyPI
	@echo "$(CYAN)🚀 Publishing to test PyPI...$(NC)"
	twine upload --repository testpypi dist/*

publish: dist ## Publish to PyPI
	@echo "$(CYAN)🚀 Publishing to PyPI...$(NC)"
	twine upload dist/*

# Legacy compatibility
pdf: build ## Legacy: build PDF (alias for build)
html: ## Legacy: build HTML
	$(PYTHON) -m resume_ats.cli build --format html

# Show current status
status: ## Show project status
	@echo "$(CYAN)📊 Project Status:$(NC)"
	@echo "  Package: $(PACKAGE)"
	@echo "  Python: $(shell $(PYTHON) --version)"
	@echo "  Virtual env: $(VIRTUAL_ENV)"
	@if [ -f "resume.yml" ]; then echo "  ✅ resume.yml found"; else echo "  ❌ resume.yml missing"; fi
	@if [ -d "templates" ]; then echo "  ✅ templates/ found"; else echo "  ❌ templates/ missing"; fi
	@if [ -d "build" ]; then echo "  ✅ build/ exists"; else echo "  ℹ️  build/ will be created"; fi 