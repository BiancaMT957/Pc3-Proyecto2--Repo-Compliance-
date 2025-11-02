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

# Issue 1.2: Implementar reglas base de auditoría.
## Objetivo
Desarrollar e integrar las reglas mínimas del motor de auditoría que permitan analizar repositorios y detectar incumplimientos básicos de seguridad, licenciamiento y buenas prácticas DevSecOps.

## Metodologia

### 1. Diseño de funciones en `auditor/core.py`.
Se crean funciones independientes para cada regla:
- `check_env_in_gitignore()`: verifica exitencia de gitignore y .env
- `check_license_file()`: verifica la existencia de licencia
- `check_makefile_targets()`: verifica exitencia de makefile con targets basicos
- `check_config_credentials()`: verifica secretos detectados

### 2. Estandarizado de resultados de cada regla.
- Se asegura que todos devuelvan un diccionario con claves:
```bash
{"rule": ..., "status": ..., "severity": ..., "details": ...}
```
- Se usa niveles de severidad (LOW, MEDIUM, HIGH) y estados (PASS, FAIL).

### 3. Implementacion de la funcion `run_audit()`.
- Ejecuta todas las reglas de la secuencia.
- Agrega sus resultados a una lista findings global.
- Prepara el entorno compatible con futuras exportaciones (CSV o JSON).

### 4. Valida deteccion de fallos comunes.
- `.env` no se encuentra en `.gitignore`: `FAIL + HIGH`
- Licencia vacia o ausente: `FAIL`
- Makefile sin targets `lint`, `test`, `coverage`: `FAIL` con lista de faltantes
- Variables sensibles o credenciales en archivos de configuracion (`config.yaml`, `.env`, etc): `FAIL + HIGH`

### 5. Probar las reglas individualmente y en conjunto.
- Genera repositorios de prueba (válidos y erróneos) en tests/data/repos/.
- Ejecuta pytest para validar que cada regla se comporte según lo esperado.
- Verifica que `run_audit()` combine correctamente los findings.

### 6. Cumplir con el umbral de calidad definido.
- Cobertura de pruebas ≥ 85 %.
- Estructura reproducible (`src/`, `tests/`, `out/`).
- Resultados reproducibles con `make test_all`.

## Evidencias
Colocamos una de las reglas diseñadas en `auditor/core.py`:
```bash
def check_env_in_gitignore(repo: Path) -> Dict:
    """Verifica que '.env' aparezca en el .gitignore."""
    gi = repo / ".gitignore"
    if not gi.exists():
        return _rule_result(
            "ENV_IN_GITIGNORE",
            "FAIL",
            "HIGH",
            {"reason": ".gitignore no existe"}
        )
    content = _read_text(gi)
    if ".env" not in content:
        return _rule_result(
            "ENV_IN_GITIGNORE",
            "FAIL",
            "HIGH",
            {"path": str(gi), "reason": "Falta la entrada .env en .gitignore"}
        )
    return _rule_result("ENV_IN_GITIGNORE", "PASS", "LOW", {"path": str(gi)})
```
El metodo nos permite hallar `.gitignore` dentro del repo, tambien nos premite verificar la existencia de `.env` dentro de `.gitignore`. 

Tambien tenemos la funcion `run_adit()` que ejecuta todas las reglas:
```bash
def run_audit(repo: Path) -> Dict:
    """Ejecuta todas las reglas y devuelve findings + resumen."""
    rules = [
        check_env_in_gitignore,
        check_license_file,
        check_makefile_targets,
        check_config_via_env,
    ]
    findings: List[Dict] = []

    for rule in rules:
        try:
            findings.append(rule(repo))
        except Exception as exc:  # protección de motor
            findings.append(_rule_result(
                rule.__name__,
                "FAIL",
                "HIGH",
                {"reason": f"{type(exc).__name__}: {exc}"}
            ))
```

# Issue 1.3: Pruebas unitarias con parametrización

##  Objetivos
Asegurar la **calidad del motor de auditoría (`auditor/core.py`)** mediante la creación de un conjunto de **tests unitarios parametrizados** que cubran escenarios buenos, malos y límite.  
El propósito del issue es alcanzar una **cobertura mínima del 85 %** (superada con 90 % final), garantizando que todas las reglas base (`check_*`) y el motor `run_audit()` funcionen de forma confiable.

