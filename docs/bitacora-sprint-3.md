# Issue 3.1 - Publicacion en Github Projects
## Objetivo
Integrar la auditoria con la API de Github Projects.

## Funcionalidades añadidas
### `auditor/github_api.py`
Creamos la clase `GitHubAPI` con la siguiente descripcion:
>Capa de abstracción mínima sobre la API de GitHub.En este sprint sólo simulamos el comportamiento:
devolvemos diccionarios que representan la acción realizada, sin hacer llamadas HTTP reales.

**Metodos implementados**
- `from_env()`: Crea una instancia leyendo el token desde variables de entorno. Esto nos permite simular tokens en pruebas con monkeypatch.
- `move_card()`: Simula mover una tarjeta (card) a otra columna en GitHub Projects. En una integración real aquí iría un POST/PUT a la API, pero en este sprint sólo devolvemos un payload trazable.
- `comment_issue()`: Simula agregar un comentario en un Issue/PR.
    - repo: 'owner/repo'
    - issue_number: número de issue o PR
    - body: contenido del comentario en Markdown.
- `build_audit_summary_body()`: Construye el cuerpo del comentario que resume los findings del auditor. No realiza I/O, sólo arma el texto; ideal para testear fácilmente.
- `comment_audit_summary()`: Comenta en un PR el resumen del auditor, incluyendo trend y blocked_time. Internamente reutiliza comment_issue() para facilitar los mocks en tests.

### `tests/test_github-api.py`
Uso de `pytest`, `monkeypatch` y `unittest.mock.patch` con `autospec` para:
- Simular tokens locales (GITHUB_TOKEN).
- Verificar que `move_card()` y `comment_issue()` se llamen con los argumentos correctos.
- Validar que el resumen generado incluya conteos por severidad, trend y blocked_time.

**Bloqueos:**
>No se realizó integración real con la API de GitHub (se dejó como simulación controlada para fines académicos y de pruebas unitarias).

# Issue 3.2 - Metricas y tendencias
## Objetivo
Calcular estadisticas de cumplimiento por sprint y guardar metricas historicas.

## Funcionalidades añadidas
### `auditor/metrics.py`
Implementa funciones para calcular metricas:

**Metodos implementados**
- `compute_compliance_percent()`: Devuelve un porcentaje de cumplimiento del repositorio, entre 0 y 100.
- `compute_trend()`: Indica si el repositorio mejoro, empeoro o se mantuvo igual. Comparando HIGH.
    - "mejora": menos HIGH que antes.
    - "empeora": mas HIGH que antes.
    - "estable": se quedo igual.
- `export_metrics_json()`: crea o sobreescribe un archivo json con metricas y devuelve el path del archivo.
```json
// Ejemplo de metrica
metrics = {
  "severity_counts": {"HIGH": 1, "MEDIUM": 2, "LOW": 1, "total": 4},
  "compliance_percent": 75.0,
  "trend": "mejora"
}
```

### Integracion de `metrics.py` en `report.py`
Mientras report cumple funcion de generar archivos de registro; metrics mide tendencias del momento, comparandolas con el historico. De esta forma sabremos si mejoramos. Por esta razon integramos ambas ya que cumplen funciones complementarias.

Añadimos comandos dentro del `main` de `report.py` y ejecutamos el siguiente comando para visualizar los resultados.

```bash
python -m auditor.report
```
generando el archivo `evidence/sprint-3/metrics.json` con el siguiente contenido:
```json
{
  "generated_at": "2025-11-14T12:20:45.668767",
  "severity_counts": {
    "HIGH": 0,
    "MEDIUM": 2,
    "LOW": 2,
    "total": 4
  },
  "compliance_percent": 100.0,
  "trend": "estable"
}
```
Lo cual nos permite dar una trazabilidad al avance de nuestro proyecto dentro del repositorio, con metricas que definimos previamente.