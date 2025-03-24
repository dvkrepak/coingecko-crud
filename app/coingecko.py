import json
from .settings import settings
from .clients import cg, redis_client as r


def get_cached_coins_list():
    cached = r.get("coins_list")
    if cached:
        return json.loads(cached)
    coins = cg.get_coins_list()
    r.set("coins_list", json.dumps(coins), ex=settings.REDIS_CACHE_TTL)
    return coins


def resolve_to_id(query: str) -> str | None:
    query_lower = query.lower()
    coins = get_cached_coins_list()
    for coin in coins:
        if query_lower in (coin["symbol"].lower(), coin["name"].lower()):
            return coin["id"]
    return None


def fetch_crypto_data(query: str):
    coin_id = resolve_to_id(query)
    if not coin_id:
        return None
    try:
        data = cg.get_coin_by_id(id=coin_id)
        return {
            "name": data["name"],
            "symbol": data["symbol"],
            "price": data["market_data"]["current_price"]["usd"]
        }
    except Exception:
        return None
