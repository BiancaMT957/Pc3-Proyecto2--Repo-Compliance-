## Sprint 1


| Fecha | Integrantes | Qué hice ayer                                                                               | Qué haré hoy                                             | Bloqueos                            |
| ----- | ----------- | ------------------------------------------------------------------------------------------- | -------------------------------------------------------- | ----------------------------------- |
| Día 1 | Bianca       | Inicialicé el repositorio y carpetas (auditor/, tests/, docs/, .github/workflows/). | Crear Makefile con targets lint, test, coverage. Cree issues y les puse sus campos y su etiquetas sorrespondientes en el talbero Kanban | Ninguno                             |
| Día 2 | Bianca     | Escribí Makefile; configuré pytest.ini y conftest.py.  Corregio pytest y rutas; instalo pre-commit                               | Validar que make test genere out/coverage.xml.  Agregar hooks (flake8, commitlint).                 | Error al generar cobertura.         |
| Día 2 | Bianca       | Ajusto hooks y documentamos en docs/hooks.md.                                          | Implemento funciones iniciales del auditor.             | Falto definir formato de salida.    |
| Día 3 | Luis  | Implementamos check_env_in_gitignore y check_license_file.                              | Crear run_audit() y testear funciones.                 | Tests parametrizados incompletos.   |
| Día 3 | Luis      | Escribimos tests con @pytest.mark.parametrize; ejecutamos cobertura (87 %).               | Revisar documentación.                                   | Ninguno                             |
| Día 3 | Bianca      | Revisamos README y evidencia.                                                               | Cierre del sprint1.                                       | —                                   |

## Sprint2


| Fecha | Integrantes | Qué hice ayer                                                                               | Qué haré hoy                                             | Bloqueos                            |
| ----- | ----------- | ------------------------------------------------------------------------------------------- | -------------------------------------------------------- | ----------------------------------- |
| Día 4 | Bianca       | Cree el compliance.yml, agregue LICENSE,hize cambios a core.py para que me detecte el HIGH,  | Pondre la ejecucion en la carpeta de evidencias, tambien explicare lo que hize en la carpeta docs| Ninguno                            |
| Dia 5 | Luis  | Implementé la simulación del flujo completo del auditor. Verifiqué el funcionamiento de `run_audit()` y `report.py` generando `out/report.json` y `out/report.md`. Configuré el workflow Compliance CI para que ejecute el auditor y genere los reportes automáticamente. Ajusté los tests para usar repositorios inválidos simulados y confirmé que el pipeline bloquea en presencia de findings HIGH. | Crear carpeta `tests/demo_repo_invalid/` con ejemplos de repos defectuosos, probar ejecución local con `act` y registrar `blocked_time` en los issues afectados. | Pendiente registrar `blocked_time` automático en el flujo (solo simulado localmente). |
| Dia 6 | Luis | Probé la ejecución completa del auditor con `report.py`, verificando que se generen los archivos `report.json`, `report.md` y `blocked_time.json`. También comprobé el funcionamiento del workflow Compliance CI en GitHub Actions y la creación automática del artifact `audit-reports`. | Registrar evidencias del flujo completo (capturas de los jobs, artifacts y reportes generados) y documentarlas en la bitácora del sprint. | Pendiente integrar el campo `blocked_time` al flujo CI/CD (solo simulado localmente). |

## Sprint 3

| Fecha | Integrantes | Qué hice ayer                                                                               | Qué haré hoy                                             | Bloqueos                            |
| ----- | ----------- | ------------------------------------------------------------------------------------------- | -------------------------------------------------------- | ----------------------------------- |
| Día 7 | Luis       | Creé la estructura inicial del módulo `auditor/github_api.py` y preparé los primeros mocks para pruebas con `unittest.mock`. | Implementar funciones para mover tarjetas y comentar PRs simulando la API de GitHub. Completar pruebas unitarias usando autospec para validar que las llamadas se hagan correctamente sin depender de la API real.| Ninguno |
| Día 8 | Luis       | Implementé el módulo `auditor/metrics.py` con funciones auxiliares para el calculo de metricas de tendencia y porcentaje de cumplimiento de las reglas. | Integrar métricas en el pipeline del auditor, generar evidence/sprint-3/metrics.json y validar que el cálculo de tendencias funcione comparando un prev.json con un reporte actual. | Ninguno 