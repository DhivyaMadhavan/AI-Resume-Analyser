from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Application
    APP_NAME: str
    APP_VERSION: str
    API_PREFIX: str

    # MongoDB
    MONGO_URI: str
    DATABASE_NAME: str

    # Redis
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int

    # Gemini
    GEMINI_API_KEY: str 

    class Config:
        env_file = ".env"


settings = Settings()