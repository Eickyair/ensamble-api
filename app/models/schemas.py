from pydantic import BaseModel, Field
from typing import Literal


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