# Plan de Mejora 
**Proyecto:** GameVision IA  
**Módulo:** 4 - Desarrollo de Aplicaciones con IA

---

## Semana 2 — API inteligente y contratos de entrada/salida

**Objetivo:** Hacer que la API sea más robusta, documentada y predecible.

| Acción | Detalle |
|---|---|
| Configuración de URLs por entorno | Mantener `VITE_API_URL` en `frontend/.env` y `ALLOWED_ORIGINS` en `backend/.env` para separar desarrollo local y despliegue |
| Versionar la API | Mover todos los endpoints a `/api/v1/` |
| Mejorar schemas Pydantic | Agregar validaciones de rango (precio ≥ 0, año válido, al menos un género seleccionado) |
| Manejo de errores estructurado | Devolver respuestas de error con formato consistente `{error, detail, code}` |
| Documentar contratos | Revisar y completar la documentación automática de FastAPI en `/docs` |
| Validar input del modelo | Rechazar predicciones con datos incoherentes antes de llegar al RF |

**Riesgo a mitigar esta semana:** #11 (rutas hardcodeadas), #4 (sin validaciones robustas) y parte del #6 (configuración frágil)

---

## Semana 3 — Pruebas y CI/CD

**Objetivo:** Que cualquier cambio en el código se pueda verificar automáticamente.

| Acción | Detalle |
|---|---|
| Tests unitarios del modelo | Verificar que `rf_model.pkl` carga correctamente y devuelve probabilidades válidas (0–1) |
| Tests del endpoint `/predict` | Enviar un payload válido y verificar que la respuesta tiene `probability`, `potential_level` y `session_id` |
| Tests del endpoint `/history` | Verificar que solo devuelve predicciones del usuario autenticado |
| GitHub Actions | Configurar workflow que corra los tests en cada push a `main` |
| Seguridad inicial de datos | Activar RLS básico en Supabase y crear políticas por `user_id` |
| Badge de estado | Agregar badge de CI al README |

**Riesgo a mitigar esta semana:** #4 (sin tests) y #7 (RLS desactivado en Supabase)

---

## Semana 4 — Contenedor y despliegue

**Objetivo:** Que el proyecto pueda ejecutarse en cualquier máquina y estar accesible en internet.

| Acción | Detalle |
|---|---|
| Dockerfile para el backend | Imagen basada en `python:3.11-slim`, instala dependencias, copia código |
| Alojar el modelo en GitHub Releases | Subir `rf_model.pkl` como asset de un Release (límite 2GB); el Dockerfile lo descarga con `wget` |
| Despliegue del frontend | Conectar el repositorio a Vercel; detecta React/Vite automáticamente, sin Docker |
| Despliegue del backend | Usar Render con el Dockerfile (un solo contenedor) |
| Variables de entorno en producción | Configurar las variables en los dashboards de Render y Vercel |
| Monitoreo de disponibilidad | Evaluar UptimeRobot o health checks externos para verificar disponibilidad del backend durante la demo |
**Riesgo a mitigar esta semana:** #1 y #9 (modelo fuera del repo), #5 (dependencias pesadas)

---

## Semana 5 — Observabilidad, rendimiento y escalabilidad

**Objetivo:** Que el equipo pueda monitorear qué pasa en producción.

| Acción | Detalle |
|---|---|
| Logs con módulo estándar de Python | Reemplazar `print()` por `logging` (INFO, ERROR, timestamps); Render los captura automáticamente en su dashboard sin servicios externos |
| Tiempo de inferencia | Registrar cuánto tarda el modelo en responder y cuánto tarda Gemini |
| Persistir memoria del chat | Eliminar `sessions_memory = {}` y cargar historial desde `chat_messages` en cada request (la tabla ya existe) |
| Endpoint de salud | Agregar `GET /health` que verifique que el modelo está cargado y la DB responde |
| Límites de requests | Agregar rate limiting básico en los endpoints del chatbot |

**Riesgo a mitigar esta semana:** #3 (memoria de chat en RAM), #2 (fallos del chatbot sin manejo)

---

## Semana 6 — Seguridad, documentación final y defensa técnica

**Objetivo:** Dejar el proyecto defendible, seguro y documentado completamente.

| Acción | Detalle |
|---|---|
| Publicar OAuth | Solicitar verificación de Google Cloud o al menos salir del modo Testing |
| Limpiar exposición de errores | Asegurarse de que la API no devuelve stack traces ni información interna en producción |
| README final | Actualizar con evidencias de producción, métricas reales y enlace a demo |
| Preparar defensa | Documentar decisiones técnicas, riesgos resueltos y lecciones aprendidas |
| Auditar RLS | Verificar que las políticas de Supabase solo permiten consultar, insertar o modificar datos asociados al `user_id` autenticado |
**Riesgo a mitigar esta semana:** #7 (RLS), #8 (OAuth Testing), #10 (solo una 2 o personas entienden realmente el proyecto)
