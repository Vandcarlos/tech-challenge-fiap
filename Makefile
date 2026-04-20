# Makefile for Python project setup

PYTHON_MIN_VERSION = 3.13
VENV_DIR = .venv

.PHONY: help
help:
	@echo "Available targets:"
	@echo "  setup-project    Install base project dependencies"
	@echo "  setup-dev        Install dev dependencies"
	@echo "  setup-tests      Install test dependencies"
	@echo "  setup-notebooks  Install notebook dependencies"
	@echo "  test             Run pytest with 90% min coverage (override: MIN_COVERAGE=X)"
	@echo "  test-verbose     Run pytest verbose with 90% min coverage"
	@echo "  activate         Show how to activate virtual environment"
	@echo "  check-python     Check Python version"
	@echo "  venv             Create virtual environment if not exists"

.PHONY: check-python
check-python:
	@if [ ! -f .python-version ]; then \
		echo ".python-version file not found"; \
		exit 1; \
	fi; \
	required_version=$$(cat .python-version | cut -d. -f1-2); \
	python_version=$$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"); \
	if [ $$(echo "$$python_version >= $$required_version" | bc -l) -eq 0 ]; then \
		echo "Python version $$python_version is too old. Need >= $$required_version"; \
		exit 1; \
	fi

.PHONY: venv
venv:
	@if [ ! -d $(VENV_DIR) ]; then \
		echo "Creating virtual environment..."; \
		python3 -m venv $(VENV_DIR); \
	fi

.PHONY: activate
activate:
	@echo "To activate the virtual environment, run: source $(VENV_DIR)/bin/activate"

.PHONY: setup-project
setup-project: check-python venv
	@echo "Installing project dependencies..."; \
	. $(VENV_DIR)/bin/activate && pip install -e .

.PHONY: setup-dev
setup-dev: check-python venv
	@echo "Installing dev dependencies (includes project base, tests, notebooks)..."; \
	. $(VENV_DIR)/bin/activate && pip install -e ".[dev,tests,notebooks]"

.PHONY: setup-tests
setup-tests: check-python venv
	@echo "Installing test dependencies..."; \
	. $(VENV_DIR)/bin/activate && pip install -e ".[tests]"

.PHONY: setup-notebooks
setup-notebooks: check-python venv
	@echo "Installing notebook dependencies..."; \
	. $(VENV_DIR)/bin/activate && pip install -e ".[notebooks]"

.PHONY: test
test: check-python
	@MIN_COVERAGE=$(MIN_COVERAGE); \
	if [ -z "$$MIN_COVERAGE" ]; then MIN_COVERAGE=90; fi; \
	. $(VENV_DIR)/bin/activate && pytest --cov-fail-under=$$MIN_COVERAGE

.PHONY: test-verbose
test-verbose: check-python
	@MIN_COVERAGE=$(MIN_COVERAGE); \
	if [ -z "$$MIN_COVERAGE" ]; then MIN_COVERAGE=90; fi; \
	. $(VENV_DIR)/bin/activate && pytest --cov-fail-under=$$MIN_COVERAGE -vv
