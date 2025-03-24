from pycoingecko import CoinGeckoAPI
import redis
from .settings import settings

cg = CoinGeckoAPI()

redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True
)
