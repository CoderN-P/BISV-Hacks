from typing import Union
import openfoodfacts
from dotenv import load_dotenv


load_dotenv()
from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware

from get_response import generate_food_response, FoodRequest
from Item import Item

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://0.0.0.0:5173",
    "https://foodlyze.neelp.tech"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# User-Agent is mandatory
api = openfoodfacts.API(user_agent="MyAwesomeApp/1.0")

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{code}")
def get_item(code: str, response: Response):
    product_fields = ["code", "product_name", "ingredients_text", "image_url", "nutrition-score-uk_100g", "energy-kcal_100g", "bicarbonate_100g", 
                      "potassium_100g",
                      "chloride_100g",
                      "calcium_100g",
                      "phosphorus_100g",
                      "iron_100g",
                      "magnesium_100g",
                      "zinc_100g",
                      "copper_100g",
                      "manganese_100g",
                      "fluoride_100g",
                      "selenium_100g",
                      "chromium_100g",
                    "fat_100g",
                      "sugars_100g",
                      "url"
                    ]
    data = api.product.get(code, fields=product_fields)

    if data is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Product not found"}
    if data.get("energy-kcal_100g"):
        data["kcal"] = data.pop("energy-kcal_100g")
    if data.get("nutrition-score-uk_100g"):
        data["nutrition_score"] = data.pop("nutrition-score-uk_100g")

    return Item(**data)

@app.post("/summary")
def summarize_item(request: FoodRequest, response: Response):

    try:
        res = generate_food_response(request)
    except Exception as e:
        try:
            res = generate_food_response(request)
        except Exception as exc:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {"error": str(exc)}

    data = {
        "description": res.description,
        "recommended_products": res.recommended_products,
        "fat": {
            "summary": res.fat.summary,
            "score": res.fat.score.value,
        },
        "score": res.score,
        "calories": {
            "summary": res.calories.summary,
            "score": res.calories.score.value,
        },
        "sugars": {
            "summary": res.sugars.summary,
            "score": res.sugars.score.value,
        },
    }

    return data
