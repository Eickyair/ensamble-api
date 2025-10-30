from fastapi import APIRouter
from app.models.schemas import HealthResponse

router = APIRouter(prefix="", tags=["Health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Verify that the API is running and responsive",
    responses={
        200: {
            "description": "API is healthy and operational",
            "content": {
                "application/json": {
                    "example": {"status": "ok"}
                }
            }
        }
    }
)
async def health_check() -> HealthResponse:
    """
    Check the health status of the API.

    Returns a simple status indicator to confirm the API is running.
    This endpoint can be used for monitoring and load balancer health checks.
    """
    return HealthResponse(status="ok")