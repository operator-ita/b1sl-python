# SAP B1 Python SDK - Testing & Development

.PHONY: help test test-vcr test-record test-demo test-ci coverage-html lint clean

# Default variables
PYTHONPATH := src:.
PYTEST := .venv/bin/pytest
VENV := .venv

help:
	@echo "Available commands:"
	@echo "  make test             - Run unit tests only (Fast, No network)"
	@echo "  make test-vcr         - Run integration tests with recorded cassettes (Offline)"
	@echo "  make test-record      - Record new VCR cassettes against a real SAP server (Requires .env)"
	@echo "  make test-demo        - Live smoke tests against SAP demo server (APP_ENV=demo)"
	@echo "  make test-ci          - Full test suite + coverage (for GitHub Actions)"
	@echo "  make coverage-html    - Run test-ci and open visual HTML gap analysis"
	@echo "  make lint             - Run static analysis (Ruff + Mypy)"
	@echo "  make clean            - Remove cache and temporary files"

test:
	@echo "🚀 Running unit tests (Layer 1)..."
	PYTHONPATH=$(PYTHONPATH) $(PYTEST) -m "not (integration or vcr)"

test-vcr:
	@echo "📽️  Running integration tests with VCR cassettes (Layer 2)..."
	PYTHONPATH=$(PYTHONPATH) $(PYTEST) -m "vcr" --record-mode=none

test-record:
	@if [ ! -f .env ]; then echo "❌ Error: .env file required for recording."; exit 1; fi
	@echo "🔴 Recording new cassettes... (Requires connection to SAP)"
	PYTHONPATH=$(PYTHONPATH) $(PYTEST) -m "vcr" --record-mode=all

test-demo:
	@if [ ! -f .env ]; then echo "❌ Error: .env file required for demo tests."; exit 1; fi
	@echo "🏗️  Running live smoke tests against demo server..."
	APP_ENV=demo PYTHONPATH=$(PYTHONPATH) $(PYTEST) -m "integration"

test-ci:
	@echo "⛓️ Running full CI suite (Unit + VCR + Coverage)..."
	PYTHONPATH=$(PYTHONPATH) $(PYTEST) -m "not integration" --cov=src --cov-report=xml --cov-report=term

coverage-html: test-ci
	@echo "📊 Generating visual coverage report..."
	.venv/bin/coverage html -d htmlcov/
	@if [ "$$(uname)" = "Darwin" ]; then open htmlcov/index.html; \
	 elif [ "$$(expr substr $$(uname -s) 1 5)" = "Linux" ]; then xdg-open htmlcov/index.html; \
	 else echo "Open htmlcov/index.html manually to see report."; fi

lint:
	@echo "🧹 Linting code..."
	$(VENV)/bin/ruff check src tests
	$(VENV)/bin/mypy src

# Release automation (Pro mode)
# Usage: make release v=0.1.x
release: lint test
	@if [ -z "$(v)" ]; then \
		echo "❌ Error: Version required. Example: make release v=0.1.2"; \
		exit 1; \
	fi
	@echo "🚀 Preparing release v$(v)..."
	git add .
	git commit -m "chore: Release v$(v) - Automated build"
	git tag -a v$(v) -m "v$(v)"
	@echo "📤 Pushing to GitHub (Branch main + Tags)..."
	git push origin main --tags
	@echo "✅ Done! GitHub Actions will handle the PyPI publication."

clean:
	@echo "🧹 Cleaning temporary files..."
	rm -rf .pytest_cache .mypy_cache .coverage htmlcov .ruff_cache coverage.xml
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
