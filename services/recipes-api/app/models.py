from sqlalchemy import Column, BigInteger, Text, Boolean, Integer, Numeric, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .db import Base

class Ingredient(Base):
    __tablename__ = "ingredients"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    brand: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_generic: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    nutrients: Mapped["IngredientNutrients"] = relationship(back_populates="ingredient", uselist=False)

class IngredientNutrients(Base):
    __tablename__ = "ingredient_nutrients"
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id", ondelete="CASCADE"), primary_key=True)
    calories_kcal: Mapped[float] = mapped_column(Numeric(10,2), nullable=False)
    protein_g:     Mapped[float] = mapped_column(Numeric(10,2), nullable=False)
    fat_g:         Mapped[float] = mapped_column(Numeric(10,2), nullable=False)
    carbs_g:       Mapped[float] = mapped_column(Numeric(10,2), nullable=False)
    fiber_g:       Mapped[float] = mapped_column(Numeric(10,2), default=0)
    sodium_mg:     Mapped[float] = mapped_column(Numeric(10,2), default=0)

    ingredient: Mapped["Ingredient"] = relationship(back_populates="nutrients")

class Recipe(Base):
    __tablename__ = "recipes"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    portions: Mapped[int] = mapped_column(Integer, nullable=False)

    items: Mapped[list["RecipeIngredient"]] = relationship(back_populates="recipe", cascade="all, delete-orphan")

class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id", ondelete="CASCADE"), primary_key=True)
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id"), primary_key=True)
    qty: Mapped[float] = mapped_column(Numeric(10,2), nullable=False)    # ilo w unit
    unit: Mapped[str] = mapped_column(Text, nullable=False)               # "g","ml","szt"
    grams: Mapped[float | None] = mapped_column(Numeric(10,2), nullable=True)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)

    recipe: Mapped["Recipe"] = relationship(back_populates="items")
    ingredient: Mapped["Ingredient"] = relationship()