## Metodología

### 1. Estructura y organización de pruebas
- Se centralizaron las pruebas en la carpeta `tests/` siguiendo la convención de `pytest`, con los siguientes archivos:
```bash
tests/
├─ conftest.py
├─ test_core_param.py
├─ test_core_mocks.py
└─ test_run_audit_integration.py
```
Se implementó la **fixture `repo_factory`** (en `conftest.py`) para generar repositorios temporales usando `tmp_path`.  
Esta función permite crear combinaciones controladas de:
- `.gitignore` con o sin `.env`.
- `LICENSE` vacío, inexistente o válido.
- `Makefile` con targets completos o faltantes.
- Archivos `.env`, `.env.example`, `settings.py`, `config.py` con posibles secretos.
- Esta fixture permitió **reutilizar repositorios simulados** en todos los tests, cumpliendo con el requisito de *fixtures reutilizables y consistentes*.

### 2. Pruebas parametrizadas
- Se desarrollaron **tests con `@pytest.mark.parametrize`** (en `test_core_param.py`) para cubrir todas las variantes de entrada:
- `.env` ausente o no listado en `.gitignore`: debe fallar con severidad HIGH.  
- `LICENSE` inexistente o vacío: FAIL.  
- `Makefile` incompleto (faltan targets `lint`, `test`, `coverage`): FAIL/MEDIUM.  
- Detección de secretos en `.env`, `settings.py` o `config.py` → FAIL/HIGH.  
- Repositorios correctos con `.env.example`: PASS/LOW.
- Esta parametrización permitió **maximizar la cobertura** y **evitar duplicación de código**.

### 3. Mocks, patch y validación de llamadas
En `test_core_mocks.py`, se empleó **monkeypatch** y wrappers espías para:
- Simular una excepción en una regla (`RuntimeError("boom")`) y verificar que `run_audit()` la capture sin interrumpir la ejecución.
- Interceptar `_exists_insensitive()` y validar sus argumentos (`call_args` equivalentes a los nombres esperados de archivos LICENSE).
- Con esto se cubrieron las ramas internas del motor y se demostró que la auditoría es **resiliente ante errores internos**.

### 4. Pruebas de integración
En `test_run_audit_integration.py` se validó el comportamiento **de punta a punta** del auditor:
- Repositorio correcto: `failed == 0`, JSON serializable.
- Repositorio con múltiples fallas: `failed >= 3`, hallazgos agregados correctamente.
- Este test asegura la **integridad del flujo** de generación de findings y del `summary`.


## Evidencias
### Test de integración con múltiples fallas

El siguiente test demuestra la ejecución completa del motor `run_audit()` ante un repositorio con múltiples incumplimientos:

```python
def test_run_audit_fail_detecta_faltantes(repo_factory):
    repo = repo_factory(
        gitignore=True, env_in_gitignore=False,  
        license_text="",                      
        make_targets=("lint",),              
        dot_env=True,                   
    )
    rep = core.run_audit(repo)
    assert rep["summary"]["failed"] >= 3
    assert any(f["rule"] == "MAKEFILE_TARGETS" and f["status"] == "FAIL" for f in rep["findings"])
```

