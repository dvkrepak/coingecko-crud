from pycoingecko import CoinGeckoAPI
import redis
from app.core.settings import settings

# Initialize CoinGecko API client
cg = CoinGeckoAPI()

# Set up Redis client for caching
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True
)
