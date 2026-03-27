# Makefile for VMAnalyzer
.PHONY: all install uninstall test lint format clean dev-install
all: install
install:
	pip3 install -e .
uninstall:
	pip3 uninstall -y vm-analyzer
test:
	pytest tests/unit/ -v
test-integration:
	pytest tests/integration/ -v
lint:
	flake8 .
	black --check .
	isort --check .
format:
	black .
	isort .
clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	rm -rf build dist *.egg-info
	rm -rf .pytest_cache .coverage htmlcov
dev-install: install
	pip3 install -r requirements-dev.txt
pre-commit-install:
	pre-commit install
pre-commit-run:
	pre-commit run --all-files
docker-build:
	docker build -t vm-analyzer .
docker-run:
	docker-compose up -d
docker-stop:
	docker-compose down

# Additional targets
check:
	@echo "Running environment check..."
	@bash check_env.sh

clean:
	@echo "Cleaning up..."
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "Cleanup completed"

dev-setup:
	@echo "Setting up development environment..."
	@pip3 install -r requirements-dev.txt
	@pre-commit install
	@echo "Development environment ready"
