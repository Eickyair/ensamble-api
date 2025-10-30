from fastapi import FastAPI, HTTPException, Request
from app.routers import health, info,predict

app = FastAPI(
    title="Ensamble API",
    description="API for ensemble model predictions using RandomForest classifier",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Health",
            "description": "Health check and monitoring endpoints"
        },
        {
            "name": "Info",
            "description": "Model configuration and metadata endpoints"
        }
    ]
)

# Include routers
app.include_router(health.router)
app.include_router(info.router)
app.include_router(predict.router)


@app.api_route(
    "/{path_name:path}",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    include_in_schema=False
)
async def catch_all(path_name: str, _: Request) -> None:
    """Catch-all route for undefined endpoints"""
    raise HTTPException(
        status_code=404,
        detail={
            "error": "Ruta no encontrada",
            "path": f"/{path_name}"
        }
    )