from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os, httpx

app = FastAPI(title="FoodBot Web UI", version="1.1.0")
templates = Jinja2Templates(directory="app/templates")
API_BASE_URL = os.getenv("API_BASE_URL", "http://recipes-api:8000")

STATIC_DIR = Path(__file__).resolve().parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/config.json", include_in_schema=False)
def config_json():
    return FileResponse(STATIC_DIR / "config.json", media_type="application/json")


@app.get("/healthz", tags=["health"])
def healthz():
    return {"status": "ok", "env": os.getenv("APP_ENV", "dev")}

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    async with httpx.AsyncClient(timeout=3.0) as client:
        try:
            r = await client.get(f"{API_BASE_URL}/healthz"); api_ok = r.json()
        except Exception as e:
            api_ok = {"status":"fail","error":str(e)}
    return templates.TemplateResponse("index.html", {"request": request, "api_ok": api_ok, "api_url": API_BASE_URL})

# --- Ingredients ---
@app.get("/ingredients", response_class=HTMLResponse)
async def ingredients_list(request: Request):
    async with httpx.AsyncClient(timeout=5.0) as client:
        r = await client.get(f"{API_BASE_URL}/api/v1/ingredients")
        items = r.json() if r.status_code==200 else []
    return templates.TemplateResponse("ingredients_list.html", {"request": request, "items": items})

@app.get("/ingredients/new", response_class=HTMLResponse)
def ingredients_new(request: Request):
    return templates.TemplateResponse("ingredient_new.html", {"request": request})

@app.post("/ingredients/new")
async def ingredients_create(
    name: str = Form(...),
    brand: str = Form(""),
    calories_kcal: float = Form(...),
    protein_g: float = Form(...),
    fat_g: float = Form(...),
    carbs_g: float = Form(...),
    fiber_g: float = Form(0),
    sodium_mg: float = Form(0),
):
    payload = {
        "name": name, "brand": brand or None, "is_generic": True,
        "nutrients": {
            "calories_kcal": calories_kcal, "protein_g": protein_g, "fat_g": fat_g,
            "carbs_g": carbs_g, "fiber_g": fiber_g, "sodium_mg": sodium_mg
        }
    }
    async with httpx.AsyncClient(timeout=5.0) as client:
        r = await client.post(f"{API_BASE_URL}/api/v1/ingredients", json=payload)
        r.raise_for_status()
    return RedirectResponse("/ingredients", status_code=303)

# --- Recipes ---
@app.get("/recipes/new", response_class=HTMLResponse)
def recipes_new(request: Request):
    return templates.TemplateResponse("recipe_new.html", {"request": request})

@app.post("/recipes/new")
async def recipes_create(
    title: str = Form(...),
    portions: int = Form(...),
    description: str = Form(""),
    ing1_id: int = Form(0), ing1_qty: float = Form(0), ing1_unit: str = Form("g"), ing1_grams: float = Form(0),
    ing2_id: int = Form(0), ing2_qty: float = Form(0), ing2_unit: str = Form("g"), ing2_grams: float = Form(0),
    ing3_id: int = Form(0), ing3_qty: float = Form(0), ing3_unit: str = Form("g"), ing3_grams: float = Form(0),
):
    items = []
    for (iid, qty, unit, grams) in [
        (ing1_id, ing1_qty, ing1_unit, ing1_grams),
        (ing2_id, ing2_qty, ing2_unit, ing2_grams),
        (ing3_id, ing3_qty, ing3_unit, ing3_grams),
    ]:
        if iid and qty:
            items.append({"ingredient_id": int(iid), "qty": float(qty), "unit": unit,
                          "grams": (None if unit.lower()=="g" else (float(grams) if grams else None))})
    payload = {"title": title, "description": (description or None), "portions": int(portions), "items": items}
    async with httpx.AsyncClient(timeout=10.0) as client:
        r = await client.post(f"{API_BASE_URL}/api/v1/recipes", json=payload)
        r.raise_for_status()
        recipe = r.json()
    return RedirectResponse(f"/recipes/{recipe['id']}", status_code=303)

@app.get("/recipes/{recipe_id}", response_class=HTMLResponse)
async def recipe_show(recipe_id: int, request: Request):
    async with httpx.AsyncClient(timeout=5.0) as client:
        r = await client.get(f"{API_BASE_URL}/api/v1/recipes/{recipe_id}")
        if r.status_code != 200:
            return HTMLResponse(f"<h3>Recipe {recipe_id} not found</h3>", status_code=404)
        recipe = r.json()
    return templates.TemplateResponse("recipe_show.html", {"request": request, "recipe": recipe})
