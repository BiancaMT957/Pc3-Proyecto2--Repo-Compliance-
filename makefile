.PHONY: lint test coverage run clean setup install_deps setup_hooks audit report

PKG ?= auditor
OUT ?= out
COV_MIN ?= 85

install_deps:
	pip install -r requirements.txt
	sudo apt update -y && sudo apt install -y nodejs npm
	npm install --save-dev @commitlint/config-conventional @commitlint/cli

setup_hooks:
	pre-commit clean
	pre-commit install --hook-type pre-commit --hook-type commit-msg
	pre-commit autoupdate
	pre-commit run --all-files || true

setup: install_deps setup_hooks
	@echo "Proyecto inicializado con hooks activos"

lint:
	@echo " Ejecutando linters..."
	black $(PKG) tests
	isort $(PKG) tests
	flake8 $(PKG) tests

test:
	@echo " Ejecutando pruebas..."
	mkdir -p $(OUT)
	pytest --cov=$(PKG) --cov-report=xml:$(OUT)/coverage.xml --cov-report=term-missing --cov-fail-under=$(COV_MIN) -v

report:
	@echo "Generando reportes JSON/MD..."
	python -m $(PKG).report

audit:
	@echo "Ejecutando auditor con gate de severidad (fail on HIGH)"
	python -m $(PKG).report --fail-on-high

run:
	@echo " Ejecutando auditor (no falla si hay HIGH)..."
	python -m $(PKG).report



clean:
	@echo " Limpiando archivos temporales..."
	rm -rf __pycache__ */__pycache__ $(OUT)/ .pytest_cache .coverage coverage.xml
