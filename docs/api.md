# API Reference — GameVision IA
**Versión:** 1.0.0  
**Base URL local:** `http://localhost:8000`  
**Swagger UI:** `http://localhost:8000/docs`  
**Herramienta usada para probar:** Swagger UI y curl desde CMD

---

## Autenticación

Los endpoints `/predict`, `/chat` e `/history` requieren un JWT emitido por Supabase Auth tras iniciar sesión con Google.

```
Authorization: Bearer <token>
```

Para obtener el token en desarrollo:
1. Iniciá sesión en `http://localhost:5173`
2. Abrí DevTools (F12) → Application → Local Storage
3. Buscá la clave que empieza con `sb-` y copiá el valor de `access_token`
4. En Swagger UI hacé click en **Authorize** y pegá `Bearer <token>`

Los endpoints `/health`, `/metadata` y `/predict-demo` son **públicos** — no requieren token.

---

## Endpoints públicos

### GET /health
Verifica que el servicio está activo, el modelo está cargado y la base de datos responde.

**Método:** GET  
**Ruta:** `/health`  
**Autenticación:** No requerida

**Herramienta de prueba:**
```bash
curl -X GET "http://localhost:8000/health" -H "accept: application/json"
```

**Respuesta exitosa (200):**
```json
{
  "status": "ok",
  "timestamp": "2026-07-16T22:53:58.750308",
  "model": "loaded",
  "database": "connected"
}
```

**Respuesta degradada (200):**
```json
{
  "status": "degraded",
  "timestamp": "2026-07-16T22:53:58.750308",
  "model": "not loaded",
  "database": "connected"
}
```

---

### GET /metadata
Información del modelo de IA, métricas de evaluación y descripción de todos los endpoints disponibles.

**Método:** GET  
**Ruta:** `/metadata`  
**Autenticación:** No requerida

**Herramienta de prueba:**
```bash
curl -X GET "http://localhost:8000/metadata" -H "accept: application/json"
```

**Respuesta exitosa (200):**
```json
{
  "name": "GameVision IA",
  "version": "1.0.0",
  "description": "Predictor de potencial comercial de videojuegos en Steam",
  "model": {
    "type": "Random Forest Classifier",
    "algorithm": "RandomForestClassifier",
    "n_estimators": 200,
    "threshold": 0.6,
    "training_samples": 58000,
    "metrics": {
      "accuracy": 0.8416,
      "f1_score": 0.4747
    }
  },
  "endpoints": {
    "predict": "POST /api/predict — requiere JWT",
    "predict_demo": "POST /api/predict-demo — público, sin JWT",
    "chat": "POST /api/chat — requiere JWT",
    "history": "GET /api/history — requiere JWT",
    "health": "GET /health — público",
    "metadata": "GET /metadata — público",
    "docs": "GET /docs — Swagger UI"
  },
  "input_features": 22,
  "output": {
    "result": "Alto / Medio / Bajo",
    "confidence": "probabilidad entre 0.0 y 1.0",
    "predicted_class": "0 = No exitoso, 1 = Exitoso",
    "model_version": "versión del modelo",
    "warnings": "advertencias si aplica",
    "request_id": "identificador único del request"
  }
}
```

---

### POST /api/predict-demo
Endpoint público de demostración. Usa el modelo Random Forest real pero no requiere autenticación y no guarda historial en la base de datos. Diseñado para pruebas y evaluación externa.

**Método:** POST  
**Ruta:** `/api/predict-demo`  
**Autenticación:** No requerida

**Payload de entrada:**
```json
{
  "price_initial": 9.99,
  "is_free": 0,
  "release_year": 2025,
  "release_month": 3,
  "genre_Indie": 1,
  "genre_Casual": 0,
  "genre_Action": 1,
  "genre_Adventure": 0,
  "genre_Simulation": 0,
  "genre_Strategy": 0,
  "genre_RPG": 0,
  "genre_Early_Access": 0,
  "genre_Free_To_Play": 0,
  "cat_Single_player": 1,
  "cat_Multi_player": 0,
  "cat_PvP": 0,
  "cat_Co_op": 0,
  "cat_Online_PvP": 0,
  "cat_Online_Co_op": 0,
  "cat_Shared_Split_Screen": 0,
  "cat_Shared_Split_Screen_PvP": 0,
  "cat_Shared_Split_Screen_Co_op": 0
}
```

**Validaciones aplicadas:**
| Campo | Regla |
|---|---|
| `price_initial` | Debe ser >= 0 |
| `release_year` | Debe estar entre 2000 y 2035 |
| `release_month` | Debe estar entre 1 y 12 |
| `is_free` y campos de género/categoría | Deben ser 0 o 1 |
| Géneros | Al menos uno debe ser 1 |

**Respuesta exitosa (200):**
```json
{
  "result": "Bajo",
  "confidence": 0.4066,
  "predicted_class": 0,
  "potential_level": "Bajo",
  "model_version": "v1.0.0",
  "warnings": [],
  "request_id": "885a0bf6",
  "demo": true,
  "note": "Endpoint de demostración. No requiere autenticación y no guarda historial."
}
```

