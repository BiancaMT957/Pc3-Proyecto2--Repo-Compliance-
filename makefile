.PHONY: lint test coverage run clean

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
