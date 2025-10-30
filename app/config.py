from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    app_name: str = "Ensamble API"
    app_version: str = "1.0.0"
    model_team: str = "pi"
    model_type: str = "RandomForestClassifier"
    n_estimators: int = 100
    max_depth: int = 8

    class Config:
        env_file = ".env"


settings = Settings()