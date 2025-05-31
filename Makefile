# Makefile – Build targets for the CV

# Path configuration
PY     ?= python
BUILD  ?= build

.PHONY: pdf html txt all clean watch

all: pdf html txt

pdf:
	$(PY) build.py pdf

html:
	$(PY) build.py html

txt:
	$(PY) build.py txt

clean:
	rm -rf $(BUILD)/*

# Convenience target to auto-rebuild PDF on YAML/template changes (requires entr)
# Usage: make watch
watch:
	@find . -name '*.yaml' -o -name '*.j2' | entr -c make pdf
