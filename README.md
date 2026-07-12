# GameVision IA
> Predictor de potencial comercial para videojuegos en Steam

## 1. Información General

**Módulo:** Módulo 4 - Desarrollo de Aplicaciones con IA  
**Semana:** Semana 1 - Diagnóstico y arquitectura inicial  
**Nombre del equipo:** Gamevision 
**Integrantes:**

- Bryan Orlando Giron Argueta
- Gerson Usiel Quintanilla Sánchez
- Saul Emmanuel Zuniga Villatoro

---

## 2. Descripción del Problema

El mercado de videojuegos en Steam es extremadamente competitivo. Cada año se publican miles de títulos y la gran mayoría no logra recuperar la inversión realizada. Los desarrolladores independientes suelen tomar decisiones de diseño comercial —como el precio, el género o la fecha de lanzamiento basándose en intuición o referencias anecdóticas, sin acceso a análisis de datos reales del mercado.

Este problema afecta principalmente a estudios indie y desarrolladores individuales que no cuentan con equipos de marketing o análisis de negocio. El contexto es la etapa de pre-producción o producción temprana de un juego, cuando aún es posible ajustar decisiones clave antes de haber invertido recursos significativos.

Una solución con IA aporta valor porque permite extraer patrones de éxito y fracaso a partir de datos históricos reales de miles de juegos publicados en Steam, entregando una estimación objetiva y fundamentada que apoya el criterio del desarrollador.

---

## 3. Usuarios o Beneficiarios

| Usuario / Beneficiario | Necesidad principal | Cómo ayuda la aplicación |
|---|---|---|
| Desarrolladores indie | Validar si su idea tiene potencial comercial antes de invertir tiempo y dinero | Entrega una probabilidad de éxito basada en datos reales de Steam junto con una explicación conversacional |
| Estudiantes de desarrollo de videojuegos | Entender qué características hacen más viable un juego en plataformas digitales | Pueden experimentar con géneros, precio y modalidad para ver cómo cambia la predicción |
| Pequeños estudios de juegos | Tomar decisiones de posicionamiento y precio con respaldo de datos | Pueden comparar múltiples escenarios usando el historial vinculado a su cuenta |

---

## 4. Descripción de la Solución

GameVision IA es una aplicación web que permite a desarrolladores estimar el potencial comercial de su idea antes de desarrollarla. El usuario ingresa las características principales del juego, precio estimado, año y mes de lanzamiento, si será gratuito, géneros y modos de juego y el sistema devuelve una probabilidad de éxito en porcentaje con una clasificación en tres niveles: Alto, Medio o Bajo.

Además del resultado numérico, la aplicación ofrece un asistente conversacional que interpreta el resultado en lenguaje natural y responde preguntas específicas sobre cómo mejorar el potencial comercial. El historial de predicciones queda guardado y vinculado a la cuenta del usuario vía autenticación con Google.

---

## 5. Componente de Inteligencia Artificial

| Elemento | Descripción |
|---|---|
| Tipo de IA utilizada | Machine Learning supervisado (clasificación binaria) + Modelo de lenguaje grande (LLM) |
| Modelo, algoritmo, servicio o técnica | Random Forest (200 árboles, scikit-learn) + Gemini 2.5 Flash vía LangChain |
| Datos de entrada | 22 features: precio, año/mes de lanzamiento, is_free, 9 géneros de Steam, 9 categorías de juego |
| Resultado generado por la IA | Probabilidad de éxito (0–100%), nivel de potencial (Alto/Medio/Bajo), respuesta conversacional |
| Métrica o forma de evaluación | Accuracy ~84%, F1-score ~47% evaluado sobre ~58,000 juegos reales de Steam |
| Limitaciones actuales | El F1 refleja el desbalance natural del dataset. El modelo no evalúa calidad gráfica, narrativa ni originalidad. |

**Explicación breve:**

El modelo Random Forest analiza las 22 características configurables del juego y las compara con patrones aprendidos de miles de juegos históricos de Steam para estimar la probabilidad de éxito comercial. El componente LLM (Gemini 2.5 Flash vía LangChain) actúa como capa de interpretación: recibe ese resultado numérico y lo convierte en una explicación comprensible, respondiendo preguntas sobre qué factores influyen en la predicción y cómo podrían ajustarse.

---

## 6. Estado Actual del Proyecto

### Funcionalidades que ya funcionan

