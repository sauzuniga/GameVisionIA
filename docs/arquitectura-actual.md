# Arquitectura Actual
**Proyecto:** GameVision IA  
**Semana:** 1

---

## Componentes actuales

| Componente | Tecnología | Responsabilidad | Estado |
|---|---|---|---|
| Interfaz | React 18 + Vite | Landing, formulario, resultado, chat, historial | Funcional |
| API / Backend | FastAPI (Python 3.11) | Expone endpoints REST, verifica JWT, orquesta IA | Funcional |
| Servicio IA — Predicción | Random Forest (scikit-learn) | Estima probabilidad de éxito con 22 features | Funcional |
| Servicio IA — Chat | Gemini 2.5 Flash + LangChain | Interpreta resultado y responde preguntas | Funcional |
| Datos | Supabase Postgres | Almacena predicciones, sesiones y mensajes por usuario | Funcional |
| Autenticación | Supabase Auth + Google OAuth | Login con Google, emisión y verificación de JWT ES256 | Funcional |
| Operación | .env + requirements.txt + package.json | Configuración de credenciales y dependencias | Manual |

---

## Diagrama de arquitectura actual

```mermaid
flowchart TD
    U([Usuario]) --> I

    subgraph Interfaz
        I[React + Vite\nLanding / Formulario / Resultado / Chat / Historial]
    end

    subgraph Autenticación
        SA[Supabase Auth]
        GO[Google OAuth 2.0]
    end

    I -- Login --> SA
    SA -- OAuth --> GO
    GO -- Token --> SA
    SA -- JWT ES256 --> I

    subgraph API_Backend [API / Backend - FastAPI]
        EP1[POST /api/predict]
        EP2[POST /api/chat]
        EP3[GET /api/history]
        JWT_V[Verificación JWT\nPyJWKClient ES256]
    end

    I -- Request + Bearer JWT --> JWT_V
    JWT_V --> EP1
    JWT_V --> EP2
    JWT_V --> EP3

    subgraph Servicio_IA [Servicio IA]
        RF[Random Forest\nrf_model.pkl\n22 features · 200 árboles]
        GEM[Gemini 2.5 Flash\nvía LangChain\nSystem prompt + guardrails]
    end

    EP1 --> RF
    EP2 --> GEM

    subgraph Datos
        DB[(Supabase Postgres\npredictions\nchat_sessions\nchat_messages)]
    end

    EP1 -- Guarda predicción + user_id --> DB
    EP2 -- Guarda mensajes --> DB
    EP3 -- Consulta por user_id --> DB

    RF -- Probabilidad + nivel --> EP1
    GEM -- Respuesta conversacional --> EP2
```

---

## Flujo básico de información

1. El usuario entra al landing y hace clic en "Analizar mi juego"
2. Supabase Auth redirige a Google OAuth; el usuario se autentica
3. Supabase emite un JWT (ES256) y lo entrega al frontend
4. El frontend llama a `POST /api/predict` con el JWT en el header `Authorization`
5. FastAPI verifica el JWT con PyJWKClient y extrae el `user_id`
6. El modelo Random Forest recibe las 22 features y devuelve una probabilidad
7. La predicción se guarda en Supabase Postgres con el `user_id` del usuario
8. El usuario puede chatear con Gemini 2.5 Flash, que interpreta el resultado
9. Los mensajes se guardan en `chat_messages` vinculados a la sesión

---

## Dependencias manuales y puntos frágiles

- `rf_model.pkl` debe copiarse manualmente a `backend/` (no está en el repo)
- La memoria de conversación del chatbot vive en RAM del servidor (`sessions_memory = {}`)
- El acceso OAuth está limitado a cuentas aprobadas manualmente (modo Testing)
- No existe ningún test automatizado
- No existe Docker ni script de despliegue
- El frontend y backend usan variables de entorno para configurar las URLs (`VITE_API_URL` en frontend y `ALLOWED_ORIGINS` en backend), manteniendo valores locales por defecto para desarrollo.
- Las tablas de Supabase requieren revisión de Row Level Security (RLS) y políticas por `user_id` antes de considerarse seguras para producción.
