from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from ..db import SessionLocal
from .. import models, schemas
from ..services.nutrition import compute_recipe_per_portion

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(prefix="/api/v1/recipes", tags=["recipes"])

@router.post("", response_model=schemas.RecipeOut)
def create_recipe(payload: schemas.RecipeIn, db: Session = Depends(get_db)):
    r = models.Recipe(title=payload.title, description=payload.description, portions=payload.portions)
    db.add(r); db.flush()
    for it in payload.items:
        item = models.RecipeIngredient(
            recipe_id=r.id, ingredient_id=it.ingredient_id, qty=it.qty, unit=it.unit, grams=it.grams, note=it.note
        )
        db.add(item)
    db.commit()
    db.refresh(r)
    per_portion = compute_recipe_per_portion(db, r)
    return schemas.RecipeOut(
        id=r.id, title=r.title, description=r.description, portions=r.portions,
        items=[schemas.RecipeItemOut(**{
            "ingredient_id": i.ingredient_id, "qty": float(i.qty), "unit": i.unit, "grams": float(i.grams) if i.grams is not None else None, "note": i.note
        }) for i in r.items],
        per_portion=per_portion
    )

@router.get("/{recipe_id}", response_model=schemas.RecipeOut)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    r = db.query(models.Recipe).options(joinedload(models.Recipe.items)).filter(models.Recipe.id==recipe_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="recipe not found")
    per_portion = compute_recipe_per_portion(db, r)
    return schemas.RecipeOut(
        id=r.id, title=r.title, description=r.description, portions=r.portions,
        items=[schemas.RecipeItemOut(**{
            "ingredient_id": i.ingredient_id, "qty": float(i.qty), "unit": i.unit, "grams": float(i.grams) if i.grams is not None else None, "note": i.note
        }) for i in r.items],
        per_portion=per_portion
    )
