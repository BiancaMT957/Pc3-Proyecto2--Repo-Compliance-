##  Issue 2.1 – Configurar flujo de CI/CD (Sprint 2)

###  Objetivo
Automatizar la ejecución del auditor mediante **GitHub Actions**.

Generar el reporte de cumplimiento `out/report.json`.

Validar que el pipeline falle cuando existan reglas de severidad **HIGH**.

Consolidar el flujo de integración continua para asegurar calidad y cumplimiento de estándares.

---

###  Metodología

#### 1️ Configuración del workflow en GitHub Actions

Se creó el archivo de pipeline en la ruta:

.github/workflows/auditor-ci.yml


Este workflow ejecuta automáticamente el auditor en cada **push** o **pull request** al repositorio.
La configuración incluye instalación del entorno virtual, dependencias y ejecución del módulo principal.
El flujo genera el archivo out/report.json, que contiene el resumen de reglas validadas, su severidad y el estado del análisis.


#### 2 Ejecución local del auditor

Antes de validar el pipeline, se ejecutó el auditor manualmente desde la terminal:

```
python -m auditor.core
```

Esto produjo un reporte en out/report.json:

```
{
  "summary": {
    "total": 4,
    "failed": 0,
    "passed": 4,
    "by_severity": {
      "HIGH": 0,
      "MEDIUM": 1,
      "LOW": 3
    }
  },
  "findings": [
    {
      "rule": "ENV_IN_GITIGNORE",
      "status": "PASS",
      "severity": "LOW",
      "details": {
        "path": ".gitignore"
      }
    },
    {
      "rule": "LICENSE_FILE",
      "status": "PASS",
      "severity": "LOW",
      "details": {
        "path": "LICENSE"
      }
    },
    {
      "rule": "MAKEFILE_TARGETS",
      "status": "PASS",
      "severity": "LOW",
      "details": {
        "path": "makefile"
      }
    },
    {
      "rule": "CONFIG_VIA_ENV",
      "status": "PASS",
      "severity": "MEDIUM"
    }
  ]
}
```


La interpretación de este reporte seria:Todas las reglas PASSED. No se registraron severidades HIGH (condición crítica). El pipeline retornó exit 0, confirmando ejecución exitosa. La regla CONFIG_VIA_ENV fue catalogada como MEDIUM solo por falta de .env.example (opcional).

### 3️  Validación de salida del pipeline

El archivo `out/report.json` se analizó para confirmar el comportamiento esperado:

|  **Condición**        |  **Resultado esperado** |
|--------------------------|---------------------------|
| Sin reglas **HIGH**      | `exit 0`  |
| Alguna regla **HIGH**    | `exit 1`  |

El pipeline se ejecutó correctamente, generando el artefacto de salida sin errores y validando la correcta configuración del flujo **CI/CD**.


#### 4 Lógica agregada en auditor/core.py

Se añadió una verificación al final del script para que el auditor devuelva un código de salida distinto según la severidad de los hallazgos.
De esta manera, el pipeline de GitHub Actions puede fallar automáticamente (exit 1) si existen findings HIGH en el reporte

######  Propósito:

Permitir que GitHub Actions interprete el resultado del auditor.

Integrar control automático de severidad en el flujo CI/CD.

Asegurar que ningún pull request se fusione con incumplimientos críticos.

* Ejecucion:

(venv) bianca007@MSI:/mnt/c/Users/Bianca/Documents/Pc3-Proyecto2--Repo-Compliance-$ python -m auditor.core
 Reporte generado en out/report.json
 Auditoría sin findings HIGH.

(venv) bianca007@MSI:/mnt/c/Users/Bianca/Documents/Pc3-Proyecto2--Repo-Compliance-$ echo $?
0


#### 5 Flujo de CI/CD – Auditor de Cumplimiento

Este workflow ejecuta verificaciones automáticas en cada Pull Request:

1. **Lint:** valida estilo y convenciones.
2. **Test:** ejecuta pruebas unitarias.
3. **Coverage:** asegura una cobertura ≥85%.
4. **Audit:** corre el auditor y bloquea merges si hay findings HIGH.

Los reportes se generan en `out/report.json` y se suben como artifact.  
Si alguno de los pasos falla, el merge queda bloqueado hasta resolver los hallazgos.

