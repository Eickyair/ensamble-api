from fastapi import APIRouter
from app.models.schemas import ModelInfo

router = APIRouter(prefix="", tags=["Info"])


@router.get(
    "/info",
    response_model=ModelInfo,
    summary="Get Model Information",
    description="Retrieve configuration and metadata about the ensemble model",
    responses={
        200: {
            "description": "Model information retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "team": "pi",
                        "model": "RandomForestClassifier",
                        "n_estimators": 50,
                        "max_features": "sqrt",
                        "max_depth": 8
                    }
                }
            }
        }
    }
)
async def info() -> ModelInfo:
    """
    Get detailed information about the machine learning model.
    
    Returns:
        ModelInfo: Configuration details including team identifier,
                   model type, and hyperparameters.
    """
    return ModelInfo(
        team="pi",
        model="RandomForestClassifier",
        n_estimators=50,
        max_features="sqrt",
        max_depth=8
    )