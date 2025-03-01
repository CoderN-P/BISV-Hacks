import json
from typing import Literal

from openai import OpenAI
from pydantic import BaseModel
from typing import List
from Item import Item
from enum import Enum


client = OpenAI()

class IngredientScore(Enum):
    GOOD = "good"
    MID = "mid"
    BAD = "bad"

class IngredientSummary(BaseModel):
    summary: str
    score: IngredientScore
# Response model (OpenAI Structured Data)
class FoodResponse(BaseModel):
    recommended_products: List[str]
    fat: IngredientSummary
    calories: IngredientSummary
    description: str
    score: float

class FoodRequest(BaseModel):
    #recipe: recommend recipes, nutrition: summarize nutrition info, summary: explain what product is
    request_type: Literal["recipe", "nutrition", "summary"]
    item: Item

# Function to generate response
def generate_food_response(request: FoodRequest) -> FoodResponse:
    assert(isinstance(request, FoodRequest))
    item = request.item
    with open(f"GPT_SYSTEM_PROMPT_{request.request_type.upper()}.txt", "r", encoding="utf-8") as f:
        system_prompt = f.read()
    

    user_prompt = item.model_dump_json()

    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        temperature=1,
        max_tokens=1000,
        top_p=1,
        response_format=FoodResponse,
    )

    return response.choices[0].message.parsed
