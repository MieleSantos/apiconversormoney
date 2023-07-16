import re
from pydantic import BaseModel, Field, validator
from typing import List


class ConverterInput(BaseModel):
    price: float = Field(gt=0)
    to_currencies: List[str]

    @validator("to_currencies")
    def validate_to_currencies(cls,value):
        

"""
{
    "price": 1234,
    "to_currencies": ["USD","GBP"]
}
"""
