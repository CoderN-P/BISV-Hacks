from pydantic import BaseModel
from typing import Union

class Item(BaseModel):
    code: str = ""
    product_name: str = ""
    ingredients_text: str = ""
    image_url: str = ""
    nutrition_score: str = ""