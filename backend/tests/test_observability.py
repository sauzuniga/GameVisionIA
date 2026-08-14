from fastapi.testclient import TestClient

from main import app

client = TestClient(app)





def juego_valido() -> dict:

    return {

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





def test_health_incluye_headers_de_observabilidad() -> None:

    """Toda respuesta, incluida /health, debe llevar request_id y duración."""

    response = client.get("/health")



    assert response.status_code == 200

    assert "X-Request-ID" in response.headers

    assert "X-Process-Time-Ms" in response.headers

    assert len(response.headers["X-Request-ID"]) == 8





def test_predict_demo_incluye_headers_de_observabilidad() -> None:

    """El flujo crítico (/predict-demo) también debe quedar correlacionado."""

    response = client.post("/api/predict-demo", json=juego_valido())



    assert response.status_code == 200

    assert "X-Request-ID" in response.headers

    assert "X-Process-Time-Ms" in response.headers



    duration = float(response.headers["X-Process-Time-Ms"])

    assert duration >= 0





def test_request_id_del_header_coincide_con_el_del_body() -> None:

    """

    El request_id que arma el middleware (header) y el que devuelve

    run_prediction() en el body deben ser el mismo id de correlación,

    no dos ids distintos que no se puedan cruzar.

    """

    response = client.post("/api/predict-demo", json=juego_valido())

    data = response.json()



    assert response.headers["X-Request-ID"] == data["request_id"]





def test_entrada_invalida_tambien_queda_correlacionada() -> None:

    """

    Un error controlado (422 por validación de Pydantic) debe seguir

    llevando headers de observabilidad, para poder correlacionarlo

    igual que una solicitud exitosa.

    """

    payload = juego_valido()

    payload["price_initial"] = -10  # inválido: precio negativo



    response = client.post("/api/predict-demo", json=payload)



    assert response.status_code == 422

    assert "X-Request-ID" in response.headers 

