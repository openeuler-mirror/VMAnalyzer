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
