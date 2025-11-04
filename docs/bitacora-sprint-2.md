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