- Autenticación completa con Google OAuth vía Supabase (login, logout, rutas protegidas)
- Formulario de entrada con las 22 features del modelo (géneros, categorías, precio, fecha, modalidad free)
- Predicción con Random Forest cargado desde `rf_model.pkl` con umbral de 0.60
- Visualización del resultado con probabilidad y nivel de potencial (Alto/Medio/Bajo)
- Chatbot conversacional con Gemini 2.5 Flash con system prompt especializado y guardrails
- Historial de predicciones por usuario guardado en Supabase Postgres
- Recuperación de conversaciones anteriores desde el historial
- Verificación de JWT con algoritmo ES256 mediante PyJWKClient

### Funcionalidades incompletas o pendientes

- Despliegue en producción (actualmente solo corre en entorno local)
- Las rutas `localhost:8000` en `api.js` y `localhost:5173` en el CORS están hardcodeadas; deben migrarse a variables de entorno antes de producción
- Google OAuth en modo "Testing"; solo cuentas aprobadas manualmente pueden acceder
- Sin tests automatizados ni pipeline CI/CD
- Sin Docker ni configuración de contenedor

### Evidencias actuales

El prototipo fue probado en entorno local y cuenta con capturas de funcionamiento en la carpeta [`docs/evidencias/`](docs/evidencias/).

Las evidencias actuales incluyen:

- Pantalla principal de la aplicación (`landing-page.png`)
- Autenticación con Google OAuth mediante Supabase (`login-google.png`)
- Formulario de predicción y resultado generado por el modelo (`formulario-resultado-prediccion.png`)
- Chatbot interpretativo conectado a Gemini (`chatbot.png`)
- Historial almacenado y recuperado por usuario (`historial-almacenado.png`)
- Registros en Supabase para predicciones (`supabase-predictions.png`)
- Registros en Supabase para sesiones de chat (`supabase-chat-sessions.png`)

---

## 7. Arquitectura Actual

Ver documento completo: [docs/arquitectura-actual.md](docs/arquitectura-actual.md)

| Componente | Descripción | Estado actual |
|---|---|---|
| Interfaz | React 18 + Vite. Landing con login, formulario, panel de resultados, chatbot e historial | Funcional |
| Backend / lógica principal | FastAPI (Python 3.11). Endpoints REST para predicción, chat e historial. Verifica JWT ES256 en cada request | Funcional |
| Componente IA — Predicción | Random Forest (scikit-learn, 200 árboles). Archivo `rf_model.pkl` de 63MB cargado en memoria al iniciar | Funcional |
| Componente IA — Chat | Gemini 2.5 Flash vía LangChain con memoria de conversación por sesión y guardrails en system prompt | Funcional |
| Datos | Supabase Postgres. Tablas: predictions (con user_id), chat_sessions, chat_messages | Funcional |
| Servicios externos | Google Cloud (OAuth 2.0), Supabase (Auth + DB), Google AI Studio (Gemini API) | Activos |
| Configuración | Variables de entorno en `.env` (backend y frontend). Sin Docker. Ejecución manual en dos terminales | Manual |

**Diagrama:** Ver [docs/arquitectura-actual.md](docs/arquitectura-actual.md)

---

## 8. Arquitectura Objetivo

Ver documento completo: [docs/arquitectura-objetivo.md](docs/arquitectura-objetivo.md)

**Elementos esperados al finalizar el módulo:**

- Rutas absolutas migradas a variables de entorno (`VITE_API_URL`, `ALLOWED_ORIGINS`)
- API versionada bajo `/api/v1/` con contratos documentados
- Tests unitarios y de integración con pipeline CI/CD en GitHub Actions
- Un solo contenedor Docker para el backend desplegado en Render
- Frontend desplegado en Vercel sin Docker (automático desde GitHub)
- Modelo `rf_model.pkl` alojado en GitHub Releases y descargado automáticamente en el build
- Logs con módulo `logging` de Python capturados por Render
- Endpoint `GET /health` para verificar estado del modelo y la base de datos
- Row Level Security (RLS) activado en Supabase
- Evaluar UptimeRobot o health checks externos para monitorear disponibilidad del backend durante la demo

**Diagrama:** Ver [docs/arquitectura-objetivo.md](docs/arquitectura-objetivo.md)
---

## 9. Estructura del Repositorio

```text
GameVisionIA/
  backend/
    routers/
      predict.py
      chat.py
      history.py
    main.py
    database.py
    models.py
    schemas.py
    auth.py
    requirements.txt
    .env.example
  frontend/
    src/
      components/
      App.jsx
      api.js
      supabaseClient.js
      main.jsx
    package.json
    .env.example
  docs/
    diagnostico-semana-1.md
    arquitectura-actual.md
    arquitectura-objetivo.md
    riesgos-tecnicos.md
    plan-mejora.md
  README.md
  .gitignore
```

