
import json
import os
import statistics
import subprocess
import time
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BENCHMARK_BASE_URL", "https://gamevisionia.onrender.com")
TEST_ACCESS_TOKEN = os.getenv("TEST_ACCESS_TOKEN")

N_PREDICT = 20
N_CHAT = 3
TIMEOUT_S = 30

GAME_PAYLOAD = {
    "price_initial": 9.99,
    "is_free": 0,
    "release_year": 2025,
    "release_month": 6,
    "genre_Indie": 1,
    "genre_Casual": 0,
    "genre_Action": 0,
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
    "cat_Shared_Split_Screen_Co_op": 0,
}

CHAT_MESSAGES = [
    "¿Qué significa este resultado de predicción?",
    "¿Qué podría mejorar el potencial comercial de este juego?",
    "¿Qué género suele desempeñarse mejor en Steam?",
]


def percentile(data: list[float], pct: float) -> float:
    """Percentil por interpolación lineal (mismo método que usa numpy)."""
    if not data:
        return 0.0
    data = sorted(data)
    k = (len(data) - 1) * (pct / 100)
    f, c = int(k), min(int(k) + 1, len(data) - 1)
    if f == c:
        return round(data[f], 2)
    return round(data[f] + (data[c] - data[f]) * (k - f), 2)


def get_git_commit() -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, timeout=5,
        )
        return out.stdout.strip() or "desconocido"
    except Exception:
        return "desconocido"


def warm_up() -> None:
    """
    Petición de calentamiento, NO se cuenta en las métricas.
    Si Render está dormido (cold-start), aquí es donde se paga ese
    costo — separado a propósito de la línea base, porque el cold-start
    ya está documentado como su propio hallazgo desde Semana 4.
    """
    print(f"Despertando el servicio en {BASE_URL} (puede tardar ~50s si está dormido)...")
    t0 = time.perf_counter()
    try:
        requests.get(f"{BASE_URL}/health", timeout=90)
        print(f"  listo en {round((time.perf_counter() - t0) * 1000)} ms\n")
    except requests.exceptions.RequestException as exc:
        print(f"  [advertencia] no se pudo despertar el servicio: {exc}\n")


def run_batch(name: str, method: str, url: str, n: int, headers=None, json_body=None):
    """
    Corre n peticiones secuenciales contra un endpoint y devuelve las
    métricas + las respuestas exitosas (por si el llamador necesita
    algo del body, como el session_id de una predicción real).
    """
    durations, statuses, errors = [], [], []
    bodies = []

    print(f"--- {name} ({n} peticiones secuenciales) ---")
    for i in range(1, n + 1):
        t0 = time.perf_counter()
        try:
            resp = requests.request(
                method, url, headers=headers, json=json_body, timeout=TIMEOUT_S
            )
            duration_ms = (time.perf_counter() - t0) * 1000
            durations.append(duration_ms)
            statuses.append(resp.status_code)
            if resp.status_code >= 400:
                errors.append(resp.status_code)
            else:
                try:
                    bodies.append(resp.json())
                except ValueError:
                    pass
            print(f"  [{i}/{n}] {resp.status_code} — {duration_ms:.1f} ms")
        except requests.exceptions.RequestException as exc:
            duration_ms = (time.perf_counter() - t0) * 1000
            durations.append(duration_ms)
            errors.append(type(exc).__name__)
            print(f"  [{i}/{n}] ERROR ({type(exc).__name__}) — {duration_ms:.1f} ms")

    result = {
        "endpoint": name,
        "n": n,
        "p50_ms": percentile(durations, 50),
        "p95_ms": percentile(durations, 95),
        "max_ms": round(max(durations), 2) if durations else 0,
        "avg_ms": round(statistics.mean(durations), 2) if durations else 0,
        "error_rate": round(len(errors) / n, 3) if n else 0,
        "status_codes": statuses,
    }
    print(f"  p50={result['p50_ms']}ms  p95={result['p95_ms']}ms  "
          f"max={result['max_ms']}ms  error_rate={result['error_rate']*100:.1f}%\n")
    return result, bodies