### Cobertura
- Ejecución con `make test`:
```bash
(venv) luis@LAPTOP-LC:/mnt/c/Users/Luis/Documents/Pc3-Proyecto2--Repo-Compliance-$ make test
 Ejecutando pruebas...
mkdir -p out
pytest --cov=auditor --cov-report=xml:out/coverage.xml --cov-report=term-missing -v
=============================================================== test session starts ===============================================================
platform linux -- Python 3.12.3, pytest-8.4.2, pluggy-1.6.0 -- /mnt/c/Users/Luis/Documents/Pc3-Proyecto2--Repo-Compliance-/venv/bin/python3
cachedir: .pytest_cache
rootdir: /mnt/c/Users/Luis/Documents/Pc3-Proyecto2--Repo-Compliance-
configfile: pytest.ini
testpaths: tests
plugins: cov-7.0.0
collected 20 items                                                                                                                                

tests/test_core_mocks.py::test_run_audit_maneja_excepcion PASSED                                                                            [  5%]
tests/test_core_mocks.py::test_exists_insensitive_llamado PASSED                                                                            [ 10%] 
tests/test_core_param.py::test_check_env_in_gitignore[False-False-FAIL-HIGH] PASSED                                                         [ 15%] 
tests/test_core_param.py::test_check_env_in_gitignore[True-False-FAIL-HIGH] PASSED                                                          [ 20%]
tests/test_core_param.py::test_check_env_in_gitignore[True-True-PASS-LOW] PASSED                                                            [ 25%]
tests/test_core_param.py::test_check_license_file[None-FAIL] PASSED                                                                         [ 30%] 
tests/test_core_param.py::test_check_license_file[-FAIL] PASSED                                                                             [ 35%]
tests/test_core_param.py::test_check_license_file[MIT-PASS] PASSED                                                                          [ 40%]
tests/test_core_param.py::test_check_makefile_targets[None-FAIL-missing_subset0] PASSED                                                     [ 45%] 
tests/test_core_param.py::test_check_makefile_targets[targets1-FAIL-missing_subset1] PASSED                                                 [ 50%] 
tests/test_core_param.py::test_check_makefile_targets[targets2-FAIL-missing_subset2] PASSED                                                 [ 55%] 
tests/test_core_param.py::test_check_makefile_targets[targets3-PASS-missing_subset3] PASSED                                                 [ 60%]
tests/test_core_param.py::test_check_config_via_env[True-False-False-FAIL-HIGH] PASSED                                                      [ 65%] 
tests/test_run_audit_integration.py::test_run_audit_fail_detecta_faltantes PASSED                                                           [ 95%] 
tests/test_sample.py::test_saludo_basico PASSED                                                                                             [100%] 

================================================================= tests coverage ==================================================================
_________________________________________________ coverage: platform linux, python 3.12.3-final-0 _________________________________________________

Name                  Stmts   Miss  Cover   Missing
---------------------------------------------------
auditor/__init__.py       0      0   100%
auditor/core.py          84      2    98%   184-185
auditor/main.py           2      0   100%
---------------------------------------------------
TOTAL                    86      2    98%
Coverage XML written to file out/coverage.xml
=============================================================== 20 passed in 1.58s ================================================================
(venv) luis@LAPTOP-LC:/mnt/c/Users/Luis/Documents/Pc3-Proyecto2--Repo-Compliance-$
```

## Observaciones
### Modificacion del `.pre-commit-config.yaml` 
1. Se añade la siguiente linea al inicio:
```yaml
default_install_hook_types: [pre-commit, commit-msg]
```
Esta linea le dice a `pre-commit` que instale ambos hooks (pre-commit y commit-msg), cuando se ejecuta `pre-commit install`.

2. Se modifica el siguientes bloque:
```yaml
- repo: https://github.com/conventional-changelog/commitlint
  rev: v17.8.0
  hooks:
    - id: commitlint
```
La validacion de commits no funcionaba correctamente, ya que no es compatible con pre-commit. Luego definimos el siguiente bloque:
```yaml
  - repo: https://github.com/alessandrojcm/commitlint-pre-commit-hook
    rev: v9.16.0
    hooks:
      - id: commitlint
        stages: [commit-msg]
        args: ["--config=.commitlintrc.json"]
``` 
Este bloque usa un repositorio wrapper oficial que adapta `commitlint` al ecosistema de pre-commit.
#### Configuracion del hook:

| Clave | Descripcion |
|--------------|--------|
| `id: ` | Define el **hook** se ejecuta desde ese repo, en nuestro caso `commitlint`. |
| `stages: ` | Define en que estapa del ciclo de Git se ejecuta: `commit-msg` (justo despues de escribir el mensaje). |
| `args: ` | Son los argumentos pasados al comando `commitlint`. Indica donde esta el archivo de configuracion: `.commitlintrc.json` |

> **Nota:** Con esto logramos configurar el diseño de los commit, ya que solo se aceptaran los convencionales.

