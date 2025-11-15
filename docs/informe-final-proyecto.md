# Informe Final del Proyecto – Repo-Compliance

## 1. Resumen general

Repo-Compliance es un auditor automatizado para repositorios Git que verifica el cumplimiento de políticas técnicas basadas en los principios 12-Factor, buenas prácticas de seguridad, linters, cobertura mínima y estandarización de workflows.  
El proyecto integra herramientas de automatización (Makefile, GitHub Actions) y publica resultados en GitHub Projects para dar seguimiento a tendencias y métricas.

---

## 2. Métricas del proyecto

### 2.1 Velocity por sprint

La velocity se midió utilizando el tablero Kanban en GitHub Projects, basado en issues completados:

| Sprint | Issues completados | Velocity |
|--------|--------------------|----------|
| **Sprint 1** (Issues 1.1–1.4) | 4 | Alta |
| **Sprint 2** (Issues 2.1–2.4) | 4 | Estable |
| **Sprint 3** (Issues 3.1–3.3) | 2 completados + 1 en progreso | Buena |

**Total issues:** 11  
**Total completados:** 10  
**% completado del proyecto:** ~91%

El flujo fue consistente en los tres sprints, con entregables equilibrados y un ritmo sostenido.

---

### 2.2 Cumplimiento y calidad

El tablero muestra que los issues alcanzaron niveles altos de cumplimiento:

- Valores entre **85% y 100%**
- **Tendencia: “Mejora”** en absolutamente todos los issues
- El proyecto mantuvo la calidad de implementación durante los sprints, especialmente en:
  - Regla de `.env` en `.gitignore`
  - Reglas de auditoría base
  - Pruebas unitarias con parametrización
  - Integración CI/CD con GitHub Actions
  - Generación y formateo de reportes

---

### 2.3 Cobertura

Se estableció una cobertura mínima requerida del **90%**.  
Los módulos de auditoría principales (reglas, reporter, simulación de API) alcanzaron:

- **Cobertura ≥ 90%**, validada mediante `pytest` + `coverage`
- Pruebas con parametrización (`pytest.mark.parametrize`)
- Uso de mocks (`patch.object`, `monkeypatch`) para aislar filesystem y repos ficticios

La cobertura se mantuvo estable durante los tres sprints.

---

### 2.4 Cycle time

El cycle time promedio (tiempo desde *In Progress* hasta *Done*) fue:

- **1–3 días por issue**, según la estimación (3–8 puntos en tablero).
- Issues más largos: configuración de CI/CD y pruebas parametrizadas.
- Issues más cortos: documentación, métricas y reportes.

---

### 2.5 Blocked time

Los bloqueos principales ocurrieron durante:

- Configuración inicial de GitHub Actions  
  (problemas de rutas y versiones de Python)
- Ajustes de formateadores y linters (`black`, `isort`, `flake8`)
- Sincronización entre reportes, pipeline y estructura del proyecto

Sin embargo, los bloqueos fueron temporales y el flujo mejoró con cada sprint.

---

## 3. Tendencias observadas

Las métricas y el tablero reflejan una tendencia general de **Mejora**, consistente en:

- **Menos hallazgos** conforme avanzaban los sprints.
- Mayor estabilidad en pipelines.
- Mejor calidad de código (menos reformateos tras integrar linters).
- Progreso más rápido en Sprints 2 y 3 por aprendizaje del flujo CI/CD.
- Documentación progresivamente más completa.

En resumen: **la deuda técnica disminuyó sprint a sprint**.

---

## 4. Lecciones aprendidas

1. La automatización desde el inicio (lint, tests y CI/CD) reduce retrabajo.
2. Las pruebas parametrizadas permiten evaluar múltiples repos rápidamente.
3. Simular la API de GitHub facilita avanzar sin depender de tokens reales.
4. Dividir issues grandes en subtareas mejora el cycle time.
5. Los reportes JSON/MD permiten trazabilidad clara de hallazgos.
6. GitHub Actions como “filtro de calidad” es clave para evitar merges defectuosos.

---

## 5. Trabajo futuro

- Configurar interacción real con GitHub Projects mediante la API oficial.
- Implementar reglas avanzadas de detección de secretos con perfiles personalizados.
- Crear dashboards de tendencias automatizados (gráficos o paneles).
- Publicar Repo-Compliance como CLI o como GitHub Action reutilizable.

---

## 6. Conclusión

Repo-Compliance cumplió con los objetivos planteados:  
se desarrolló un auditor funcional, con CI/CD, reporte automatizado, pruebas robustas y métricas visibles en el tablero. Las tendencias demostraron mejora continua y un flujo de trabajo consolidado sprint tras sprint.
