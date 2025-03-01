from typing import Union
import openfoodfacts
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173",
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
def read_item(code: str):
    data = api.product.get(code, fields=["code", "product_name", "ingredients_text", "image_url", "nutrition-score-uk_100g"])
    return data


