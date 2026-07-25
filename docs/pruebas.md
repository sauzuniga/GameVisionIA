# Pruebas automatizadas — GameVision IA Backend

Este documento explica qué verifica cada archivo dentro de `backend/tests/`
y por qué existe. En total hay **15 pruebas** repartidas en **6 capas**
distintas del backend.

## Mapa de capas

```
Petición HTTP
    |
Validación (schemas.py)          -> test_validation.py
    |
Autenticación (auth.py)          -> test_predict_auth.py
    |
Router (routers/predict.py, routers/chat.py)
                                  -> test_predict_demo.py, test_predict_auth.py, test_chat.py
    |
Servicio IA (services/predict_service.py)
                                  -> test_predict_service.py
    |
Base de datos (models.py)        -> test_predict_auth.py, test_chat.py (al guardar)
```

## Detalle por archivo

### `test_health.py` (2 pruebas)

Verifica que la API "está viva" y que el endpoint de metadatos describe
correctamente el modelo cargado.

- `test_health_responde_ok` — `/health` responde 200 con una llave `status`.
- `test_metadata_incluye_info_del_modelo` — `/metadata` responde 200 e
  incluye la lista de endpoints disponibles.

### `test_predict_service.py` (4 pruebas)

Prueba la lógica de negocio del servicio de IA **de forma aislada**, sin
pasar por la API ni por HTTP — llamando directamente a las funciones de
Python.

- `test_potencial_alto_con_probabilidad_alta` / `..._medio_...` /
  `..._bajo_...` — confirman que `get_potential_level()` clasifica
  correctamente en los tres rangos (Alto ≥ 0.75, Medio ≥ 0.60, Bajo el resto).
- `test_run_prediction_retorna_estructura_valida` — confirma que
  `run_prediction()` arma un diccionario con todas las llaves esperadas
  (`result`, `confidence`, `model_version`, `request_id`, etc.), usando un
  modelo simulado que siempre regresa la misma probabilidad.

### `test_predict_demo.py` (2 pruebas)

Prueba el endpoint público `/api/predict-demo`, el único que no requiere
autenticación.

- `test_predict_demo_responde_sin_token` — confirma que responde 200 sin
  necesidad de header de autorización.
- `test_predict_demo_devuelve_contrato_esperado` — confirma que la
  respuesta trae exactamente los campos que promete `DemoPredictionResponse`.

### `test_validation.py` (3 pruebas)

Prueba que la API **rechaza** datos mal formados en vez de aceptarlos
silenciosamente, usando los validadores definidos en `schemas.py`.

- `test_rechaza_precio_negativo` — un precio negativo produce 422.
- `test_rechaza_anio_fuera_de_rango` — un año fuera de 2000-2035 produce 422.
- `test_rechaza_sin_ningun_genero_seleccionado` — no marcar ningún género
  produce 422.

### `test_predict_auth.py` (2 pruebas)

Prueba el endpoint protegido `/api/predict`, el que sí exige token y sí
guarda en base de datos.

- `test_predict_rechaza_sin_token` — sin header de autorización, responde
  401/403.
- `test_predict_funciona_con_token_simulado` — con un usuario simulado
  (vía `app.dependency_overrides`, sin generar un JWT real ni llamar a
  Supabase), la predicción se ejecuta y se guarda correctamente.

### `test_chat.py` (2 pruebas)

Prueba el flujo del chatbot, simulando el modelo de lenguaje (Gemini) con
`FakeListChatModel` de LangChain para no depender de una llamada real.

- `test_chat_rechaza_sesion_inexistente` — mandar un mensaje a un
  `session_id` que no existe responde 404.
- `test_chat_responde_y_guarda_mensajes` — prueba de integración completa:
  crea una predicción real (vía `/api/predict`) para obtener una sesión
  válida, manda un mensaje, y confirma que tanto el mensaje del usuario
  como la respuesta simulada de la IA quedaron guardados en la base de
  datos de prueba.

## Por qué se simulan el modelo, la base de datos y el LLM

Ver `docs/registro-errores-semana-3.md`, sección 3, para el detalle completo
de esta decisión de diseño.

## Cómo ejecutar las pruebas

```bash
cd backend
pip install -r requirements-dev.txt
pytest -v
```
