from pydantic import BaseModel
from typing import Optional

class Dish(BaseModel):
    id: Optional[int]
    name: str
    calories: int
    price: float