**Notas sobre la estructura:**

- `backend/` — lógica del servidor FastAPI, modelos de datos SQLAlchemy, endpoints y verificación JWT
- `frontend/` — aplicación React con Vite, componentes de UI y cliente de Supabase
- `docs/` — documentación técnica del módulo 4: diagnóstico, arquitecturas, riesgos y plan de mejora
- `tests/` — reservada para pruebas automatizadas que se desarrollarán en Semana 3
- `data/` — reservada para datasets o archivos de referencia del modelo
- El archivo `rf_model.pkl` (63MB) no está en el repositorio; en local se copia manualmente, en producción se descargará desde GitHub Releases

---

## 10. Instalación y Ejecución

### Requisitos previos

- Python 3.11
- Node.js 18+
- Cuenta de Supabase con proyecto creado y Google OAuth configurado
- API key de Google Gemini (Google AI Studio)
- Archivo `rf_model.pkl` (solicitar al equipo o descargar desde el enlace compartido)

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux / Mac
pip install -r requirements.txt
```

Crear `backend/.env` con las variables requeridas, luego:

```bash
uvicorn main:app --reload
```

Backend disponible en `http://localhost:8000`  
Documentación automática en `http://localhost:8000/docs`

### Frontend

```bash
cd frontend
npm install
```

Crear `frontend/.env` con las variables requeridas, luego:

```bash
npm run dev
```

Frontend disponible en `http://localhost:5173`

### Archivo del modelo

Copiar `rf_model.pkl` manualmente a `backend/rf_model.pkl`.  
*(En producción se descargará automáticamente desde GitHub Releases)*

### Variables de entorno

**backend/.env**

| Variable | Descripción | Obligatoria |
|---|---|---|
| `GEMINI_API_KEY` | API key de Google AI Studio | Sí |
| `DATABASE_URL` | Connection string de Supabase Postgres (Session pooler, puerto 5432) | Sí |
| `SUPABASE_JWT_SECRET` | JWT Secret del proyecto en Supabase → Project Settings → API | Sí |

**frontend/.env**

| Variable | Descripción | Obligatoria |
|---|---|---|
| `VITE_SUPABASE_URL` | URL del proyecto de Supabase | Sí |
| `VITE_SUPABASE_ANON_KEY` | Anon/public key de Supabase | Sí |

Ver archivos `.env.example` en cada carpeta como referencia.

---

## 11. Datos Utilizados

| Fuente de datos | Tipo de datos | Uso dentro del proyecto | Observaciones |
|---|---|---|---|
| Steam Store (dataset público de Kaggle) | Datos históricos de ~58,000 juegos: género, precio, categorías, fecha de lanzamiento, métricas de éxito | Entrenamiento del modelo Random Forest | Dataset público, no contiene datos personales |
| Supabase Postgres | Predicciones, sesiones de chat y mensajes generados por usuarios de la app | Almacenamiento del historial por usuario | Datos generados por la aplicación, vinculados a user_id |
| Google AI Studio (Gemini API) | Mensajes del usuario enviados al chatbot | Generación de respuestas conversacionales | Servicio externo; los mensajes se envían a la API de Gemini |

**Consideraciones:**

- El dataset de Steam es público y no contiene información sensible
- Los datos de usuarios se almacenan en Supabase con autenticación; cada usuario solo accede a los suyos
- El modelo ya está entrenado; no se requiere el dataset original para ejecutar la aplicación
- Las tablas de Supabase aún no tienen Row Level Security activado; se planea aplicar políticas básicas por `user_id` en Semana 3 y auditarlas en Semana 6.
---

## 12. Riesgos Técnicos y Deuda Técnica

Ver documento completo: [docs/riesgos-tecnicos.md](docs/riesgos-tecnicos.md)

| Riesgo | Categoría | Probabilidad | Impacto | Mitigación propuesta |
|---|---|---|---|---|
| `rf_model.pkl` de 63MB no está en el repo | Datos | Media | Alto | Alojar en GitHub Releases; el Dockerfile lo descarga con `wget` |
| Chatbot depende de API externa de Gemini | Modelo | Media | Alto | Manejo de error graceful que informe al usuario si el servicio falla |
| Memoria de chat en RAM se borra al reiniciar | Código | Alta | Medio | Persistir en tabla `chat_messages` que ya existe en la DB |
| Rutas `localhost` hardcodeadas en frontend y CORS | Código | Alta | Alto | Migrar a `VITE_API_URL` y `ALLOWED_ORIGINS` en Semana 2 |
| Conexión directa a Supabase puede fallar por IPv6 | Configuración | Media | Alto | Usar Session pooler de Supabase (puerto 5432) |
| Sin tests automatizados | Código | Alta | Medio | Escribir tests unitarios y de integración en Semana 3 |
| RLS desactivado en Supabase | Seguridad | Media | Medio | Activar políticas básicas por `user_id` en Semana 3 y auditar seguridad en Semana 6 |
| Render duerme el servidor tras 15 min sin uso | Despliegue | Alta | Medio | Configurar UptimeRobot para ping cada 10 minutos |

