from openai import OpenAI
from pydantic import BaseModel
from typing import List
from Item import Item


client = OpenAI()


# Response model (OpenAI Structured Data)
class FoodResponse(BaseModel):
    recommended_products: List[str]
    description: str
    
    
# Function to generate response
def generate_food_response(item: Item) -> FoodResponse:
    system_prompt = "You are a helpful nutrition scientist and advisor. You will be helping people make healthy and informed food choices. Given some information about a food product, explain to the user what the product is and recommend similar products."
    user_prompt = ""
    
    for k, v in item.model_dump().items():
        user_prompt += f"{k}: {v}\n"
        
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