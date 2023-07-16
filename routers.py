from asyncio import gather
from fastapi import APIRouter, Path, Query
from converter import sync_converter, async_converter
from schemas import ConverterInput, ConverterOutput

router = APIRouter(prefix="/converter")


@router.get("/{from_currency}")
def converte(
    from_currency: str = Path(max_length=3, regex=r"^[A-Z]{3}$"),
    to_currencies: str = Query(max_length=50, regex=r"^[A-Z]{3}(,[A-Z]{3})*$"),
    price: float = Query(gt=0),
):
    to_currenciess = to_currencies.split(",")

    result = []
    for corrency in to_currenciess:
        response = sync_converter(
            from_currency=from_currency, to_currency=corrency, price=price
        )
        result.append(response)
    return result


@router.get("/async/{from_currency}")
async def async_converter_router(
    from_currency: str = Path(max_length=3, regex=r"^[A-Z]{3}$"),
    to_currencies: str = Query(max_length=50, regex=r"^[A-Z]{3}(,[A-Z]{3})*$"),
    price: float = Query(gt=0),
):
    to_currenciess = to_currencies.split(",")

    couroutines = []

    for corrency in to_currenciess:
        coro = await async_converter(
            from_currency=from_currency, to_currency=corrency, price=price
        )
        couroutines.append(coro)
    result = await gather(*couroutines)
    return result


@router.get("/async/v2/{from_currency}", response_model=ConverterOutput)
async def async_converter_router_v2(
    body: ConverterInput, from_currency: str = Path(max_length=3, regex=r"^[A-Z]{3}$")
):
    to_currenciess = body.to_currencies
    price = body.price

    couroutines = []

    for corrency in to_currenciess:
        coro = await async_converter(
            from_currency=from_currency, to_currency=corrency, price=price
        )
        couroutines.append(coro)
    result = await gather(*couroutines)
    return ConverterOutput(message="success", data=result)
