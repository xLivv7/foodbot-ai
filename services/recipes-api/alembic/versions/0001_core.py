"""create core tables"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0001_core"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "ingredients",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("brand", sa.Text(), nullable=True),
        sa.Column("is_generic", sa.Boolean(), nullable=False, server_default=sa.text("true")),
    )
    op.create_table(
        "ingredient_nutrients",
        sa.Column("ingredient_id", sa.BigInteger(), sa.ForeignKey("ingredients.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("calories_kcal", sa.Numeric(10,2), nullable=False),
        sa.Column("protein_g", sa.Numeric(10,2), nullable=False),
        sa.Column("fat_g", sa.Numeric(10,2), nullable=False),
        sa.Column("carbs_g", sa.Numeric(10,2), nullable=False),
        sa.Column("fiber_g", sa.Numeric(10,2), server_default="0"),
        sa.Column("sodium_mg", sa.Numeric(10,2), server_default="0"),
    )
    op.create_table(
        "recipes",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("portions", sa.Integer(), nullable=False),
    )
    op.create_table(
        "recipe_ingredients",
        sa.Column("recipe_id", sa.BigInteger(), sa.ForeignKey("recipes.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("ingredient_id", sa.BigInteger(), sa.ForeignKey("ingredients.id"), primary_key=True),
        sa.Column("qty", sa.Numeric(10,2), nullable=False),
        sa.Column("unit", sa.Text(), nullable=False),
        sa.Column("grams", sa.Numeric(10,2), nullable=True),
        sa.Column("note", sa.Text(), nullable=True),
    )

def downgrade():
    op.drop_table("recipe_ingredients")
    op.drop_table("recipes")
    op.drop_table("ingredient_nutrients")
    op.drop_table("ingredients")
