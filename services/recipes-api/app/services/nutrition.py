from decimal import Decimal
from sqlalchemy.orm import Session
from ..models import Recipe, RecipeIngredient, Ingredient, IngredientNutrients

def _to_float(x: Decimal | float | int | None) -> float:
    return float(x or 0)

def grams_from(qty: Decimal | float, unit: str, grams_field: Decimal | float | None) -> float:
    unit = unit.lower()
    if unit == "g":
        return float(qty)
    # MVP: jeli nie g, bierz z pola grams
    if grams_field is None:
        raise ValueError("For unit != g please provide 'grams'")
    return float(grams_field)

def nutrition_for_ingredient(n: IngredientNutrients, grams: float) -> dict:
    factor = grams / 100.0
    return {
        "calories_kcal": _to_float(n.calories_kcal) * factor,
        "protein_g":     _to_float(n.protein_g)     * factor,
        "fat_g":         _to_float(n.fat_g)         * factor,
        "carbs_g":       _to_float(n.carbs_g)       * factor,
        "fiber_g":       _to_float(n.fiber_g)       * factor,
        "sodium_mg":     _to_float(n.sodium_mg)     * factor,
    }

def sum_nutrition(items: list[dict]) -> dict:
    keys = ["calories_kcal","protein_g","fat_g","carbs_g","fiber_g","sodium_mg"]
    total = {k: 0.0 for k in keys}
    for it in items:
        for k in keys:
            total[k] += it[k]
    return total

def compute_recipe_per_portion(db: Session, recipe: Recipe) -> dict:
    parts = []
    for ri in recipe.items:
        ingr = db.get(Ingredient, ri.ingredient_id)
        if not ingr or not ingr.nutrients:
            continue
        grams = grams_from(ri.qty, ri.unit, ri.grams)
        parts.append(nutrition_for_ingredient(ingr.nutrients, grams))
    total = sum_nutrition(parts)
    portions = max(1, recipe.portions)
    return {k: round(v/portions, 2) for k, v in total.items()}
