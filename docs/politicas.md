
#   Políticas y Reglas Implementadas — Sprint 1

## 1. Reglas Base del Auditor ( ` auditor/core.py ` )

| Regla | Descripción | Severidad | Estado | Ejemplo válido | Ejemplo inválido |
| ------- | -------------- | ------------ | --------- | ---------------- | ------------------ |
|  ** ENV_IN_GITIGNORE **  | Verifica que ` .env` esté listado en ` .gitignore` . | ALTA | PASA/FALLA |  ` .gitignore ` contiene ` .env `  |  ` .gitignore ` no lista ` .env ` o no existe |
|  ** LICENCIA_ARCHIVO **  | Comprueba existencia y contenido del archivo de licencia ( ` LICENSE ` o ` LICENSE.md ` ). | MEDIANO | PASA/FALLA |  ` LICENCIA ` con texto MIT | Falta ` LICENCIA ` o está vacío |
|  ** MAKEFILE_TARGETS **  | Revisa que ` Makefile` contiene los objetivos obligatorios ( ` lint` , ` test` , ` covery` ) . | MEDIANO | PASA/FALLA | Makefile con todos los objetivos definidos | Faltan uno o más objetivos |
|  ** CONFIG_VIA_ENV **  | Detecta uso indebido de credenciales en archivos ( ` .env ` , ` config.py ` , etc.). | ALTA | PASA/FALLA | Variables configuradas mediante entorno ( ` os.getenv` ) | Claves o contraseñas codificadas |

---

## 2. Estructura del Resultado de Auditoría

Cada regla devuelve un diccionario con las siguientes claves:

``` python
{
  " regla " : " ENV_IN_GITIGNORE " ,
  " estado " : " PASA " ,
  " gravedad " : " BAJA " ,
  " detalles " : { " ruta " : " .gitignore " }
}
```

### 3. Niveles de Severidad

|  ** Severidad **  |  ** Descripción **  |  ** Criterio **  |
| ---------------- | ----------------- | -------------- |
|  ** ALTO **  | Riesgo de exposición o incumplimiento crítico (por ejemplo, secretos o archivos sensibles). | Rompe tubería/bloquea fusión. |
|  ** MEDIANO **  | Incumplimiento de buenas prácticas o configuración incompleta. | Requiere corrección antes del lanzamiento. |
|  ** BAJO **  | Advertencia o recomendación de estilo o mantenimiento. | No bloqueador. |


### 4. Ejecución del Auditor

El motor se ejecuta desde la terminal con:

``` bash
python -m auditor.main
```

### 5. Ejemplos de repositorios

|  ** Repositorio **  |  ** Archivo **  |  ** Condición / Problema **  |
| ------------------ | ------------- | ---------------------------- |
|  ** Válido **  |  ` .gitignore `  | Contiene ` .env `  |
|  ** Válido **  |  ` LICENCIA `  | Contiene texto válido (por ejemplo, MIT) |
|  ** Válido **  |  ` Makefile `  | Incluye ` lint` , ` test` , ` cobertura` |​​​ 
|  ** Válido **  |  ` config.py `  | Usa ` os.getenv() ` para variables seguras |
|  ** Inválido **  |  ` .gitignore `  | No contiene ` .env `  |
|  ** Inválido **  |  ` LICENCIA `  | Vacío o ausente |
|  ** Inválido **  |  ` Makefile `  | Faltan * objetivos * requeridos |
|  ** Inválido **  |  ` config.py `  | Contiene ` "contraseña=123" ` o claves codificadas |

---

### 6. Deuda Técnica (Sprint 1)

|  ** Elemento Pendiente **  |  ** Descripción **  |
| -------------------------- | ----------------- |
| 🔹 Análisis de tamaño de artefactos | Falta implementar validación de archivos mayores a 100 MB. |
| 🔹 Integración de gitleaks | Pendiente de integración en la * pipeline * de CI para detección avanzada de secretos. |
| 🔹 Informe unificado | Falta generar un ` report.md` con resumen automático de * hallazgos * . |
| 🔹 xfail / skip documentados | Se documentaron pruebas * xfail * para escenarios no soportados en Windows (rutas y permisos). |

---

### 7. Métricas del Sprint

|  ** Métrica **  |  ** Resultado **  |
| -------------- | ---------------- |
| Cobertura de código | 98 % |
| Pruebas pasadas | 20 / 20 |
| Tiempo promedio de ejecución | 1,58 s |
| Gravedades detectadas | 0 ALTO / 1 MEDIO / 3 BAJO |
| Calidad de código ( * flake8 / black / isort * ) | Sin errores ni * advertencias *  |


# Políticas y Reglas Implementadas — Sprint 2

## 1. Reglas Base del Auditor (`auditor/core.py`)

