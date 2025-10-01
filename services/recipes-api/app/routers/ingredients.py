from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ..db import SessionLocal
from .. import models, schemas

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(prefix="/api/v1/ingredients", tags=["ingredients"])

@router.post("", response_model=schemas.IngredientOut)
def create_ingredient(payload: schemas.IngredientIn, db: Session = Depends(get_db)):
    ing = models.Ingredient(name=payload.name, brand=payload.brand, is_generic=payload.is_generic)
    db.add(ing); db.flush()
    nut = models.IngredientNutrients(
        ingredient_id=ing.id,
        calories_kcal=payload.nutrients.calories_kcal,
        protein_g=payload.nutrients.protein_g,
        fat_g=payload.nutrients.fat_g,
        carbs_g=payload.nutrients.carbs_g,
        fiber_g=payload.nutrients.fiber_g,
        sodium_mg=payload.nutrients.sodium_mg,
    )
    db.add(nut); db.commit(); db.refresh(ing)
    return ing

@router.get("", response_model=List[schemas.IngredientOut])
def list_ingredients(db: Session = Depends(get_db)):
    return db.query(models.Ingredient).order_by(models.Ingredient.id.desc()).all()
