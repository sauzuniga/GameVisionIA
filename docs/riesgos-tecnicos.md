# Riesgos Técnicos y Deuda Técnica
**Proyecto:** GameVision IA  
**Semana:** 1

---

## Tabla de riesgos

| # | Categoría | Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|---|---|
| 1 | Datos | El archivo `rf_model.pkl` (63 MB) no está en el repositorio; si se pierde el enlace de Drive el modelo no está disponible | Media | Alto | Publicar el modelo como asset en un GitHub Release (límite 2GB); el Dockerfile lo descarga con `wget` al construir la imagen |
| 2 | Modelo | El chatbot depende de la API de Gemini; si hay corte del servicio o se agota la cuota, el chat falla completamente | Media | Alto | Implementar manejo de error graceful que informe al usuario; explorar alternativa con modelo local (Ollama) |
| 3 | Modelo | La memoria de conversación (`sessions_memory = {}`) vive en RAM del servidor; cualquier reinicio la borra | Alta | Medio | Persistir el historial de mensajes en la base de datos (ya existe la tabla `chat_messages`) |
| 4 | Código | No existen tests automatizados; un cambio puede romper el flujo de predicción sin que nadie lo detecte | Alta | Medio | Escribir tests unitarios básicos en Semana 3 |
| 5 | Dependencias | scikit-learn y las dependencias de LangChain son pesadas; el contenedor Docker puede tardar mucho en construirse | Media | Medio | Usar imagen base optimizada; fijar versiones en `requirements.txt` |
| 6 | Configuración | Son necesarias 5 variables de entorno de 3 servicios distintos; un error en cualquiera impide arrancar | Alta | Alto | Documentar claramente en `.env.example`; agregar validación al inicio del servidor |
| 7 | Seguridad | Las tablas en Supabase no tienen Row Level Security (RLS) activado; usuarios podrían acceder a datos que no les corresponden | Media | Alto | Activar RLS entre Semana 2 y 3 con políticas por `user_id`; auditar seguridad en Semana 6 |
| 8 | Seguridad | El OAuth de Google está en modo "Testing"; solo cuentas aprobadas manualmente pueden entrar | Alta | Medio | Publicar la app OAuth antes de la demo final (Semana 6) |
| 9 | Despliegue | El `rf_model.pkl` de 63 MB supera el límite de 50 MB de Supabase Storage (tier gratuito) y no puede incluirse en el repo | Alta | Alto | Usar GitHub Releases para alojar el modelo (gratuito, hasta 2GB por archivo); el Dockerfile lo descarga automáticamente con `wget` |
| 10 | Equipo | Actualmente solo un integrante comprende la arquitectura completa y puede ejecutar el proyecto | Media | Alto | Documentar instalación y ejecución; compartir variables de entorno por canal seguro o agregar integrantes a Supabase con permisos controlados |
| 11 | Código | Las URLs `localhost:8000` en `api.js` y `localhost:5173` en el CORS de `main.py` están hardcodeadas; en producción el proyecto no funcionará | Alta | Alto | Mover ambas a variables de entorno (`VITE_API_URL` y `ALLOWED_ORIGINS`) en Semana 2 |
| 12 | Configuración | La conexión directa a Supabase (`db.xxx.supabase.co:5432`) resuelve a IPv6 en algunas redes y puede impedir conectarse a la base de datos | Media | Alto | Usar el Session pooler de Supabase (mismo puerto 5432 pero en infraestructura diferente que responde por IPv4) |

---

## Deuda técnica identificada

| Elemento | Descripción | Prioridad |
|---|---|---|
| `sessions_memory = {}` | Memoria de chat en RAM, no persiste entre reinicios | Alta |
| Sin versionar la API | Los endpoints no tienen prefijo `/v1/`; un cambio rompe todo | Media |
| Sin tests | Cero cobertura de pruebas automatizadas | Alta |
| Sin Docker | No existe forma reproducible de ejecutar el proyecto en cualquier máquina | Media |
| Sin logs estructurados | Los errores solo aparecen en la terminal del servidor | Media |
| RLS desactivado | Las tablas de Supabase no tienen políticas de seguridad a nivel de fila | Alta |
| OAuth en modo Testing | Solo 100 usuarios máximo y solo cuentas aprobadas | Baja (para demo) |
| `.pkl` fuera del repo | Dependencia manual que puede perderse o desincronizarse | Alta |
