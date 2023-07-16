from os import getenv
import requests
from fastapi import HTTPException, status

import aiohttp

ALPHAVANTAGE_APIKEY = getenv("ALPHAVANTAGE_APIKEY")


def sync_converter(from_currency: str, to_currency: str, price: float):
    url = (
        "https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_"
        + f"currency={from_currency}&to_currency={to_currency}&apikey="
        + f"{ALPHAVANTAGE_APIKEY}"
    )
    try:
        resp = requests.get(url)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)

    data = resp.json()

    if "Realtime Currency Exchange Rate" not in data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Realtime Currency Exchange Rate not in response-{data}",
        )

    exchange_rate = float(data["Realtime Currency Exchange Rate"]["5. Exchange Rate"])
    return price * exchange_rate


async def async_converter(from_currency: str, to_currency: str, price: float):
    url = (
        "https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_"
        + f"currency={from_currency}&to_currency={to_currency}&apikey="
        + f"{ALPHAVANTAGE_APIKEY}"
    )
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url) as response:
                data = await response.json()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)

    if "Realtime Currency Exchange Rate" not in data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Realtime Currency Exchange Rate not in response-{data}",
        )

    exchange_rate = float(data["Realtime Currency Exchange Rate"]["5. Exchange Rate"])
    return price * exchange_rate
