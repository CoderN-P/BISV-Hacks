from pydantic import BaseModel
from typing import Union

class Item(BaseModel):
    code: str = ""
    url: str = ""
    sugars_100g: float = 0
    product_name: str = ""
    ingredients_text: str = ""
    image_url: str = ""
    nutrition_score: str = ""
    kcal: Union[int, float] = 0
    bicarbonate_100g: float = 0
    potassium_100g: float = 0
    chloride_100g: float = 0
    calcium_100g: float = 0
    phosphorus_100g: float = 0
    iron_100g: float = 0
    magnesium_100g: float = 0
    zinc_100g: float = 0
    copper_100g: float = 0
    manganese_100g: float = 0
    fluoride_100g: float = 0
    fat_100g: float = 0
    saturated_fat_100g: float = 0
    selenium_100g: float = 0
    chromium_100g: float = 0
