# Plan de contingencia de la demostración — GameVision IA

Release evaluado: `v1.0.0-rc.1` (commit `b21aa85`)


## Riesgos, prevención y respuesta preparada

| Riesgo | Prevención (acción concreta) | Respuesta preparada (pasos exactos) |
|---|---|---|
| Servicio render dormido (cold-start ~53s medido en Semana 5) | Abrir `/health` desde un cualquier dispositivo del equipo 15 minutos antes de que empiece nuestra exposición | Si igual sale lento en vivo: explicar para todos la situación y que todo se debe al cold-start del plan gratuito, mencionar que se documento en la Semana 5, tarda hasta ~55s en despertar el backend de la app cuando el servicio al ser un plan gratuito de render se duerme por inactividad|
| Cuota de Gemini agotada | Sábado: entrar a aistudio.google.com/apikey, confirmar que la cuota diaria (RPD) de gemini-2.5-flash no está en 0 | El timeout de 20s ya implementado responde con 504 controlado — mostrarlo como el control funcionando, no como una disculpa |
| Deploy roto o release incorrecto en producción | No tocar configuración de Render/Vercel entre el freeze del sábado y la demo | **Confirmado disponible (captura 19/08/2026).** Rollback paso a paso: 1) Render Dashboard → servicio → pestaña "Events". 2) Buscar el deploy exitoso de `v1.0.0-rc.1` (o el commit estable `1e62dbc`). 3) Clic en "Rollback" → confirmar. 4) **Importante:** esto desactiva el autodeploy — reactivarlo en Settings después de la crisis. **Respaldo si el botón no aparece para un commit específico:** `git checkout v1.0.0-rc.1 -- .` + commit + push, dispara el pipeline normal |
| Sesión de la cuenta demo vencida (Google OAuth) | Iniciar sesión con la cuenta demo la noche antes **y** la mañana del domingo — no asumir que la sesión guardada sigue viva | Reingreso rápido con la misma cuenta; credenciales accesibles solo por el equipo, nunca visibles en pantalla compartida |
| Red, audio o pantalla compartida falla | Probar la plataforma de videollamada, cámara y compartir pantalla el sábado, no el domingo en la mañana | Segundo dispositivo con hotspot, ya logueado y con `game-vision-ia.vercel.app` abierto de antemano |
| Supabase con caída real de su plataforma (no algo causado por nosotros) | Verificar `status.supabase.com` el sábado durante el freeze | Externa y verificable — mostrar capturas de respaldo de una corrida exitosa anterior, con captura de la página de estado de Supabase como prueba, y avisar al docente antes de usarlas |
| Examinador remoto (otro país) prueba la URL por su cuenta, no solo observa por pantalla compartida | Confirmar con antelación si el examinador interactuará directo con la app o solo observará; probar la URL desde una VPN de otro país antes del domingo para estimar la latencia real | Si se ve lento desde su conexión: explicar que es la latencia de red esperada según la región de despliegue (Render, plan gratuito), no una falla — mismo tono que con el cold-start |

## Cuándo sí se puede usar el respaldo (y cuándo no)

El respaldo (capturas de una corrida exitosa anterior) **no sustituye la demo en vivo por comodidad** — según la sección 11 del descriptor: *"Falta de créditos, servicio no activado, credenciales vencidas o release incorrecto son contingencias controlables"*, es decir, **no** justifican usar el respaldo, son responsabilidad nuestra haberlas prevenido. Solo aplica ante algo externo, verificable, y con autorización del docente en el momento.

| Situación | ¿Justifica usar el respaldo? |
|---|---|
| Caída real de la plataforma de Supabase (verificable en status.supabase.com) | Sí — externa y comprobable |
| Falla total de internet/energía en el lugar de la defensa | Sí — externa y evidente |
| Cuota de Gemini agotada | No — controlable, se revisa antes |
| Cold-start de Render | No — se maneja calentando el servicio antes, no es excusa |
| Sesión o credenciales vencidas | No — controlable, se revisa antes |

**Dónde vive:** capturas guardadas en `docs/final/respaldo/` dentro de este mismo repositorio.

## Caso exitoso preparado — mapeado a los 3 minutos exactos de la demo

| Tiempo | Acción |
|---|---|
| 0:00–0:20 | Abrir `https://game-vision-ia.vercel.app`, mencionar en voz alta la versión (`v1.0.0`) |
| 0:20–1:30 | Iniciar sesión con la cuenta demo, ejecutar una predicción con el payload fijo de abajo, mostrar resultado y `session_id` |
| 1:30–2:10 | Enviar el mismo payload con `price_initial` en negativo, mostrar el 422 controlado |
| 2:10–2:40 | Abrir `/health` o `/metadata`, mostrar estado del modelo y la base de datos |
| 2:40–3:00 | Cerrar mencionando una limitación honesta (ej. sin rate limiting) y que existe un plan de rollback probado |

**Payload fijo del caso exitoso** (el mismo usado en las pruebas automatizadas — ya probado docenas de veces, sin sorpresas):

```json
{
  "price_initial": 19.99, "is_free": 0, "release_year": 2023, "release_month": 6,
  "genre_Indie": 1, "genre_Casual": 0, "genre_Action": 1, "genre_Adventure": 0,
  "genre_Simulation": 0, "genre_Strategy": 0, "genre_RPG": 1,
  "genre_Early_Access": 0, "genre_Free_To_Play": 0,
  "cat_Single_player": 1, "cat_Multi_player": 0, "cat_PvP": 0, "cat_Co_op": 0,
  "cat_Online_PvP": 0, "cat_Online_Co_op": 0, "cat_Shared_Split_Screen": 0,
  "cat_Shared_Split_Screen_PvP": 0, "cat_Shared_Split_Screen_Co_op": 0
}
```

**Payload del caso de error controlado:** el mismo de arriba, con `"price_initial": -10`.



## Verificaciones programadas

| Momento | Acciones |
|---|---|
| Sábado (~24h antes) | Congelar release final (`v1.0.0`), correr smoke test completo, **probar el rollback una vez de verdad** (no asumir que funciona) |
| ~1 horas antes | Confirmar URL pública, cuenta demo, cuota de Gemini, pipeline en verde |
| ~15 minutos antes | Calentar el backend (`/health`), iniciar sesión con la cuenta demo, cerrar notificaciones, dejar pestañas necesarias abiertas |
| Al finalizar | No dejar credenciales visibles en pantalla; registrar cualquier incidente ocurrido durante la demo |

## Responsable de la demo y del respaldo



- Persona que ejecuta la demo: Bryan Orlando Giron


