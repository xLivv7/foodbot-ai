from fastapi import FastAPI
import os
from .routers import ingredients, recipes

app = FastAPI(title="FoodBot Recipes API", version="1.0.0")

@app.get("/healthz", tags=["health"])
def healthz():
    return {"status": "ok", "env": os.getenv("APP_ENV", "dev")}

app.include_router(ingredients.router)
app.include_router(recipes.router)