## Issue 2.2 - Generar y formatear reportes (Sprint 2)

### Objetivo
Crear report.json y report.md legibles con resumen por severidad.


Implementar auditor/report.py con funciones que generen JSON y Markdown legible. Agrupar findings por severidad e incluir resumen.

**Checklist**

- Implementar generate_json_report(findings, out_path) → out/report.json.

- Implementar generate_markdown_report(findings, out_path) → out/report.md con resumen (High/Medium/Low counts).

- Escribir tests en tests/test_report.py con tmp_path y @pytest.mark.parametrize.

### Metodologia
#### 1. Modificacion del auditor y creacion de `report.py`.
Se reestructura la logica del auditor, es decir separamos responsabilidades:
- `auditor/core.py`: responsable del motor de analisis y deteccion de findings.
- `auditor/report.py`: responsable de generar reportes (JSON y .md) y controlar el estado final del pipeline (exit code).

**Cambios realizados en `auditor/core.py`**

**Modificacion**: 
- Se elimino el bloque main que generaba un archivo `out/report.json`.
- El archivo ahora queda como una libreria dedicada a ejecutar las reglas de auditoria y retornar findings y metricas al ser llamada desde otro modulo.

**Motivo**:
- Evitar que `core.py` y `report.py` generen JSON duplicados.
- Mantener `core` como unidad logica reusable.
- Prepara el terreno para que `report.py` controle el flujo completo del pipeline y la salida final.

**Creacion de `auditor/report.py`**

**Descripcion**: Se diseña como punto unico de ejecucion del auditor:
1. Importa y ejecuta `core.run_audit(repo)`.
2. Genera los reportes: `out/report.json`, `out/report.md`.
3. Controla el estado de finalizacion del pipeline: si detecta findings con severidad HIGH, retorna `exit 1` y bloquea el flujo de CI/CD.
4. Implementa interfaz CLI con parametros:
  ```bash
  python -m auditor.report --fail-on-high --no-md --no-json
  ```
**Funciones clave:**
| Función | Descripción |
|----------|-------------|
| `write_json(findings, out_json)` | Escribe el reporte JSON formateado (con resumen por severidad y total de findings). |
| `write_markdown(findings, out_md)` | Genera un reporte legible en Markdown con íconos y agrupación por severidad. |
| `main()` | Punto de entrada CLI. Ejecuta el auditor, llama a los generadores y maneja el código de salida. |

**Conclusiones**
Estos cambios permiten un flujo mas limpio, robusto y mantenible, donde:
- `auditor/core.py` actua como motor de reglas (logica pura, sin I/O).
- `auditor/report.py` asume la responsabilidad de presentacion y control de calidad.
- El pipeline CI/CD se simplifica a un unico paso funcional, reduciendo redundancia y aumentando la trazabilidad.

#### 2. Modificacion del Makefile
Se modifica el makefile para implementar la ejecucion del auditor y generacion de reportes, con salida de error si hay HIGH.

```makefile
.PHONY: audit report
audit:
	python -m auditor.report --fail-on-high
report:
	python -m auditor.report  
```

Tambien modificamos el target `test`, que ahora incluye **gate de cobertura** con `--cov-fail-under=$(COV_MIN)` (default 85%), para no necesitar un target `coverage` aparte.

`report` y `audit` delegan en `auditor.report`:
- `report`: genera `out/report.json` y `out/report.md` sin fallar.
- `audit`: igual, pero falla si hay HIGH (ideal para CI o validar antes de un PR).

#### 3. Modificacion del flujo CI (Jobs: Auditor y Reportes)
Se simplifica el flujo de automatizacion para que el auditor y la generacion de reportes se ejecuten de forma integrada, haciendo que `auditor/report` sea responsable de:
- Ejecutar el analisis completo del repositorio.
- Generar los reportes (`report.json` y `report.md`).
- Bloquear el pipeline si existen findings de severidad HIGH.

**Cambios realizados**