| Regla | Descripción | Severidad | Estado | Ejemplo válido | Ejemplo inválido |
| ------- | -------------- | ------------ | --------- | ---------------- | ------------------ |
| **ENV_IN_GITIGNORE** | Verifica que `.env` esté listado en `.gitignore`. | ALTA | PASA/FALLA | `.gitignore` contiene `.env` | `.gitignore` no lista `.env` o no existe |
| **LICENSE_FILE** | Verifica que exista un archivo `LICENSE` no vacío. | MEDIA | PASA/FALLA | Archivo `LICENSE` con contenido válido | `LICENSE` vacío o ausente |
| **MAKEFILE_TARGETS** | Comprueba que el Makefile tenga los targets básicos (`test`, `audit`, `report`). | MEDIA | PASA/FALLA | Makefile con todos los targets | Faltan targets esenciales |
| **CONFIG_VIA_ENV** | Valida que no existan claves sensibles versionadas y que las configuraciones se manejen por variables de entorno. | MEDIA | PASA/FALLA | Uso de `os.getenv()` | Variables sensibles (`SECRET_KEY`, `.env`) versionadas |

---

## 2. Nuevas Políticas y Workflow — Sprint 2

### 2.1. Flujo CI/CD Automatizado

**Objetivo:** Garantizar la calidad y cumplimiento de estándares mediante la automatización del auditor en GitHub Actions.

**Archivo principal:** `.github/workflows/compliance.yml`

#### Configuración del pipeline
- Se ejecuta automáticamente en cada `push` o `pull request`.
- Instala dependencias y ejecuta el auditor (`python -m auditor.report --fail-on-high`).
- Genera artefactos: `out/report.json` y `out/report.md`.
- Bloquea el pipeline (`exit 1`) si existen findings con severidad **HIGH**.

#### Lógica interna del auditor
- Se añadió verificación en `auditor/core.py` y `auditor/report.py` para controlar el código de salida.
- `report.py` centraliza la generación de reportes y el control de fallos críticos.
- GitHub Actions interpreta el `exit code` para bloquear merges automáticos cuando existan findings críticos.

---

### 2.2. Generación de Reportes (`auditor/report.py`)

**Objetivo:** Crear reportes automáticos en formato JSON y Markdown con resumen por severidad.

#### Cambios principales
- `auditor/core.py`: se convierte en motor puro de análisis (sin I/O).
- `auditor/report.py`: genera reportes y maneja el estado final del pipeline.
- CLI integrada con opciones:
  ```bash
  python -m auditor.report --fail-on-high --no-md --no-json
  ```

#### Funciones principales
| Función | Descripción |
|----------|-------------|
| `write_json(findings, out_json)` | Escribe reporte JSON con resumen por severidad y total. |
| `write_markdown(findings, out_md)` | Genera reporte legible con íconos y agrupación por severidad. |
| `main()` | Punto de entrada CLI. Controla la ejecución completa del auditor. |

---

### 2.3. Cambios en el Makefile

**Nuevos targets:**
```makefile
.PHONY: audit report
audit:
	python -m auditor.report --fail-on-high
report:
	python -m auditor.report
```

- `report`: genera reportes sin bloquear pipeline.  
- `audit`: falla si hay findings HIGH (ideal para CI).  
- El target `test` ahora incluye gate de cobertura con `--cov-fail-under=85`.

---

### 2.4. Ajustes en el Workflow (CI/CD)

- Se reemplazó la ejecución de `auditor.core` por `auditor.report`.
- Se consolidaron los pasos de subida de artefactos (`report.json`, `report.md`) bajo un único bloque:
  ```yaml
  - name: Upload audit reports
    uses: actions/upload-artifact@v4
    with:
      name: audit-reports
      path: |
        out/report.json
        out/report.md
  ```
- Se eliminaron pasos redundantes como `Check HIGH findings`, ya que `--fail-on-high` controla este comportamiento.

---

### 2.5. Pruebas Unitarias (`test_report.py`)

**Validaciones incluidas:**
- Estructura y conteos correctos en JSON.
- Generación adecuada del Markdown con íconos y severidades.
- Escenarios parametrizados con `pytest.mark.parametrize` para casos con y sin findings.
- Verificación de artefactos temporales generados (`report.json`, `report.md`).

---

### 2.6. Simulación Completa del Pipeline (`Issue 2.3`)

**Repositorio de prueba:** `tests/demo_repo_invalid/`  
Contiene ejemplos con incumplimientos para validar el comportamiento del auditor.

#### Casos simulados
| Archivo | Regla fallida | Severidad |
|----------|----------------|------------|
| `.gitignore` | ENV_IN_GITIGNORE | HIGH |
| `.env` | CONFIG_VIA_ENV | HIGH |
| `LICENSE` | LICENSE_FILE | MEDIUM |
| `Makefile` | MAKEFILE_TARGETS | LOW |
| `settings.py` | CONFIG_VIA_ENV | HIGH |

**Objetivo:** Confirmar que el pipeline se bloquea correctamente (`exit 1`) cuando existen findings HIGH y que los reportes se generan exitosamente.

---

### 2.7. Conclusión

El auditor evolucionó a una arquitectura modular y automatizada:
- **core.py:** motor de reglas.  
- **report.py:** generación de reportes y control de flujo CI/CD.  
- **Makefile + GitHub Actions:** integran la automatización completa.

El flujo actual asegura que **ningún PR pueda fusionarse con hallazgos críticos**, manteniendo estándares de calidad y cumplimiento.


