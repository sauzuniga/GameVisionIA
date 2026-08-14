from fastapi import APIRouter, Depends, HTTPException, Request

from sqlalchemy.orm import Session



from auth import get_current_user

from database import get_db

from models import ChatSession, Prediction

from schemas import DemoPredictionResponse, GameInput, PredictionResponse

from services.predict_service import model, run_prediction



router = APIRouter()





def _stash_observability_state(request: Request, result: dict) -> None:

    """

    Guarda model_version y stage_timings en request.state para que el

    middleware de observabilidad (main.py) los incluya en el log y en

    el registro de RequestLog, sin acoplar predict_service a Supabase.

    Si esto falla por lo que sea, la predicción ya calculada se devuelve

    igual — nunca debe tumbar la respuesta al usuario.

    """

    try:

        request.state.model_version = result.get("model_version")

        request.state.stage_timings = result.get("stage_timings")

    except Exception:

        pass





@router.post("/predict", response_model=PredictionResponse)

def predict(

    game: GameInput,

    request: Request,

    db: Session = Depends(get_db),

    user_id: str = Depends(get_current_user)

):

    if model is None:

        raise HTTPException(

            status_code=503,

            detail={

                "error": "model_unavailable",

                "detail": "El modelo no está disponible."

            }

        )



    request_id = getattr(request.state, "request_id", None)



    try:

        result = run_prediction(game.model_dump(), request_id=request_id)

        _stash_observability_state(request, result)

    except Exception as exc:

        raise HTTPException(

            status_code=500,

            detail={

                "error": "prediction_failed",

                "detail": f"Error al ejecutar el modelo: {str(exc)}"

            }

        ) from exc



    try:

        db_prediction = Prediction(

            user_id=user_id,

            probability=result["confidence"],

            predicted_class=result["predicted_class"],

            potential_level=result["potential_level"],

            price_initial=game.price_initial,

            is_free=game.is_free,

            release_year=game.release_year,

            release_month=game.release_month,

            genres=",".join([

                k.replace("genre_", "") for k, v in game.model_dump().items()

                if k.startswith("genre_") and v == 1

            ]),

            categories=",".join([

                k.replace("cat_", "") for k, v in game.model_dump().items()

                if k.startswith("cat_") and v == 1

            ])

        )

        db.add(db_prediction)

        db.commit()

        db.refresh(db_prediction)



        chat_session = ChatSession(prediction_id=db_prediction.id)

        db.add(chat_session)

        db.commit()

        db.refresh(chat_session)



    except Exception as exc:

        db.rollback()

        raise HTTPException(

            status_code=500,

            detail={

                "error": "database_error",

                "detail": "Error al guardar la predicción."

            }

        ) from exc



    return {

        "id": db_prediction.id,

        "result": result["result"],

        "confidence": result["confidence"],

        "probability": result["confidence"], 

        "predicted_class": result["predicted_class"],

        "potential_level": result["potential_level"],

        "model_version": result["model_version"],

        "warnings": result["warnings"],

        "request_id": result["request_id"],

        "session_id": chat_session.id,

        "created_at": db_prediction.created_at

    }





@router.post("/predict-demo", response_model=DemoPredictionResponse)

def predict_demo(game: GameInput, request: Request):

    """

    Endpoint público de demostración. No requiere autenticación

    y no guarda nada en la base de datos. Usa el mismo modelo real.

    """

    if model is None:

        raise HTTPException(

            status_code=503,

            detail={

                "error": "model_unavailable",

                "detail": "El modelo no está disponible."

            }

        )



    request_id = getattr(request.state, "request_id", None)



    try:

        result = run_prediction(game.model_dump(), request_id=request_id)

        _stash_observability_state(request, result)

    except Exception as exc:

        raise HTTPException(

            status_code=500,

            detail={

                "error": "prediction_failed",

                "detail": f"Error al ejecutar el modelo: {str(exc)}"

            }

        ) from exc



    return {

        "result": result["result"],

        "confidence": result["confidence"],

        "predicted_class": result["predicted_class"],

        "potential_level": result["potential_level"],

        "model_version": result["model_version"],

        "warnings": result["warnings"],

        "request_id": result["request_id"],

        "demo": True,

        "note": "Endpoint de demostración. No requiere autenticación y no guarda historial."

    } 

