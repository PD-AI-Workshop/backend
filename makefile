.PHONY: help install run test-unit test-integration test-api test-cov lint clean db-upgrade db-downgrade db-migrate

UVICORN = poetry run uvicorn
PYTEST = poetry run pytest
ALEMBIC = poetry run alembic
BLACK = poetry run black
FLAKE8 = poetry run flake8

help:
	@echo "Available commands:"
	@echo "  make install     	- Install dependencies"
	@echo "  make run         	- Run the application"
	@echo "  make test-unit   	- Run unit tests"
	@echo "  make test-integ  	- Run integration tests"
	@echo "  make test-api  	- Run api tests"
	@echo "  make test-cov    	- Run tests with coverage"
	@echo "  make lint        	- Run code style checks"
	@echo "  make clean       	- Clean cache and temporary files"
	@echo "  make db-upgrade  	- Upgrade database to latest revision"
	@echo "  make db-downgrade 	- Downgrade database one revision"
	@echo "  make db-migrate  	- Create new migration"
	@echo "  make db-history  	- Show migration history"

install:
	poetry install --no-root

run:
	python3 main.py

test-unit:
	$(PYTEST) ./tests/unit/

test-integ:
	$(PYTEST) ./tests/integration/

test-api:
	$(PYTEST) ./tests/api/

lint:
	$(FLAKE8) . --max-line-length=88
	$(BLACK) . --check

db-upgrade:
	$(ALEMBIC) upgrade head

db-downgrade:
	$(ALEMBIC) downgrade -1

db-migrate:
	@read -p "Enter migration message: " msg; \
	$(ALEMBIC) revision --autogenerate -m "$$msg"

db-history:
	$(ALEMBIC) history --verbose

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -delete
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	rm -rf dist/ build/
	rm -f .coverage coverage.xml
	