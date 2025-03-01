import json
from typing import Literal

from openai import OpenAI
from pydantic import BaseModel
from typing import List
from Item import Item


client = OpenAI()


# Response model (OpenAI Structured Data)
class FoodResponse(BaseModel):
    recommended_products: List[str]
    description: str

class FoodRequest(BaseModel):
    #recipe: recommend recipes, nutrition: summarize nutrition info, summary: explain what product is
    request_type: Literal["recipe", "nutrition", "summary"]
    item: Item

# Function to generate response
def generate_food_response(request: FoodRequest) -> FoodResponse:
    assert(isinstance(request, FoodRequest))
    item = request.item
    with open("GPT_SYSTEM_PROMPT.txt", "r", encoding="utf-8") as f:
        system_prompt = f.read()
    user_prompt = ""

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
        max_tokens=500,
        top_p=1,
        response_format=FoodResponse,
    )

    return response.choices[0].message.parsed
