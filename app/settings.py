from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = Field(..., env="DATABASE_URL")

    # Redis
    REDIS_HOST: str = Field(default="redis", env="REDIS_HOST")
    REDIS_PORT: int = Field(default=6379, env="REDIS_PORT")
    REDIS_CACHE_TTL: int = Field(default=3600, env="REDIS_CACHE_TTL")

    # Coingecko
    COINGECKO_API_BASE: str = Field(default="https://api.coingecko.com/api/v3", env="COINGECKO_API_BASE")

    class Config:
        env_file = ".env"


settings = Settings()
