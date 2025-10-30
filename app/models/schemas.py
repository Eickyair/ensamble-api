from pydantic import BaseModel, Field, field_validator
from typing import Literal, List


class HealthResponse(BaseModel):
    """Health check response model"""
    status: Literal["ok"] = Field(
        description="API health status",
        examples=["ok"]
    )


class ModelInfo(BaseModel):
    """Model information and configuration"""
    team: str = Field(
        description="Team identifier",
        examples=["pi"]
    )
    model: str = Field(
        description="Machine learning model type",
        examples=["RandomForestClassifier"]
    )
    n_estimators: int = Field(
        description="Number of trees in the forest",
        gt=0,
        examples=[100]
    )
    max_depth: int = Field(
        description="Maximum depth of the trees",
        gt=0,
        examples=[8]
    )


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

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(
        description="Error message",
        examples=["Ruta no encontrada"]
    )
    path: str = Field(
        description="Requested path that caused the error",
        examples=["/invalid/path"]
    )

class ErrorResponseBase(BaseModel):
    """Error response model"""
    error: str = Field(
        description="Error message",
        examples=["Ruta no encontrada"]
    )