from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """
    Configuration settings for the application, loaded from environment variables.

    Attributes:
        DATABASE_URL (str): Database connection URL.
        REDIS_HOST (str): Redis server host.
        REDIS_PORT (int): Redis server port.
        REDIS_CACHE_TTL (int): Cache TTL (Time-To-Live) for Redis in seconds.
        COINGECKO_API_BASE (str): Base URL for the CoinGecko API.
        UPDATE_INTERVAL_MINUTES (int): Interval in minutes for scheduled tasks.

    Configuration is loaded from environment variables or defaults.
    """
    # Database
    DATABASE_URL: str = Field(..., env="DATABASE_URL")

    # Redis
    REDIS_HOST: str = Field(default="redis", env="REDIS_HOST")
    REDIS_PORT: int = Field(default=6379, env="REDIS_PORT")
    REDIS_CACHE_TTL: int = Field(default=3600, env="REDIS_CACHE_TTL")

    # Coingecko
    COINGECKO_API_BASE: str = Field(default="https://api.coingecko.com/api/v3", env="COINGECKO_API_BASE")

    # Update interval
    UPDATE_INTERVAL_MINUTES: int = Field(default=10, env="UPDATE_INTERVAL_MINUTES")

    class Config:
        env_file = ".env"


settings = Settings()
