# Makefile – Build targets for the CV

# Path configuration
PY     ?= python
BUILD  ?= build

.PHONY: pdf html txt all clean watch setup-ats test-ats build-and-test test-legacy

all: pdf html txt

pdf:
	$(PY) build.py pdf

html:
	$(PY) build.py html

txt:
	$(PY) build.py txt

clean:
	rm -rf $(BUILD)/*

# ATS-friendly testing with pytest
setup-ats:
	@echo "🔧 Configuration des dépendances ATS..."
	@./setup_ats_deps.sh

test-ats:
	@echo "🧪 Test ATS-friendly du CV avec pytest..."
	@pytest tests/test_ats_compatibility.py -v

# Legacy ATS test (shell script)
test-legacy:
	@echo "🧪 Test ATS-friendly legacy..."
	@./test_ats_friendly.sh

# Build and test in one command
build-and-test: pdf test-ats
	@echo "✅ Build et test ATS terminés avec succès !"

# Convenience target to auto-rebuild PDF on YAML/template changes (requires entr)
# Usage: make watch
watch:
	@find . -name '*.yaml' -o -name '*.j2' | entr -c make pdf
