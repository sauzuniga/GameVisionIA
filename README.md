# GameVision IA
> Predictor de potencial comercial para videojuegos en Steam

## 1. Información General

**Módulo:** Módulo 4 - Desarrollo de Aplicaciones con IA  
**Semana:** Semana 6 - Seguridad, versionamiento y defensa técnica final (documento acumulativo desde Semana 1)  
**Nombre del equipo:** GameVision  
**URL en producción (backend):** https://gamevisionia.onrender.com  
**URL en producción (frontend):** https://game-vision-ia.vercel.app  
**Release / tag:** [`v1.0.0-rc.1`](https://github.com/sauzuniga/GameVisionIA/releases/tag/v1.0.0-rc.1) — ver [release-manifest.yml](release-manifest.yml) para el commit exacto y los componentes de cada versión  
**Informe final:** [`docs/final/informe-final.md`](docs/final/informe-final.md)  
**Presentación final:** [`docs/final/presentacion-final.pdf`](docs/final/presentacion-final.pdf)  
**Integrantes:**

- Bryan Orlando Girón Argueta
- Gerson Usiel Quintanilla Sánchez
- Saúl Emmanuel Zúñiga Villatoro

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
- Endpoint GET /health que verifica el estado del modelo y la base de datos
- Endpoint GET /metadata con información del modelo, métricas y contrato de la API
- Endpoint POST /api/predict-demo público (sin JWT) para pruebas externas
- Capa de servicios separada en backend/services/predict_service.py
- Validaciones de entrada con rangos y reglas de negocio en schemas.py
- Manejo controlado de errores con códigos HTTP descriptivos (422, 503, 500)
- Suite de 19 pruebas automatizadas (pytest) cubriendo salud, servicio IA, contrato público, validación, autenticación, chatbot y observabilidad — ver [docs/pruebas.md](docs/pruebas.md)
- Pipeline CI/CD en GitHub Actions (`.github/workflows/ci.yml`): instala dependencias, ejecuta Ruff y pytest y, tras un `push` exitoso a `main`, activa el despliegue en Render mediante un Deploy Hook
- Backend contenerizado con Docker (construcción multietapa, usuario sin privilegios) y desplegado públicamente en Render 
- Modelo `rf_model.pkl` alojado en GitHub Releases, descargado automáticamente durante el build de Docker
- Pipeline CI/CD completo: GitHub Actions ejecuta las pruebas y, si pasan, dispara automáticamente el despliegue en Render vía Deploy Hook (confirmado con la etiqueta "Triggered via Deploy Hook" en el panel de eventos de Render)
- Frontend desplegado en Vercel (https://game-vision-ia.vercel.app), conectado al backend en producción — el flujo login → predicción → chat → historial funciona de punta a punta en producción real
- Middleware de observabilidad global (`main.py`): genera `request_id`, mide `duration_ms`, agrega headers `X-Request-ID` / `X-Process-Time-Ms`, y aplica a **todos** los endpoints, no solo a `/predict`
- Tabla `request_logs` en Supabase, con desglose interno de tiempos (`validate_ms`, `feature_prep_ms`, `inference_ms`) para las predicciones, guardado como `BackgroundTask` para no sumarse a la latencia medida
- Retención automática de logs vía `pg_cron` (job `purge_request_logs_30d`, corre diario, borra filas con más de 30 días) — ver [backend/scripts/setup_retention.sql](backend/scripts/setup_retention.sql)
- Script de línea base de rendimiento (`backend/scripts/benchmark_predict.py`) con cálculo de p50/p95/máx/tasa de error sobre `/predict-demo`, `/predict` real y `/chat`
- Optimización aplicada en `/api/predict`: se redujo de 4 a 2-3 viajes de red hacia Supabase (uso de `flush()` en vez de dos ciclos de `commit()`+`refresh()`), con -58.6% de reducción medida en el overhead de autenticación + base de datos
- Google OAuth publicado a producción (fuera de modo "Testing") — cualquier cuenta de Google puede autenticarse, no solo cuentas aprobadas manualmente
- Row Level Security (RLS) activado en las 4 tablas públicas de Supabase (`predictions`, `chat_sessions`, `chat_messages`, `request_logs`) — ver [backend/scripts/enable_rls.sql](backend/scripts/enable_rls.sql)
- Corrección de vulnerabilidad IDOR en el chat: `POST /api/chat` y `GET /api/chat/{id}/messages` ahora verifican que la sesión le pertenezca al usuario autenticado antes de permitir acceso — probado con test adversarial automatizado y en producción real (acceso cruzado entre cuentas → 404)
- Timeout explícito de 20s en la llamada a Gemini (antes sin límite; una llamada real había tardado 177s) — responde 504 controlado si se excede
- Mensajes de error ya no exponen detalles internos de excepciones al cliente; el detalle real solo se registra en el log del servidor
- Tag y release publicados en GitHub (`v1.0.0-rc.1`), con manifiesto de versión (`release-manifest.yml`) documentando código, modelo, componente conversacional y pruebas

### Funcionalidades incompletas o pendientes

- Rate limiting en `/predict` y `/chat` — decisión consciente de no implementarlo tan cerca de la defensa final, por el riesgo de romper algo sin tiempo de probarlo a fondo
- Prueba de carga concurrente (las mediciones de Semana 5 fueron secuenciales, no simulan múltiples usuarios al mismo tiempo)
- Versionado formal del prompt del chatbot
- Rollback probado en un ensayo real (mecanismo confirmado disponible en Render; ejecución de prueba programada para el freeze previo a la defensa)

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
| Componente IA — Predicción | Random Forest (scikit-learn, 200 árboles). El archivo `rf_model.pkl` se almacena en GitHub Releases, se descarga durante el build de Docker y se carga en memoria al iniciar | Funcional en Render |
| Componente IA — Chat | Gemini 2.5 Flash vía LangChain con memoria de conversación por sesión y guardrails en system prompt | Funcional |
| Datos | Supabase Postgres. Tablas: predictions (con user_id), chat_sessions, chat_messages | Funcional |
| Servicios externos | Render, Vercel, Supabase (Auth + PostgreSQL), Google Cloud OAuth, Google AI Studio (Gemini API) y GitHub Releases | Activos |
| Configuración | Backend contenerizado con Docker, desplegado en Render con variables de entorno gestionadas en el panel del servicio. Frontend desplegado en Vercel con build automático desde GitHub | Backend y frontend en producción |
| Observabilidad | Middleware global en `main.py` + tabla `request_logs` en Supabase con retención automática de 30 días (`pg_cron`) | Funcional en producción |
| Seguridad | OAuth publicado a producción, RLS activo en las 4 tablas, IDOR corregido y probado, timeout de 20s en Gemini, errores sin exponer detalles internos | Funcional en producción |

**Diagrama:** Ver [docs/arquitectura-actual.md](docs/arquitectura-actual.md)

---

## 8. Arquitectura Objetivo

Ver documento completo: [docs/arquitectura-objetivo.md](docs/arquitectura-objetivo.md)

**Elementos esperados al finalizar el módulo:**

- ✅ Rutas absolutas migradas a variables de entorno (`VITE_API_URL`, `ALLOWED_ORIGINS`)
- API versionada bajo `/api/v1/` con contratos documentados — pendiente
- ✅ Tests unitarios y de integración con pipeline CI/CD en GitHub Actions
- ✅ Un solo contenedor Docker para el backend desplegado en Render
- ✅ Frontend desplegado en Vercel sin Docker (automático desde GitHub)
- ✅ Modelo `rf_model.pkl` alojado en GitHub Releases y descargado automáticamente en el build
- ✅ Logs estructurados en JSON (módulo `logging` de Python) capturados por Render, más persistencia en tabla `request_logs` de Supabase con retención automática de 30 días
- ✅ Endpoint `GET /health` para verificar estado del modelo y la base de datos
- ✅ Línea base de rendimiento documentada (p50/p95/máx/error) con comparación antes/después de una mejora aplicada
- ✅ Row Level Security (RLS) activado en Supabase
- ✅ Timeout explícito en la llamada a Gemini
- ✅ OAuth de Google publicado a producción (fuera de modo Testing)
- ✅ Tag y release publicados en GitHub, con manifiesto de versión
- Rate limiting en endpoints de predicción y chat — pendiente, declarado como limitación aceptada
- Evaluar UptimeRobot o health checks externos para monitorear disponibilidad del backend durante la demo — pendiente

**Diagrama:** Ver [docs/arquitectura-objetivo.md](docs/arquitectura-objetivo.md)
---

## 9. Estructura del Repositorio

```text
GameVisionIA/
  .github/
    workflows/
      ci.yml
  backend/
    routers/
      predict.py
      chat.py
      history.py
    services/
      __init__.py
      predict_service.py
    tests/
      conftest.py
      test_health.py
      test_predict_service.py
      test_predict_demo.py
      test_validation.py
      test_predict_auth.py
      test_chat.py
      test_observability.py
    scripts/
      benchmark_predict.py
      setup_retention.sql
      enable_rls.sql
    main.py
    database.py
    models.py
    schemas.py
    auth.py
    Dockerfile
    .dockerignore
    requirements.txt
    requirements-dev.txt
    pyproject.toml
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
    plan-infraestructura.md
    plan-mejora.md
    api.md
    pruebas.md
    registro-errores-semana-3.md
    evidencias/
    final/
      plan-contingencia-demo.md
      informe-final.md          # pendiente
      informe-final.pdf         # pendiente
      presentacion-final.pdf    # pendiente
      respaldo/                 # pendiente (capturas de respaldo para el freeze)
  release-manifest.yml
  README.md
  .gitignore
```

**Notas sobre la estructura:**

- `backend/` — lógica del servidor FastAPI, modelos de datos SQLAlchemy, endpoints, verificación JWT y `Dockerfile` para contenerizar el servicio
- `frontend/` — aplicación React con Vite, componentes de UI y cliente de Supabase
- `docs/` — documentación técnica del módulo 4: diagnóstico, arquitecturas, riesgos, pruebas, infraestructura, costos y registro de errores por semana
- `docs/final/` — entregables de la evaluación final: informe integrador, presentación y plan de contingencia de la demo. **A la fecha de este README, solo `plan-contingencia-demo.md` existe; el informe y la presentación finales están en construcción**
- El archivo `rf_model.pkl` (63MB) no está en el repositorio; en local se copia manualmente, en producción el `Dockerfile` lo descarga automáticamente desde GitHub Releases durante el build

---

## 10. Instalación y Ejecución

### Requisitos previos

- Python 3.11
- Node.js 18+
- Cuenta de Supabase con proyecto creado y Google OAuth configurado
- API key de Google Gemini (Google AI Studio)
- Docker Desktop, si se utilizará la ejecución mediante contenedor
- Archivo `rf_model.pkl` únicamente para la ejecución manual sin Docker

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

### Ejecutar el backend con Docker

Alternativa a instalar Python localmente — construye una imagen que descarga el modelo automáticamente desde GitHub Releases:

```bash
cd backend
docker build -t gamevision-backend .
docker run -p 8000:8000 --env-file .env gamevision-backend
```

Backend disponible en `http://localhost:8000`, igual que con `uvicorn` directo.

### Despliegue actual

- **Backend en Render:** https://gamevisionia.onrender.com
- **Health check:** https://gamevisionia.onrender.com/health
- **Documentación Swagger:** https://gamevisionia.onrender.com/docs
- **Frontend en Vercel:** https://game-vision-ia.vercel.app

Nota: el plan gratuito de Render suspende el backend tras ~15 minutos sin tráfico. La primera petición tras ese período puede tardar hasta ~50-55 segundos en responder (cold-start medido y documentado en Semana 5).

### Probar la API

Una vez corriendo el backend, se pueden probar los endpoints públicos desde:

**Swagger UI:** `http://localhost:8000/docs`

**curl:**
```bash
curl -X GET "http://localhost:8000/health"
curl -X GET "http://localhost:8000/metadata"
```
Ver documentación completa en [docs/api.md](docs/api.md)

### Archivo del modelo

El modelo entrenado no se incluye directamente en el repositorio debido a su tamaño. Está publicado como asset en GitHub Releases:

[Descargar modelo Random Forest (`rf_model.pkl`)](https://github.com/sauzuniga/GameVisionIA/releases/download/model-v1.0.0/rf_model.pkl)

El `Dockerfile` lo descarga automáticamente durante la construcción de la imagen. Para ejecutar el backend manualmente sin Docker, debe descargarse y colocarse en:

```text
backend/rf_model.pkl
```

**Notebook de entrenamiento:** el proceso de limpieza de datos, entrenamiento y evaluación del modelo (de donde salen las métricas de accuracy ~84% y F1 ~47% citadas en este README) está documentado en [Google Colab](https://colab.research.google.com/drive/1rz4PfT_a_I4DltkfnBvSCp5shMwzzWYw?usp=sharing).

### Variables de entorno

**backend/.env**

| Variable | Descripción | Obligatoria |
|---|---|---|
| `GEMINI_API_KEY` | API key de Google AI Studio | Sí |
| `DATABASE_URL` | Cadena de conexión de Supabase Postgres — usar el **Session Pooler** (no la conexión directa, que falla por IPv6 dentro de Docker) con `?sslmode=require` al final | Sí |
| `SUPABASE_JWT_SECRET` | JWT Secret del proyecto en Supabase → Project Settings → API | Sí |
| `ALLOWED_ORIGINS` | Orígenes permitidos para CORS, por ejemplo `http://localhost:5173` | Sí |
| `TEST_ACCESS_TOKEN` | JWT de una cuenta de prueba, usado solo por `scripts/benchmark_predict.py` para medir `/predict` y `/chat` reales | No (solo para benchmark) |
| `BENCHMARK_BASE_URL` | Ambiente contra el que corre el benchmark; por defecto `https://gamevisionia.onrender.com` | No (solo para benchmark) |

**frontend/.env**

| Variable | Descripción | Obligatoria |
|---|---|---|
| `VITE_SUPABASE_URL` | URL del proyecto de Supabase | Sí |
| `VITE_SUPABASE_ANON_KEY` | Anon/public key de Supabase | Sí |
| `VITE_API_URL` | URL base del backend, por ejemplo `http://localhost:8000/api` | Sí |

Ver archivos `.env.example` en cada carpeta como referencia.

### Valores según el entorno

**Desarrollo local**

```env
ALLOWED_ORIGINS=http://localhost:5173
VITE_API_URL=http://localhost:8000/api
```

**Producción (valores reales en uso)**

```env
ALLOWED_ORIGINS=https://game-vision-ia.vercel.app
VITE_API_URL=https://gamevisionia.onrender.com/api
```

Las variables sensibles del backend se administran desde el panel de Render. Las variables públicas del frontend se administran desde el panel de Vercel.

### Medir la línea base de rendimiento (Semana 5)

```bash
cd backend
pip install requests   # única dependencia adicional para el script
```

Se necesita un `TEST_ACCESS_TOKEN` en `backend/.env` — un JWT real de una cuenta de Google cualquiera (el OAuth ya está publicado a producción desde Semana 6, así que no hace falta que la cuenta esté pre-aprobada como test user). Para obtenerlo: loguearse en https://game-vision-ia.vercel.app con esa cuenta, abrir las herramientas de desarrollador del navegador (F12) → pestaña Application/Almacenamiento → Local Storage → buscar la clave `sb-<project-ref>-auth-token` → copiar el valor de `access_token` de ahí. El token expira en aproximadamente 1 hora. Opcionalmente se puede definir `BENCHMARK_BASE_URL` para apuntar a un ambiente distinto al de producción. Luego:

```bash
python scripts/benchmark_predict.py
```

El script despierta el servicio, corre 20 peticiones secuenciales contra `/api/predict-demo`, 20 contra `/api/predict` (real, autenticado) y una muestra de 3 contra `/api/chat`, calcula p50/p95/máx/tasa de error, y guarda los resultados en `docs/evidencias/linea_base_rendimiento.json` (incluye ambiente, payload usado y commit de código de esa corrida). Sin `TEST_ACCESS_TOKEN` configurado, el script corre igual pero solo mide `/predict-demo`.

### Activar la retención automática de logs (una sola vez)

El archivo [`backend/scripts/setup_retention.sql`](backend/scripts/setup_retention.sql) contiene el SQL para activar `pg_cron` en Supabase y programar el borrado diario de filas de `request_logs` con más de 30 días. Se corre una única vez desde el **SQL Editor** del panel de Supabase (no requiere acceso desde la terminal ni variables de entorno adicionales).

---

## API inteligente - Semana 2

La funcionalidad principal de IA fue expuesta mediante endpoints consumibles desde Swagger, curl o Postman.

| Método | Endpoint | Autenticación | Descripción |
|---|---|---|---|
| GET | `/health` | No requiere | Verifica que el servicio, el modelo y la base de datos estén disponibles |
| GET | `/metadata` | No requiere | Devuelve información del proyecto, modelo, métricas y endpoints |
| POST | `/api/predict-demo` | No requiere | Ejecuta el modelo Random Forest real sin guardar historial |
| POST | `/api/predict` | Requiere JWT | Ejecuta la predicción real y guarda historial asociado al usuario |

La documentación técnica de la API está en [`docs/api.md`](docs/api.md).

Las evidencias de prueba con Swagger y curl están en [`docs/evidencias/evidencias-api-semana-2.pdf`](docs/evidencias/evidencias-api-semana-2.pdf).

---

## Pruebas y CI/CD — Semanas 3 y 4

Se agregó una suite de **19 pruebas automatizadas** con `pytest` (15 desde Semana 3, ampliada con 4 más en Semana 5), cubriendo siete capas del backend: salud, servicio de IA, contrato de la API pública, validación de entradas, autenticación, chatbot y observabilidad. El workflow de GitHub Actions instala dependencias, revisa el código con Ruff y ejecuta las pruebas en cada `push` y pull request hacia `main`.

### Ejecutar las pruebas localmente

```bash
cd backend
pip install -r requirements-dev.txt
pytest -v
```

Revisar calidad de código:

```bash
ruff check .
```

### Qué se simula y por qué

Las pruebas no dependen de Supabase real, del modelo `rf_model.pkl` ni de la API de Gemini — se usa SQLite temporal, un modelo simulado y `FakeListChatModel` de LangChain. El detalle completo está en [docs/registro-errores-semana-3.md](docs/registro-errores-semana-3.md), sección 3.

### Comportamiento del flujo CI/CD

1. GitHub Actions descarga el repositorio.
2. Configura Python 3.11 e instala las dependencias.
3. Ejecuta Ruff y las pruebas automatizadas con pytest.
4. Guarda un reporte JUnit como artefacto.
5. Solo cuando el evento es un `push` a `main` y el job de pruebas termina correctamente, activa el Deploy Hook de Render.
6. Render reconstruye y despliega la imagen Docker.

Si Ruff o pytest fallan, el job de despliegue no se ejecuta y la nueva versión no se publica en Render.

### Documentación relacionada

- [`docs/pruebas.md`](docs/pruebas.md) — qué verifica cada archivo de pruebas
- [`docs/registro-errores-semana-3.md`](docs/registro-errores-semana-3.md) — errores encontrados, correcciones aplicadas y evidencia de ejecución
- [`.github/workflows/ci.yml`](.github/workflows/ci.yml) — definición del pipeline

---

## Despliegue en producción - Semana 4

El backend se contenerizó con Docker (construcción multietapa, usuario sin privilegios) y se desplegó públicamente en Render. El pipeline de CI de Semana 3 se extendió a CI/CD: cada push a `main` corre la suite completa de pruebas y, solo si pasan, dispara automáticamente el despliegue en Render mediante un Deploy Hook.

**Ruta elegida:** Docker (contenedor único para el backend), en la plataforma PaaS Render.

**URL pública del backend:** https://gamevisionia.onrender.com

```bash
curl https://gamevisionia.onrender.com/health
curl -X POST https://gamevisionia.onrender.com/api/predict-demo \
  -H "Content-Type: application/json" \
  -d '{"price_initial": 14.99, "is_free": 0, "release_year": 2025, "release_month": 3, ...}'
```

**Flujo de CI/CD:**

```text
git push a main → GitHub Actions corre las pruebas → ¿pasan?
    → SÍ → dispara Deploy Hook de Render → build de Docker → despliegue automático
    → NO → nunca llega a Render, nada se despliega roto
```

---

## Observabilidad, rendimiento y escalabilidad - Semana 5

Se incorporó observabilidad mínima real al proyecto (no un ejemplo aparte), se midió el rendimiento del flujo crítico de producción, y se aplicó una mejora con evidencia de comparación antes/después.

**Instrumentación:**

- Middleware global en `main.py` que corre para toda la API — genera `request_id`, mide `duration_ms`, agrega headers `X-Request-ID` / `X-Process-Time-Ms`, y persiste cada petición en la tabla `request_logs` de Supabase como `BackgroundTask` (después de responder, para no afectar la latencia medida).
- Desglose interno de tiempos (`validate_ms`, `feature_prep_ms`, `inference_ms`) dentro de `run_prediction()`, correlacionado con el mismo `request_id` del middleware.
- Retención automática: job `pg_cron` que borra logs con más de 30 días — ver [backend/scripts/setup_retention.sql](backend/scripts/setup_retention.sql).
- Ningún log guarda tokens, contraseñas, encabezados de autorización, cadenas de conexión ni contenido de mensajes del chat — solo metadatos técnicos.

**Línea base de rendimiento** (20 peticiones secuenciales por escenario, ambiente de producción):

| Escenario | p50 | p95 | máx | error |
|---|---|---|---|---|
| `/predict-demo` (sin auth) | 817-1021 ms | 969-1195 ms | 1064-1295 ms | 0% |
| `/predict` real (autenticado) | 1239-1431 ms | 1446-1784 ms | 1873-2335 ms | 0% |
| `/chat` (muestra de 3) | avg 6280-12436 ms | — | 12900-30761 ms | 0-1 timeout |

**Diagnóstico:** el modelo Random Forest representa solo 3-13% del tiempo total de una predicción real (39-46 ms medidos internamente); el resto es autenticación JWT y escrituras en Supabase. Se identificó además un cold-start real de ~53.5 segundos tras inactividad, y una llamada al chat que tardó 177 segundos sin que exista timeout explícito hacia Gemini.

**Mejora aplicada:** se redujeron los viajes de red a Supabase en `/api/predict` de 4 (dos ciclos de `commit()`+`refresh()`) a 2-3 (`flush()` + un solo `commit()` final), midiendo -58.6% en el overhead de autenticación + base de datos (781 ms → 353 ms de `duration_ms` promedio, medido del lado del servidor).

**Documentación completa:** ver el informe de evidencias de Semana 5 en `docs/` (capturas, código, línea base completa y plan de escalabilidad).

---

## Seguridad, versionamiento y defensa final - Semana 6

Se revisó el proyecto real en busca de riesgos de seguridad, se corrigieron los más prioritarios con evidencia verificable, y se publicó un release identificable y trazable, siguiendo la lógica de "convertir el proyecto en un release trazable y defendible".

**Riesgos identificados y controles aplicados:**

| Riesgo | Estado | Evidencia |
|---|---|---|
| IDOR — acceso a sesiones de chat de otros usuarios (`session_id` consecutivo y adivinable, sin verificar dueño) | Corregido | `test_chat_rechaza_sesion_de_otro_usuario` (pytest) + prueba manual en producción: acceso cruzado entre cuentas → 404, acceso propio → 200 |
| OAuth de Google en modo Testing (bloqueaba cuentas no aprobadas) | Corregido | App publicada a producción en Google Cloud Console |
| Row Level Security desactivado en 4 tablas públicas de Supabase | Corregido | Security Advisor sin errores CRITICAL tras `enable_rls.sql` |
| Sin timeout en la llamada a Gemini (evidencia real: 177s sin control, Semana 5) | Corregido | Timeout de 20s vía `ThreadPoolExecutor`; responde 504 controlado |
| Mensajes de error exponían detalles internos de excepciones | Corregido | `routers/predict.py`: detalle real solo en logs, respuesta genérica al cliente |
| Sin rate limiting en `/predict` ni `/chat` | Declarado, no corregido | Decisión consciente: cambio de mayor riesgo/esfuerzo tan cerca de la defensa final |

**Versionamiento:** primer release formal del proyecto, siguiendo Semantic Versioning — `v1.0.0-rc.1`, publicado como pre-release en GitHub. El manifiesto [`release-manifest.yml`](release-manifest.yml) documenta el commit exacto, la versión del modelo, del componente conversacional, y el estado de las pruebas para ese release.

**Rollback:** confirmado disponible vía el botón "Rollback" del historial de deploys de Render (Dashboard → servicio → Events), con un procedimiento alternativo vía `git checkout` documentado en [`docs/final/plan-contingencia-demo.md`](docs/final/plan-contingencia-demo.md) por si el primero no está disponible para un commit específico.

**Plan de contingencia de la demostración:** riesgos, prevención y respuesta preparada para la defensa en vivo — ver [`docs/final/plan-contingencia-demo.md`](docs/final/plan-contingencia-demo.md).

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
- Las tablas de Supabase tienen Row Level Security (RLS) activado desde Semana 6. El backend se conecta con un rol que, por diseño de Postgres, no queda sujeto a RLS (ignora las políticas al ser el dueño de las tablas); RLS bloquea específicamente el acceso público no autorizado vía la API REST de Supabase
---

## 12. Riesgos Técnicos y Deuda Técnica

Ver documento completo: [docs/riesgos-tecnicos.md](docs/riesgos-tecnicos.md)

| Riesgo | Categoría | Probabilidad | Impacto | Mitigación propuesta |
|---|---|---|---|---|
| ~~`rf_model.pkl` de 63MB no está en el repo~~ | Datos | — | — | ✅ Resuelto en Semana 4 — publicado en GitHub Release, el Dockerfile lo descarga con `curl` |
| Chatbot depende de API externa de Gemini | Modelo | Media | Alto | Manejo de error graceful que informe al usuario si el servicio falla |
| Caché de mensajes en RAM (`sessions_memory`) no escala a múltiples workers | Código | Baja | Bajo | El historial real ya persiste en `chat_messages` (la caché en RAM solo evita relecturas); revisar si se agrega Redis al escalar a más de 1 worker |
| Configuración incorrecta de URLs en producción | Configuración | Media | Alto | Verificar que `VITE_API_URL` y `ALLOWED_ORIGINS` estén correctamente definidos en el entorno de despliegue |
| ~~Conexión directa a Supabase puede fallar por IPv6~~ | Configuración | — | — | ✅ Resuelto en Semana 4 — Session Pooler de Supabase (IPv4) + `sslmode=require` |
| ~~Sin tests automatizados~~ | Código | — | — | ✅ Resuelto en Semana 3 — ver [docs/pruebas.md](docs/pruebas.md) |
| ~~RLS desactivado en Supabase~~ | Seguridad | — | — | ✅ Resuelto en Semana 6 — activado en las 4 tablas públicas |
| La instancia gratuita de Render puede suspenderse por inactividad | Despliegue | Alta | Bajo | Confirmado con evidencia real en Semana 5: cold-start medido de 53.5s tras inactividad. Aceptado para el entorno académico; se evaluará monitoreo externo o un plan de pago |
| ~~Sin timeout explícito en la llamada a Gemini (LangChain)~~ | Código | — | — | ✅ Resuelto en Semana 6 — timeout de 20s, responde 504 controlado |
| ~~IDOR en sesiones de chat (session_id adivinable sin verificar dueño)~~ | Seguridad | — | — | ✅ Resuelto en Semana 6 — verificación de dueño en `POST /api/chat` y `GET /api/chat/{id}/messages`, probado en producción |
| ~~Mensajes de error exponían detalles internos de excepciones~~ | Seguridad | — | — | ✅ Resuelto en Semana 6 — detalle real solo en logs del servidor |
| ~~OAuth de Google en modo Testing~~ | Seguridad | — | — | ✅ Resuelto en Semana 6 — app publicada a producción |
| Sin rate limiting en `/predict` ni `/chat` | Seguridad | Media | Medio | **Declarado, no corregido** — decisión consciente por proximidad a la defensa final; agotamiento de cuota o abuso del endpoint quedan sin control automático |
| Conexión a BD directa al puerto de Postgres, no vía API REST | Seguridad | Baja | Medio | Patrón oficialmente recomendado por Supabase para servidores de larga duración; credenciales solo en variables de entorno del servidor. Pendiente: Network Restrictions de Supabase |
| Un solo contenedor Docker, sin redundancia | Arquitectura | Baja | Medio | Aceptado como apropiado para el tamaño actual del proyecto; reevaluar solo si el tráfico real lo justifica |

---

## 13. Plan de Mejora por Semana

| Semana | Mejora esperada | Evidencia esperada |
|---|---|---|
| Semana 2 | ✅ Endpoints /health, /metadata y /predict-demo implementados. Validaciones Pydantic, manejo de errores, capa de servicios separada, CORS con variable de entorno | Swagger funcional, evidencia con curl en CMD, docs/api.md completo |
| Semana 3 | ✅ 15 tests automatizados (unitarios, contrato, validación, autenticación, chatbot) con pytest, pipeline de CI en GitHub Actions, calidad de código con Ruff (41→0 hallazgos). Políticas RLS: **pendiente** | Resultados de tests en GitHub Actions (`docs/evidencias/semana3-*.png`), registro de errores en [docs/registro-errores-semana-3.md](docs/registro-errores-semana-3.md) |
| Semana 4 | ✅ Dockerfile para el backend, modelo en GitHub Releases, backend desplegado en Render, pipeline CI/CD completo (despliegue automático vía Deploy Hook). Frontend en Vercel y UptimeRobot: **pendientes** | Backend público funcional (`docs/evidencias/semana4-*.png`), registro de errores en [docs/registro-errores-semana-4.md](docs/registro-errores-semana-4.md) |
| Semana 5 | ✅ Middleware de observabilidad global, tabla `request_logs` con retención automática (`pg_cron`), línea base de rendimiento con comparación antes/después, mejora aplicada (-58.6% overhead en `/predict`). Timeout explícito en Gemini: **pendiente** | Este README, informe de evidencias en `docs/`, `backend/scripts/benchmark_predict.py` y `backend/scripts/setup_retention.sql` |
| Semana 6 | ✅ IDOR corregido en chat, OAuth publicado a producción, RLS activado, timeout en Gemini, mensajes de error sin exponer detalles internos, tag/release `v1.0.0-rc.1` con manifiesto. Rate limiting: **declarado, no corregido**. Informe final y presentación: **en construcción** | Este README, `release-manifest.yml`, `docs/final/plan-contingencia-demo.md`, test adversarial `test_chat_rechaza_sesion_de_otro_usuario`, [release en GitHub](https://github.com/sauzuniga/GameVisionIA/releases/tag/v1.0.0-rc.1) |

---

## 14. Limitaciones Actuales

- El modelo fue entrenado con datos históricos de Steam hasta una fecha específica; no refleja tendencias recientes del mercado
- El F1-score de ~47% indica dificultad para identificar correctamente juegos exitosos debido al desbalance natural del dataset
- El chatbot depende de la API externa de Gemini; sin conexión a internet o sin cuota disponible no funciona
- La caché conversacional en memoria se pierde si el servidor se reinicia, aunque el historial persistente permanece almacenado en Supabase
- El archivo `rf_model.pkl` de 63MB no puede incluirse en el repositorio por su tamaño (se resuelve descargándolo desde GitHub Releases)
- La instancia gratuita de Render puede suspenderse por inactividad y provocar un arranque inicial lento (medido: ~53.5 segundos en Semana 5)
- Las mediciones de rendimiento de Semana 5 fueron secuenciales (20 peticiones una tras otra); no se probó el comportamiento bajo múltiples usuarios concurrentes
- Sin rate limiting en `/predict` ni `/chat` — decisión consciente, no implementada por proximidad a la defensa final
- El prompt del chatbot no tiene versionado formal
- El rollback está confirmado como disponible (Render) pero pendiente de un ensayo real antes de la defensa
- El proyecto localmente requiere abrir dos terminales (o usar Docker para el backend) y configurar manualmente los archivos `.env`

---

## 15. Evidencias

| Evidencia | Enlace o ubicación | Descripción |
|---|---|---|
| Landing page | [Ver captura](docs/evidencias/LandingPage.png) | Pantalla principal de GameVision IA |
| Login con Google | [Ver captura](docs/evidencias/LoginGoogle.png) | Autenticación con Google OAuth mediante Supabase Auth |
| Formulario y resultado de predicción | [Ver captura](docs/evidencias/formulario-resultado-prediccion.png) | Entrada de datos del videojuego y resultado generado por el modelo |
| Chatbot | [Ver captura](docs/evidencias/Chatbot.png) | Asistente conversacional interpretando el resultado |
| Historial almacenado | [Ver captura](docs/evidencias/HistorialAlmacenado.jpeg) | Recuperación de predicciones o conversaciones previas |
| Tabla `predictions` en Supabase | [Ver captura](docs/evidencias/supabasepredictions.jpeg) | Predicciones almacenadas con `user_id`, probabilidad y nivel de potencial |
| Tabla `chat_sessions` en Supabase | [Ver captura](docs/evidencias/supabase_chat_sessions.jpeg) | Sesiones de conversación almacenadas en la base de datos |
| Ruff sin errores | [Ver captura](docs/evidencias/pruebaRuff.png) | `ruff check .` → `All checks passed!` tras corregir 41 hallazgos |
| Pruebas locales | [Ver captura](docs/evidencias/pytestlocal.png) | `pytest -v` → 15 pruebas pasando en entorno local |
| Pipeline en GitHub Actions | [Ver captura](docs/evidencias/pipeline.png) | Vista resumen del workflow en verde (Success) |
| Log detallado del pipeline | [Ver captura](docs/evidencias/workflows.png) | Las 15 pruebas ejecutándose una por una dentro de GitHub Actions |
| Informe de Semana 4 | [Ver PDF](docs/Semana4_Despliegue_Infraestructura_GameVisionIA.pdf) | Evidencias de contenedor, despliegue, endpoints, infraestructura, costos y riesgos |
| Informe de Semana 5 | [Ver PDF](docs/GameVisionIA_Semana5_Evidencias.pdf) | Instrumentación, línea base de rendimiento, diagnóstico, mejora antes/después y plan de escalabilidad |
| Línea base de rendimiento (JSON) | [Ver archivo](docs/evidencias/linea_base_rendimiento.json) | Resultado estructurado del benchmark: ambiente, payload, commit y métricas p50/p95/máx/error |
| Manifiesto de release | [Ver archivo](release-manifest.yml) | Commit, versión del modelo y del componente conversacional, estado de pruebas, riesgos y controles del release `v1.0.0-rc.1` |
| Release en GitHub | [Ver release](https://github.com/sauzuniga/GameVisionIA/releases/tag/v1.0.0-rc.1) | Tag `v1.0.0-rc.1`, notas de la versión, pre-release |
| Plan de contingencia de la demo | [Ver archivo](docs/final/plan-contingencia-demo.md) | Riesgos, prevención y respuesta preparada para la defensa en vivo |
| Informe final integrador | [Ver documento](docs/final/informe-final.md) | Síntesis de las seis sesiones del Módulo 4 |
| Presentación final | [Ver PDF](docs/final/presentacion-final.pdf) | Presentación de 7 minutos para la defensa técnica |
| Capturas de seguridad de Semana 6 (OAuth, Security Advisor, IDOR) | [Ver carpeta](docs/final/respaldo/) | Evidencia visual de los controles de seguridad aplicados |

---

## 16. Créditos y Referencias

- [scikit-learn](https://scikit-learn.org/) — Random Forest y pipeline de ML
- [FastAPI](https://fastapi.tiangolo.com/) — Framework del backend
- [LangChain](https://python.langchain.com/) — Orquestación del chatbot con memoria de conversación
- [Google Gemini 2.5 Flash](https://ai.google.dev/) — Modelo LLM para el asistente conversacional
- [Supabase](https://supabase.com/) — Autenticación con Google OAuth y base de datos Postgres
- [React](https://react.dev/) + [Vite](https://vitejs.dev/) — Framework del frontend
- [Dataset público de videojuegos de Steam](https://drive.google.com/file/d/1gBKymTt2OR5NVLVYlTuYrTRESsLgghRZ/view?usp=sharing)
---

