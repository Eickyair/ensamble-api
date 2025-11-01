from fastapi import APIRouter, HTTPException
import os
import joblib
import sys
from functools import lru_cache
from model.rf_custom import SimpleRandomForest
from app.models.schemas import PredictionInput, PredictionResponse

sys.modules['__main__'].SimpleRandomForest = SimpleRandomForest


@lru_cache()
def load_model():
    """Load model once and cache it"""
    PATH_MODEL = os.path.join(os.path.dirname(__file__), "..", "..", "model", "model.pkl")
    model = joblib.load(PATH_MODEL)
    print("Modelo cargado:")
    print(model['est'])
    return model['est']

# Caché muy agresivo (1000 predicciones únicas)
@lru_cache(maxsize=1000)
def cached_predict(features_tuple):
    model = load_model()
    features = [list(features_tuple)]
    prediction_index = model.predict(features)[0]
    return int(prediction_index)

router = APIRouter(prefix="", tags=["Predictions"])

MAP_INDEX_TO_SPECIES = {0: "setosa", 1: "versicolor", 2: "virginica"}

@router.post(
    "/predict",
    summary="Make Prediction",
    description="Submit data to receive a prediction from the ensemble model",
    response_model=PredictionResponse,
    responses={
        400: {"description": "Invalid input"},
        500: {"description": "Internal server error"}
    }
)
async def predict(input_data: PredictionInput) -> PredictionResponse:
    """
    Make a prediction using the ensemble machine learning model.
    """
    try:
        features_tuple = tuple(input_data.features)
        print("Received features:", features_tuple)
        prediction_index = cached_predict(features_tuple)
        specie = MAP_INDEX_TO_SPECIES.get(prediction_index, "unknown")
        return PredictionResponse(prediction=specie)
    except Exception as e:
        print("Error during prediction:", e, file=sys.stderr)
        raise HTTPException(status_code=500, detail=f"Error en predicción")