#  Políticas y Reglas Implementadas — Sprint 1

## 1. Reglas Base del Auditor (`auditor/core.py`)

| Regla | Descripción | Severidad | Estado | Ejemplo válido | Ejemplo inválido |
|-------|--------------|------------|---------|----------------|------------------|
| **ENV_IN_GITIGNORE** | Verifica que `.env` esté listado en `.gitignore`. | HIGH | PASS/FAIL | `.gitignore` contiene `.env` | `.gitignore` no lista `.env` o no existe |
| **LICENSE_FILE** | Comprueba existencia y contenido del archivo de licencia (`LICENSE` o `LICENSE.md`). | MEDIUM | PASS/FAIL | `LICENSE` con texto MIT | Falta `LICENSE` o está vacío |
| **MAKEFILE_TARGETS** | Revisa que `Makefile` contenga los targets obligatorios (`lint`, `test`, `coverage`). | MEDIUM | PASS/FAIL | Makefile con todos los targets definidos | Faltan uno o más targets |
| **CONFIG_VIA_ENV** | Detecta uso indebido de credenciales en archivos (`.env`, `config.py`, etc.). | HIGH | PASS/FAIL | Variables configuradas mediante entorno (`os.getenv`) | Claves o contraseñas hardcodeadas |

---

## 2. Estructura del Resultado de Auditoría

Cada regla devuelve un diccionario con las siguientes claves:

```python
{
  "rule": "ENV_IN_GITIGNORE",
  "status": "PASS",
  "severity": "LOW",
  "details": {"path": ".gitignore"}
}
```

### 3. Niveles de Severidad

| **Severidad** | **Descripción** | **Criterio** |
|----------------|-----------------|--------------|
| **HIGH** | Riesgo de exposición o incumplimiento crítico (por ejemplo, secretos o archivos sensibles). | Rompe pipeline / bloquea merge. |
| **MEDIUM** | Incumplimiento de buenas prácticas o configuración incompleta. | Requiere corrección antes del release. |
| **LOW** | Advertencia o recomendación de estilo o mantenimiento. | No bloqueante. |


### 4. Ejecución del Auditor

El motor se ejecuta desde la terminal con:

```bash
python -m auditor.main
```

### 5. Ejemplos de Repositorios

| **Repositorio** | **Archivo** | **Condición / Problema** |
|------------------|-------------|----------------------------|
| **Válido** | `.gitignore` | Contiene `.env` |
| **Válido** | `LICENSE` | Contiene texto válido (por ejemplo, MIT) |
| **Válido** | `Makefile` | Incluye `lint`, `test`, `coverage` |
| **Válido** | `config.py` | Usa `os.getenv()` para variables seguras |
| **Inválido** | `.gitignore` | No contiene `.env` |
| **Inválido** | `LICENSE` | Vacío o ausente |
| **Inválido** | `Makefile` | Faltan *targets* requeridos |
| **Inválido** | `config.py` | Contiene `"password=123"` o claves codificadas |

---

### 6. Deuda Técnica (Sprint 1)

| **Elemento Pendiente** | **Descripción** |
|--------------------------|-----------------|
| 🔹 Análisis de tamaño de artefactos | Falta implementar validación de archivos mayores a 100 MB. |
| 🔹 Integración de gitleaks | Pendiente de integración en la *pipeline* de CI para detección avanzada de secretos. |
| 🔹 Reporte unificado | Falta generar un `report.md` con resumen automático de *findings*. |
| 🔹 xfail / skip documentados | Se documentaron pruebas *xfail* para escenarios no soportados en Windows (rutas y permisos). |

---

### 7. Métricas del Sprint

| **Métrica** | **Resultado** |
|--------------|----------------|
| Cobertura de código | 98 % |
| Pruebas pasadas | 20 / 20 |
| Tiempo promedio de ejecución | 1.58 s |
| Severidades detectadas | 0 HIGH / 1 MEDIUM / 3 LOW |
| Calidad de código (*flake8 / black / isort*) | Sin errores ni *warnings* |