def main() -> None:
    warm_up()

    results = {
        "metadata": {
            "fecha_utc": datetime.now(timezone.utc).isoformat(),
            "ambiente": BASE_URL,
            "version_codigo": get_git_commit(),
            "payload_predict": GAME_PAYLOAD,
        },
        "escenarios": [],
    }

    # --- Escenario 1 (oficial): /api/predict-demo, sin auth ---
    r_demo, _ = run_batch(
        "POST /api/predict-demo (sin auth, comparación auxiliar)",
        "POST", f"{BASE_URL}/api/predict-demo", N_PREDICT,
        json_body=GAME_PAYLOAD,
    )
    results["escenarios"].append(r_demo)

    if not TEST_ACCESS_TOKEN:
        print("No hay TEST_ACCESS_TOKEN en tu .env — se omite /api/predict "
              "(real) y /api/chat. Solo se midió /predict-demo.\n")
    else:
        headers = {"Authorization": f"Bearer {TEST_ACCESS_TOKEN}"}

        # --- Escenario 2 (oficial): /api/predict real, con auth ---
        r_real, bodies_real = run_batch(
            "POST /api/predict (real, flujo crítico de producción)",
            "POST", f"{BASE_URL}/api/predict", N_PREDICT,
            headers=headers, json_body=GAME_PAYLOAD,
        )
        results["escenarios"].append(r_real)

        # --- Escenario 3: /api/chat, muestra chica ---
        session_id = None
        for body in reversed(bodies_real):
            if isinstance(body, dict) and body.get("session_id"):
                session_id = body["session_id"]
                break

        if session_id is None:
            print("No se obtuvo session_id de /predict — se omite /api/chat.\n")
        else:
            chat_durations, chat_statuses = [], []
            print(f"--- POST /api/chat (muestra de {N_CHAT}, session_id={session_id}) ---")
            for i, message in enumerate(CHAT_MESSAGES[:N_CHAT], start=1):
                t0 = time.perf_counter()
                try:
                    resp = requests.post(
                        f"{BASE_URL}/api/chat", headers=headers, timeout=TIMEOUT_S,
                        json={"session_id": session_id, "message": message},
                    )
                    duration_ms = (time.perf_counter() - t0) * 1000
                    chat_durations.append(duration_ms)
                    chat_statuses.append(resp.status_code)
                    print(f"  [{i}/{N_CHAT}] {resp.status_code} — {duration_ms:.1f} ms")
                except requests.exceptions.RequestException as exc:
                    duration_ms = (time.perf_counter() - t0) * 1000
                    chat_durations.append(duration_ms)
                    print(f"  [{i}/{N_CHAT}] ERROR ({type(exc).__name__}) — {duration_ms:.1f} ms")

            results["escenarios"].append({
                "endpoint": "POST /api/chat (muestra chica, no percentiles formales)",
                "n": len(chat_durations),
                "avg_ms": round(statistics.mean(chat_durations), 2) if chat_durations else 0,
                "max_ms": round(max(chat_durations), 2) if chat_durations else 0,
                "status_codes": chat_statuses,
                "nota": "Muestra pequeña por cuota externa de Gemini; "
                        "no se calculan p50/p95 formales.",
            })
            print()

    os.makedirs("../docs/evidencias", exist_ok=True)
    output_path = "../docs/evidencias/linea_base_rendimiento.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"Resultados guardados en {output_path}")
    print("\n=== RESUMEN ===")
    for r in results["escenarios"]:
        print(f"- {r['endpoint']}")
        if "p50_ms" in r:
            print(f"    p50={r['p50_ms']}ms  p95={r['p95_ms']}ms  "
                  f"max={r['max_ms']}ms  error_rate={r['error_rate']*100:.1f}%")
        else:
            print(f"    avg={r['avg_ms']}ms  max={r['max_ms']}ms")


if __name__ == "__main__":
    main()
