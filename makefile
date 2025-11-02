.PHONY: lint test coverage run clean setup install_deps setup_hooks

install_deps:
	pip install -r requirements.txt
	sudo apt update -y && sudo apt install -y nodejs npm
	npm install --save-dev @commitlint/{config-conventional,cli}

setup_hooks:
	pre-commit clean
	pre-commit install --hook-type pre-commit --hook-type commit-msg
	pre-commit autoupdate
	pre-commit run --all-files || true

setup: install_deps setup_hooks
	@echo "Proyecto inicializado con hooks activos"

lint:
	@echo " Ejecutando linters..."
	black auditor tests
	isort auditor tests
	flake8 auditor tests

test:
	@echo " Ejecutando pruebas..."
	mkdir -p out
	pytest --cov=auditor --cov-report=xml:out/coverage.xml --cov-report=term-missing -v

coverage:
	@echo " Mostrando reporte de cobertura..."
	mkdir -p out
	pytest --cov=auditor --cov-report=term-missing -v

run:
	@echo " Ejecutando auditor..."
	python -m auditor

clean:
	@echo " Limpiando archivos temporales..."
	rm -rf __pycache__ */__pycache__ out/ .pytest_cache .coverage coverage.xml
