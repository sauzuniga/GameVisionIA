# Diagnóstico Técnico — Semana 1
**Proyecto:** GameVision IA  
**Fecha:** Julio 2026

---

## Estado actual del proyecto

GameVision IA es una aplicación web funcional que permite predecir el potencial comercial de un videojuego en Steam. No es un prototipo básico: tiene backend, frontend, modelo de ML, chatbot con LLM y autenticación con Google OAuth, todo conectado y funcionando en entorno local.

---

## Partes que funcionan actualmente

- Autenticación completa con Google OAuth vía Supabase (login, logout, rutas protegidas)
- Formulario de entrada con las 22 features del modelo
- Predicción con Random Forest cargado desde `rf_model.pkl`
- Visualización del resultado con probabilidad y nivel de potencial (Alto/Medio/Bajo)
- Chatbot conversacional con Gemini 2.5 Flash, system prompt especializado y guardrails contra prompt injection
- Historial de predicciones por usuario guardado en Supabase Postgres
- Recuperación de conversaciones anteriores desde el historial
- Verificación de JWT con algoritmo ES256 (PyJWKClient)

---

## Partes manuales, incompletas o frágiles

| Parte | Problema |
|---|---|
| `rf_model.pkl` (63 MB) | No está en el repositorio; debe copiarse manualmente a `backend/` |
| Rutas absolutas hardcodeadas | `localhost:8000` en `api.js` y `localhost:5173` en el CORS de `main.py`; el proyecto no funcionará en producción sin cambiarlas a variables de entorno |
| `sessions_memory = {}` en `chat.py` | Diccionario en memoria del servidor; se pierde al reiniciar |
| Google OAuth en modo "Testing" | Solo cuentas aprobadas manualmente pueden acceder |
| Sin tests automatizados | Ninguna prueba unitaria ni de integración escrita |
| Sin Docker | No existe Dockerfile ni configuración de contenedor |
| Sin logs estructurados | Los errores solo se ven en la terminal del servidor |
| Row Level Security en Supabase | Las tablas requieren revisión de RLS y políticas por `user_id` antes de considerarse seguras para producción |
---

## Dependencias técnicas

**Backend:**
- Python 3.11
- FastAPI, Uvicorn
- scikit-learn, joblib (modelo RF)
- LangChain + langchain-google-genai (Gemini)
- SQLAlchemy + psycopg2-binary (Supabase Postgres — se recomienda usar el Session pooler en puerto 5432 para evitar problemas de resolución IPv6 en algunas redes)
- PyJWT + cryptography (verificación JWT ES256)
- python-dotenv

**Frontend:**
- Node.js 18+
- React 18 + Vite
- React Router DOM
- Axios
- @supabase/supabase-js

**Servicios externos:**
- Supabase (autenticación + base de datos Postgres)
- Google Cloud (OAuth 2.0)
- Google AI Studio (API de Gemini)

---

## Datos, archivos y credenciales necesarias

| Elemento | Dónde se obtiene |
|---|---|
| `rf_model.pkl` | Google Drive (enlace interno del equipo) |
| `GEMINI_API_KEY` | Google AI Studio (aistudio.google.com) |
| `DATABASE_URL` | Supabase → Project Settings → Database → Connection string |
| `SUPABASE_JWT_SECRET` | Supabase → Project Settings → API → JWT Settings |
| `VITE_SUPABASE_URL` | Supabase → Project Settings → API |
| `VITE_SUPABASE_ANON_KEY` | Supabase → Project Settings → API |

---

## Cómo se ejecuta actualmente

```bash
# Backend
cd backend && uvicorn main:app --reload
# → http://localhost:8000

# Frontend
cd frontend && npm run dev
# → http://localhost:5173
```

Al arrancar el backend, `Base.metadata.create_all()` crea las tablas en Supabase automáticamente si no existen.

---

## Evidencia de que el prototipo funciona

- Tablas `predictions`, `chat_sessions` y `chat_messages` activas en Supabase con datos reales de prueba
- Predicciones guardadas con `user_id` de Supabase, verificable desde el Table Editor
- Prueba con dos cuentas de Google distintas confirma aislamiento de historial por usuario
- Backend documentado automáticamente en `http://localhost:8000/docs`
