.PHONY: help install export run build docker-build docker-run clean

# Default target executed when no arguments are given to make
default: help

help:
	@echo "Available commands:"
	@echo "  make install         - Install dependencies"
	@echo "  make export          - Export dependencies to requirements.txt"
	@echo "  make run             - Run the FastAPI application"
	@echo "  make build           - Build the Python package"
	@echo "  make docker-build    - Build Docker image"
	@echo "  make docker-run      - Run Docker container"
	@echo "  make clean           - Clean up temporary files"

# Install dependencies
install:
	pip install -r requirements.txt

# Export dependencies to requirements.txt
export:
	uv export --format requirements-txt > requirements.txt

# Run the application
run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Build the Python package
build:
	python setup.py sdist bdist_wheel

# Build Docker image
docker-build:
	docker build -t orgsvc .

# Run Docker container
docker-run:
	docker run -p 8000:8000 orgsvc

# Clean up temporary files
clean:
	rm -rf __pycache__
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf dist
	rm -rf build
	find . -name "__pycache__" -type d -exec rm -rf {} +
	find . -name "*.pyc" -delete

uv_export:
	uv export --format requirements-txt > requirements.txt  

build_test:
	docker compose -f docker-compose-test.yml build --no-cache 

test:
	make uv_export && export ENV=test && docker compose -f docker-compose-test.yml run orgsvc-test pytest --disable-warnings -v /orgsvc/tests/ --asyncio-mode=auto\
		--cov=src \
		--cov-report term \
		--cov-report term-missing \
		--cov-report html
	docker compose stop