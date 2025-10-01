from pydantic import BaseModel, Field
from typing import Optional, List

# ------ Ingredients ------
class IngredientNutrientsIn(BaseModel):
    calories_kcal: float
    protein_g:     float
    fat_g:         float
    carbs_g:       float
    fiber_g:       float = 0
    sodium_mg:     float = 0

class IngredientIn(BaseModel):
    name: str
    brand: Optional[str] = None
    is_generic: bool = True
    nutrients: IngredientNutrientsIn

class IngredientOut(BaseModel):
    id: int
    name: str
    brand: Optional[str]
    is_generic: bool
    class Config:
        from_attributes = True

# ------ Recipes ------
class RecipeItemIn(BaseModel):
    ingredient_id: int
    qty: float
    unit: str
    grams: Optional[float] = None
    note: Optional[str] = None

class RecipeIn(BaseModel):
    title: str
    description: Optional[str] = None
    portions: int = Field(gt=0)
    items: List[RecipeItemIn]

class RecipeItemOut(BaseModel):
    ingredient_id: int
    qty: float
    unit: str
    grams: Optional[float]
    note: Optional[str] = None

class NutritionOut(BaseModel):
    calories_kcal: float
    protein_g: float
    fat_g: float
    carbs_g: float
    fiber_g: float
    sodium_mg: float

class RecipeOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    portions: int
    items: List[RecipeItemOut]
    per_portion: NutritionOut