---

## 13. Plan de Mejora por Semana

| Semana | Mejora esperada | Evidencia esperada |
|---|---|---|
| Semana 2 | Eliminar rutas hardcodeadas, versionar API bajo `/api/v1/`, validaciones Pydantic robustas, manejo de errores estructurado | Variables de entorno funcionando, Swagger actualizado en `/docs`, respuestas de error consistentes |
| Semana 3 | Tests unitarios del modelo y endpoints, pipeline CI/CD en GitHub Actions, activar políticas RLS básicas por `user_id` | Badge de CI en README, resultados de tests en GitHub Actions, evidencia de políticas RLS aplicadas |
| Semana 4 | Dockerfile para el backend, modelo en GitHub Releases, frontend en Vercel, backend en Render, UptimeRobot activo | URL pública funcional de la aplicación completa accesible desde el navegador |
| Semana 5 | Logs con módulo `logging` de Python, persistir memoria del chat en DB, endpoint `/health` | Logs visibles en dashboard de Render, chat que mantiene historial al reiniciar el servidor |
| Semana 6 | Auditar seguridad y validar acceso por usuario, limpiar exposición de errores, OAuth fuera de modo Testing, documentación final | Demo en producción, README con URL real, defensa técnica preparada |

---

## 14. Limitaciones Actuales

- El modelo fue entrenado con datos históricos de Steam hasta una fecha específica; no refleja tendencias recientes del mercado
- El F1-score de ~47% indica dificultad para identificar correctamente juegos exitosos debido al desbalance natural del dataset
- El chatbot depende de la API externa de Gemini; sin conexión a internet o sin cuota disponible no funciona
- La memoria de conversación del chatbot se pierde si el servidor se reinicia
- El modelo OAuth está en modo "Testing"; solo cuentas aprobadas manualmente pueden acceder
- El archivo `rf_model.pkl` de 63MB no puede incluirse en el repositorio por su tamaño
- No existen tests automatizados ni pipeline de CI/CD
- El proyecto actualmente requiere abrir dos terminales y configurar manualmente los archivos `.env`

---

## 15. Evidencias

| Evidencia | Enlace o ubicación | Descripción |
|---|---|---|
| Landing page | [Ver captura](docs/evidencias/LandingPage.png) | Pantalla principal de GameVision IA |
| Login con Google | [Ver captura](docs/evidencias/LoginGoogle.png) | Autenticación con Google OAuth mediante Supabase Auth |
| Formulario y resultado de predicción | [Ver captura](docs/evidencias/formulario-resultado-prediccion.png) | Entrada de datos del videojuego y resultado generado por el modelo |
| Chatbot | [Ver captura](docs/evidencias/Chatbot.png) | Asistente conversacional interpretando el resultado |
| Historial almacenado | [Ver captura](docs/evidencias/HistorialAlmacenado.png) | Recuperación de predicciones o conversaciones previas |
| Tabla `predictions` en Supabase | [Ver captura](docs/evidencias/supabasepredictions.png) | Predicciones almacenadas con `user_id`, probabilidad y nivel de potencial |
| Tabla `chat_sessions` en Supabase | [Ver captura](docs/evidencias/supabase_chat_sessions.png) | Sesiones de conversación almacenadas en la base de datos |

---

## 16. Créditos y Referencias

- [scikit-learn](https://scikit-learn.org/) — Random Forest y pipeline de ML
- [FastAPI](https://fastapi.tiangolo.com/) — Framework del backend
- [LangChain](https://python.langchain.com/) — Orquestación del chatbot con memoria de conversación
- [Google Gemini 2.5 Flash](https://ai.google.dev/) — Modelo LLM para el asistente conversacional
- [Supabase](https://supabase.com/) — Autenticación con Google OAuth y base de datos Postgres
- [React](https://react.dev/) + [Vite](https://vitejs.dev/) — Framework del frontend
- [Dataset público de videojuegos de Steam](https://drive.google.com/file/d/13IYfQMRxx3-ZS70z5Hjs2ir8kre_j2_z/view?usp=sharing) — Dataset utilizado como base para entrenar el modelo Random Forest de GameVision IA.
---

