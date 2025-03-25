import json
import logging
import time

from fastapi import HTTPException

from app.core.settings import settings
from .clients import cg, redis_client as r

logger = logging.getLogger(__name__)


def get_cached_coins_list():
    """
    Retrieve the list of coins, either from Redis cache or Coingecko API.

    Caches the coin list in Redis for subsequent requests to avoid repeated API calls.

    Returns:
        list: A list of coins fetched from Coingecko or Redis cache.

    Raises:
        HTTPException: If fetching coins from Coingecko fails.
    """
    cached = r.get("coins_list")
    if cached:
        logger.debug("Loaded coins list from Redis cache")
        return json.loads(cached)

    logger.info("Fetching coins list from Coingecko API")
    try:
        coins = cg.get_coins_list()
        r.set("coins_list", json.dumps(coins), ex=settings.REDIS_CACHE_TTL)
        logger.info(f"Cached {len(coins)} coins to Redis")
        return coins
    except Exception as e:
        logger.exception("Failed to fetch coins list from Coingecko")
        raise HTTPException(status_code=502, detail="Failed to fetch coins list from external API")


def resolve_to_id(query: str) -> str | None:
    """
    Resolve a query (coin symbol, name, or ID) to a CoinGecko ID.

    Searches for an exact match for the coin ID, symbol, or name.

    Args:
        query (str): The query to resolve (e.g., coin symbol or name).

    Returns:
        str | None: The resolved CoinGecko ID or None if not found.

    Raises:
        HTTPException: If there are multiple matches for a symbol or no match found.
    """
    query_lower = query.lower()
    coins = get_cached_coins_list()

    # 1. Exact match on CoinGecko ID
    for coin in coins:
        if coin["id"].lower() == query_lower:
            logger.debug(f"Resolved '{query}' as exact Coingecko ID")
            return coin["id"]

    # 2. Exact match on symbol
    matches = [coin for coin in coins if coin["symbol"].lower() == query_lower]
    if len(matches) == 1:
        logger.debug(f"Resolved '{query}' to ID via symbol match: {matches[0]['id']}")
        return matches[0]["id"]
    elif len(matches) > 1:
        logger.warning(f"Ambiguous symbol '{query}': multiple matches")
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
            logger.debug(f"Resolved '{query}' to ID via name match: {coin['id']}")
            return coin["id"]

    logger.warning(f"Failed to resolve '{query}' to any known coin")
    return None


def fetch_crypto_data(query: str):
    """
    Fetch market data for a cryptocurrency from CoinGecko.

    Args:
        query (str): The query to resolve (e.g., coin symbol or name).

    Returns:
        dict | None: A dictionary containing the coin's market data or None if not found.
    """
    start = time.time()
    coin_id = resolve_to_id(query)
    duration = round(time.time() - start, 2)
    logger.info(f"Coingecko API responded in {duration}s for {coin_id}")
    if not coin_id:
        logger.warning(f"Coin '{query}' not found in Coingecko")
        return None
    try:
        data = cg.get_coin_by_id(id=coin_id)
        logger.info(f"Fetched market data for coin '{coin_id}'")
        return {
            "id": data["id"],
            "name": data["name"],
            "symbol": data["symbol"],
            "price": data["market_data"]["current_price"]["usd"]
        }
    except Exception:
        logger.exception(f"Failed to fetch market data for coin '{coin_id}'")
        return None
