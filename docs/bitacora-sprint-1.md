#  Issue 1.1 – Configuración inicial del proyecto (Sprint 1)

##  Objetivo

- Crear la estructura base del repositorio y configurar el entorno de pruebas.  
- Establecer herramientas de calidad (linters, hooks) y medición de cobertura.  
- Documentar el flujo de trabajo inicial.

---

##  Metodología

### 1️) Estructura base del proyecto

Se creó la arquitectura mínima sugerida para el repositorio, asegurando una separación clara entre el código fuente, las pruebas y la documentación:

auditor/ # Código fuente principal
tests/ # Pruebas unitarias con pytest
docs/ # Documentación del proyecto
.github/workflows/ # Pipelines de CI/CD
out/ # Reportes y archivos generados por pytest



**Archivos iniciales añadidos:**
- `README.md`
- `.gitignore`
- `requirements.txt`
- `pytest.ini`
- `.pre-commit-config.yaml`
- `Makefile`

---

### 2️) Configuración de pytest y cobertura

Se instaló y configuró **pytest** junto con **pytest-cov** para medir la cobertura de código.  
El archivo `pytest.ini` se definió con los parámetros necesarios para generar el reporte XML:

```ini
[pytest]
minversion = 7.0
addopts = --cov=auditor --cov-report=xml:out/coverage.xml --cov-report=term-missing -v
testpaths = tests
python_files = test_*.py

La ejecucion se dio con:

```
make test


produce el archivo out/coverage.xml con el detalle de cobertura.



**Resultados de primer test del sprint1** :

El primer test paso de la manera correcta con cobertura mayor a 90 porciento, en este caso con 100 porciento.


```
(venv) bianca007@MSI:/mnt/c/Users/Bianca/Documents/Pc3-Proyecto2--Repo-Compliance-$ make test
 Ejecutando pruebas...
mkdir -p out
pytest --cov=auditor --cov-report=xml:out/coverage.xml --cov-report=term-missing -v
============================================================== test session starts ===============================================================
platform linux -- Python 3.12.3, pytest-8.4.2, pluggy-1.6.0 -- /mnt/c/Users/Bianca/Documents/Pc3-Proyecto2--Repo-Compliance-/venv/bin/python3
cachedir: .pytest_cache
rootdir: /mnt/c/Users/Bianca/Documents/Pc3-Proyecto2--Repo-Compliance-
configfile: pytest.ini
testpaths: tests
plugins: cov-7.0.0
collected 1 item                                                                                                                                 



tests/test_sample.py::test_saludo_basico PASSED                                                                                            [100%] 

================================================================= tests coverage =================================================================
________________________________________________ coverage: platform linux, python 3.12.3-final-0 _________________________________________________

Name                  Stmts   Miss  Cover   Missing
---------------------------------------------------
auditor/__init__.py       0      0   100%

tests/test_sample.py::test_saludo_basico PASSED                                                                                            [100%] 

================================================================= tests coverage =================================================================
________________________________________________ coverage: platform linux, python 3.12.3-final-0 _________________________________________________

Name                  Stmts   Miss  Cover   Missing
---------------------------------------------------
auditor/__init__.py       0      0   100%
auditor/main.py           2      0   100%
---------------------------------------------------
TOTAL                     2      0   100%
Coverage XML written to file out/coverage.xml
=============================================================== 1 passed in 0.99s ================================================================
```



### 3) Configuración del Makefile

Se implementaron los targets estándar solicitados:

Target	 |   Descripción
lint	     Ejecuta linters (black, isort, flake8)
test	     Ejecuta pytest con cobertura
coverage	 Muestra resumen de cobertura en terminal
run	         Ejecuta la aplicación principal
clean	     Limpia archivos generados

Esto permite mantener un flujo reproducible y automatizado de pruebas y validación.

### 4) Hooks de pre-commit

Se instaló pre-commit con los siguientes hooks en fase no bloqueante:

* Formato de código: black, isort

* Linter: flake8

* Validación de mensajes de commit: Conventional Commits

* Detección básica de secretos: detect-secrets

* La configuración se documentó en docs/hooks.md , indicando cómo instalar y activar los hooks localmente.