**Modificacion:** `name: Run auditor & build reports` (antes: Run auditor)
- **Antes:** El paso ejecutaba `auditor.core` y luego un bloque adicional en python para volver a crear los reportes JSON y Markdown.
- **Ahora:** Se reemplazo por `python -m auditor.report --fail-on-high` que centraliza toda la logica de auditoria, generacion de reportes y control del exit code.
  **Motivo:** 
    - Evitar duplicacion de logica entre `core.py` y `report.py`.
    - Garantiza que el pipeline use siempre el mismo punto de generacion de resultados.
    - Mejorar la mantenibilidad y tranzabilidad.

**Modificacion:** `name: Upload audit reports` (antes: Upload report artifacts)
- **Antes:** Exitian dos pasos de subida de artifacts separados (`Upload report artifacts` y `Upload report artifact`), lo que duplicaba la evidencia de salida.
- **Ahora:** Se consolida en un paso unico.
```yaml
- name: Upload audit reports
  uses: actions/upload-artifact@v4
  with:
    name: audit-reports
    path: |
      out/report.json
      out/report.md
```
- **Motivo:** 
  - Elimina redundancia, reduce tiempos de ejecucion.
  - Agrupa los archivos generados (`.json` y `.md`) bajo un solo artifact coherente.

**Se elimina:** 
- `name: Upload artifacts`: Paso redundante, subia los mismo archivos que el nuevo bloque. 
- `name: Upload report artifact`: era un duplicado que subia solo `report.json`. 
- `name: Check HIGH findings`: verificaba si el `report.json` contenia findings `"severity":"HIGH"`. Este control ahora lo realiza `auditor.report` mediante la opcion `--fail-on-high`, con lo que garantiza `exit 1` cuando hay `HIGH`.

#### 4. Pruebas de generacion y formato de reportes (`test_report.py`).
Validaremos mediante pruebas unitarias parametrizadas que las siguientes funciones de `auditor/report.py` generen los archivos esperados y en el formato solicitado:
- `generate_json_report()`
- `generate_markdown_report()`

**Configuracion del test**
1. El archivo importa los modulos necesarios:
```python
from auditor.report import generate_json_report, generate_markdown_report
```
2. Validamos `test_generate_json_report` y que la salida JSON tenga estructura y los conteos correctos. Para eso definimos 2 escenearios con `@pytest.mark.parametrize`:
- **sin findings**: lista vacia.
- **con findings**: HIGH, MEDIUM y LOW

```python
@pytest.mark.parametrize(
    "findings,expected_counts",
    [
        ([], {"HIGH": 0, "MEDIUM": 0, "LOW": 0, "total": 0}),
        (
            [
                {"rule": "A", "status": "FAIL", "severity": "HIGH"},
                {"rule": "B", "status": "PASS", "severity": "LOW"},
                {"rule": "C", "status": "FAIL", "severity": "MEDIUM"},
                {"rule": "D", "status": "PASS", "severity": "LOW"},
            ],
            {"HIGH": 1, "MEDIUM": 1, "LOW": 2, "total": 4},
        ),
    ],
)
```
- `tmp_path` crea una carpeta temporal donde se guarda `report.json`.
- Se lee el archivo y se verifican:
  - Las claves principales: "summary" y "findings".
  - Que el conteo en "summary" coincida con lo esperado.
  - Que el total de findings sea igual al numero de reglas procesadas.

3. `test_generate_markdown_report` comprueba que el reporte en formato markdown se genere correctamente. Tendremos dos casos:
- **sin findings**: se espera una tabla con conteos en 0.
- **con findings**: debe aparecer cada regla con su estado, nombre y severidad.
```python
@pytest.mark.parametrize(
    "findings,expect_fragments",
    [
        ([], ["| HIGH | 0 |", "| MEDIUM | 0 |", "| LOW | 0 |", "Total findings: 0"]),
        (
            [
                {"rule": "ENV_IN_GITIGNORE", "status": "FAIL", "severity": "HIGH", "details": {"reason": "missing .env"}},
                {"rule": "LICENSE_FILE", "status": "PASS", "severity": "LOW"},
            ],
            ["| HIGH | 1 |", "| LOW | 1 |", "ENV_IN_GITIGNORE", "LICENSE_FILE", "❌", "✅"],
        ),
    ],
)
```
- Se genera `report.md` en la carpeta temporal.
- Se verifica que exista y contenga los fragmentos esperados, como la tabla de severidades y los iconos de estado.