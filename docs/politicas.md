@@ -0,0 +1,81 @@
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


