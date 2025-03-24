import json

from fastapi import HTTPException

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

    # 1. Exact match on Coingecko ID
    for coin in coins:
        if coin["id"].lower() == query_lower:
            return coin["id"]

    # 2. Exact match on symbol
    matches = [coin for coin in coins if coin["symbol"].lower() == query_lower]
    if len(matches) == 1:
        return matches[0]["id"]
    elif len(matches) > 1:
        raise HTTPException(
            status_code=400,
            detail={
                "error": f"Symbol '{query}' is ambiguous.",
                "message": "Multiple coins found with this symbol. Please use full coin ID.",
                "options": [f"{coin['id']} ({coin['name']})" for coin in matches]
            }
        )

    # 3. Exact match on name
    for coin in coins:
        if coin["name"].lower() == query_lower:
            return coin["id"]

    # 4. Not found
    return None


def fetch_crypto_data(query: str):
    coin_id = resolve_to_id(query)
    if not coin_id:
        return None
    try:
        data = cg.get_coin_by_id(id=coin_id)
        return {
            "id": data["id"],
            "name": data["name"],
            "symbol": data["symbol"],
            "price": data["market_data"]["current_price"]["usd"]
        }
    except Exception:
        return None

