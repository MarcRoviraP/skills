---
name: memory-orchestrator
version: 1.0.0
description: |
  Skill que integra Engram automáticamente para almacenar y recuperar memoria
  persistente en proyectos gestionados por project-orchestrator.
author: Marc Rovira
---

# Memory Orchestrator

## When to use
Use this skill when:
- Starting a new project or session with `project-orchestrator` to recover previous context.
- Key decisions or plans are made that need to be persisted across sessions.
- A phase of the project is completed and a summary is needed.
- You need to search for historical decisions or information from past sessions.

## Objetivo
Proveer memoria persistente al agente para que recuerde decisiones, planes y
resultados de sesiones previas, sin intervención manual.

## Comportamiento esperado
1. Detectar si Engram está disponible.
2. Antes de ejecutar cualquier fase, recuperar contexto relevante (run $ `python scripts/memory.py context`).
3. Durante la fase, guardar decisiones clave y resultados (run $ `python scripts/memory.py save_context <title> <content>`).
4. Al finalizar, generar resumen de sesión para futuras ejecuciones (run $ `python scripts/memory.py finalize_session <summary>`).

## Funciones
- `initialize_memory()` → Conecta con Engram. Descarga el binario si no está presente.
- `save_context(title, content)` → Guarda cualquier decisión o plan.
- `get_context(query)` → Recupera información relevante por similitud o búsqueda.
- `finalize_session(summary)` → Cierra sesión y guarda resumen para la próxima.

## Flujo
1. **start_session**
   - Inicializar memoria (run $ `python scripts/memory.py init`)
   - Recuperar contexto anterior (run $ `python scripts/memory.py context`)
2. **execute_phase(phase)**
   - Guardar decisiones y resultados (run $ `python scripts/memory.py save_context`)
3. **end_session**
   - Generar resumen
   - Guardar todo en Engram (run $ `python scripts/memory.py finalize_session`)

## Quickstart
Run the following command to initialize:
```bash
python scripts/memory.py init
```
