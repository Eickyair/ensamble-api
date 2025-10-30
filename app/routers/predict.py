from fastapi import APIRouter
from pydantic import BaseModel, Field, field_validator

from typing import List
from typing import Literal
import os, joblib
import sys
from model.rf_custom import SimpleRandomForest

sys.modules['__main__'].SimpleRandomForest = SimpleRandomForest

print(SimpleRandomForest)
PATH_MODEL = os.path.join(os.path.dirname(__file__),"..","..","model","model.pkl")
model = joblib.load(PATH_MODEL)
print("Modelo cargado con éxito")
print("Modelo:", model)

print("Cargando modelo desde:", PATH_MODEL)
class PredictionInput(BaseModel):
    features: List[float] = Field(..., min_length=4, max_length=4)

    @field_validator('features')
    def validate_features(cls, v):
        if len(v) != 4:
            raise ValueError('Must provide exactly 4 features')
        if any(x < 0 for x in v):
            raise ValueError('All features must be greater than or equal to zero')
        return v
class PredictionResponse(BaseModel):
    prediction: Literal["setosa", "versicolor", "virginica", "unknown"]


router = APIRouter(prefix="", tags=["Predictions"])

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
async def predict(input_data: PredictionInput):
    """
    Make a prediction using the ensemble machine learning model.

    Args:
        input_data: Input features for prediction

    Returns:
        dict: A dictionary containing the prediction result.
    """
    features = [input_data.features]
    map_index_to_species = {0: "setosa", 1: "versicolor", 2: "virginica"}
    prediction_index = model['model'].predict(features)[0]
    specie = map_index_to_species.get(prediction_index, "unknown")
    return PredictionResponse(
        prediction=specie,
    )