**Descripción de campos de respuesta:**
| Campo | Descripción |
|---|---|
| `result` | Nivel de potencial: Alto, Medio o Bajo |
| `confidence` | Probabilidad de éxito entre 0.0 y 1.0 |
| `predicted_class` | 0 = No exitoso, 1 = Exitoso (umbral: 0.60) |
| `potential_level` | Igual que result |
| `model_version` | Versión del modelo usado |
| `warnings` | Advertencias si la predicción está cerca del umbral |
| `request_id` | Identificador único del request para trazabilidad |
| `demo` | Siempre true en este endpoint |
| `note` | Aclaración sobre el endpoint de demostración |

**Errores posibles:**

| Código | Causa | Ejemplo |
|---|---|---|
| 422 | Datos de entrada inválidos | Precio negativo, año fuera de rango, sin géneros |
| 503 | Modelo no disponible | El archivo rf_model.pkl no está cargado |
| 500 | Error interno del servidor | Error inesperado en la inferencia |

**Evidencia de error 422 — precio negativo:**
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "price_initial"],
      "msg": "Value error, El precio no puede ser negativo",
      "input": -5,
      "ctx": {"error": {}}
    }
  ]
}
```

**Herramienta de prueba — curl:**
```bash
curl -X POST "http://localhost:8000/api/predict-demo" ^
  -H "Content-Type: application/json" ^
  -d "{\"price_initial\":9.99,\"is_free\":0,\"release_year\":2025,\"release_month\":3,\"genre_Indie\":1,\"genre_Casual\":0,\"genre_Action\":1,\"genre_Adventure\":0,\"genre_Simulation\":0,\"genre_Strategy\":0,\"genre_RPG\":0,\"genre_Early_Access\":0,\"genre_Free_To_Play\":0,\"cat_Single_player\":1,\"cat_Multi_player\":0,\"cat_PvP\":0,\"cat_Co_op\":0,\"cat_Online_PvP\":0,\"cat_Online_Co_op\":0,\"cat_Shared_Split_Screen\":0,\"cat_Shared_Split_Screen_PvP\":0,\"cat_Shared_Split_Screen_Co_op\":0}"
```

---

## Endpoints protegidos (requieren JWT)

### POST /api/predict
Endpoint principal de IA. Usa el mismo modelo Random Forest, requiere autenticación y guarda el historial en Supabase vinculado al usuario.

**Método:** POST  
**Ruta:** `/api/predict`  
**Autenticación:** Bearer JWT requerido

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Payload de entrada:** mismo formato que `/api/predict-demo`

**Respuesta exitosa (200):**
```json
{
  "id": 42,
  "result": "Medio",
  "confidence": 0.6834,
  "probability": 0.6834,
  "predicted_class": 1,
  "potential_level": "Medio",
  "model_version": "v1.0.0",
  "warnings": [],
  "request_id": "a1b2c3d4",
  "session_id": 38,
  "created_at": "2026-07-16T10:00:00.000000"
}
```

**Errores posibles:**

| Código | Causa |
|---|---|
| 401 | Token JWT ausente, expirado o inválido |
| 422 | Datos de entrada inválidos |
| 503 | Modelo no disponible |
| 500 | Error del modelo o de la base de datos |

---

### POST /api/chat
Envía un mensaje al asistente conversacional GameVision Assistant (Gemini 2.5 Flash vía LangChain).

**Método:** POST  
**Ruta:** `/api/chat`  
**Autenticación:** Bearer JWT requerido

**Payload de entrada:**
```json
{
  "session_id": 38,
  "message": "¿Por qué el potencial es Bajo?",
  "prediction_context": "El juego tiene una probabilidad de éxito del 40.6%, con potencial Bajo."
}
```

**Respuesta exitosa (200):**
```json
{
  "role": "assistant",
  "content": "El potencial es Bajo principalmente porque...",
  "created_at": "2026-07-16T10:01:00.000000"
}
```

---

### GET /api/history
Devuelve el historial completo de predicciones del usuario autenticado.

**Método:** GET  
**Ruta:** `/api/history`  
**Autenticación:** Bearer JWT requerido

**Respuesta exitosa (200):** lista de predicciones del usuario con todos sus campos.

---

### GET /api/history/{prediction_id}
Devuelve el detalle de una predicción específica del usuario autenticado.

**Método:** GET  
**Ruta:** `/api/history/{prediction_id}`  
**Autenticación:** Bearer JWT requerido

**Error si no pertenece al usuario (200):**
```json
{
  "error": "Predicción no encontrada"
}
```

---

## Resumen de endpoints

| Método | Ruta | Descripción | Autenticación |
|---|---|---|---|
| GET | /health | Estado del servicio y modelo | Pública |
| GET | /metadata | Info del modelo y endpoints | Pública |
| POST | /api/predict-demo | Predicción sin guardar historial | Pública |
| POST | /api/predict | Predicción con historial | JWT requerido |
| POST | /api/chat | Asistente conversacional | JWT requerido |
| GET | /api/history | Historial del usuario | JWT requerido |
| GET | /api/history/{id} | Detalle de predicción | JWT requerido |
| GET | /docs | Swagger UI | Pública |