Se adjunta ejemplo de uso:
```bash
(venv) luis@LAPTOP-LC:/mnt/c/Users/Luis/Documents/Pc3-Proyecto2--Repo-Compliance-$ git commit -m "añadi cambios"
[ERROR] Your pre-commit configuration is unstaged.
`git add .pre-commit-config.yaml` to fix this.
```

### Modificacion del `Makefile`.
Como proceso para la automatizacion del proyecto, añadimos los siguientes targets para preparar el entorno con las dependencias y hooks necesarios.

1. Añadimos el target `install_deps`, que nos permite instalar dependencias del sistema y del proyecto, instala `Python` y `Node.js`. 
```Makefile
install_deps:
	pip install -r requirements.txt
	sudo apt update -y && sudo apt install -y nodejs npm
	npm install --save-dev @commitlint/{config-conventional,cli}

```
**Por qué existe:**
- Asegura que el entorno tenga lo necesario: pytest, flake8, black, pre-commit, commitlint, etc.
- Evita que los desarrolladores olviden instalar algo manualmente.
- Permite repetir el proceso sin miedo (idempotente).
2. Añadimos el target `setup_hooks`, que configura los hooks de Git, usa las herramientas que se instalaron antes para crear los hooks dentro del repositorio.

```Makefile
setup_hooks:
	pre-commit clean
	pre-commit install --hook-type pre-commit --hook-type commit-msg
	pre-commit autoupdate
	pre-commit run --all-files || true
```
**Por qué existe:**
- Limpia posibles hooks viejos.
- Crea los archivos reales en `.git/hooks/`:
    - `pre-commit`: ejecuta black, isort, flake8, detect-secrets.
    - `commit-msg`: ejecuta commitlint.
- Actualiza versiones de hooks (`autoupdate`).
- Ejecuta una pasada de prueba (`run --all-files`).

3. Finalmente agrupamos ambas dentro del target `setup`, ya que representan todo el flujo de inicializacion del proyecto.

### ¿Por qué usamos Hooks?
Un Hook de Git (o "gancho") es simplemente un script que Git ejecuta automáticamente en ciertos eventos clave durante su operación normal.

Funcionan como mecanismos de automatización y validación que te permiten personalizar el comportamiento interno de Git. Puedes usarlos para asegurar que el código cumpla con ciertos estándares o para automatizar tareas repetitivas.

## Ejecucion con conventional commit
La configuracion (`.pre-commit-config.yaml`) contiene múltiples etapas:
- Primero corre el hook `pre-commit`, ejecutando black, isort, flake8, detect-secrets, etc.
- Luego corre el hook `commit-msg`, ejecutando nuevamente el pipeline (por diseño, pre-commit lanza los hooks activos en ambas etapas), más `commitlint`.

Daremos el ejemplo al hacer commit sobre el archivo `.pre-commit-config.yaml` que se modifico, dando el siguiente resultado:
```bash
(venv) luis@LAPTOP-LC:/mnt/c/Users/Luis/Documents/Pc3-Proyecto2--Repo-Compliance-$ git commit -m "fix: configura el uso de conventional commits"
[WARNING] Unstaged files detected.
[INFO] Stashing unstaged files to /home/luis/.cache/pre-commit/patch1762110720-8631.
black................................................(no files to check)Skipped
isort................................................(no files to check)Skipped
flake8...............................................(no files to check)Skipped
Detect hardcoded secrets.................................................Passed
Detect secrets...........................................................Passed
[INFO] Restored changes from /home/luis/.cache/pre-commit/patch1762110720-8631.
[WARNING] Unstaged files detected.
[INFO] Stashing unstaged files to /home/luis/.cache/pre-commit/patch1762110724-8669.
black................................................(no files to check)Skipped
flake8...............................................(no files to check)Skipped
Detect hardcoded secrets.................................................Passed
commitlint...............................................................Passed
Detect secrets...........................................................Passed
[INFO] Restored changes from /home/luis/.cache/pre-commit/patch1762110724-8669.
[feature/configuracion-inicial/Luis 091de24] fix: configura el uso de conventional commits
 2 files changed, 39 insertions(+), 1 deletion(-)
```
Finalmente observamos la correcta ejecucion del `commitlint` ya que ahora nos pide un conventional commit para poder hacer los commits.