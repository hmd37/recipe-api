from sqlalchemy.orm import Session
from models import Recipe
from schemas import RecipeCreate, RecipeRead

# Create a new recipe
def create_recipe(db: Session, recipe: RecipeCreate):
    db_recipe = Recipe(
        title=recipe.title,
        description=recipe.description,
        ingredients=recipe.ingredients,
        instructions=recipe.instructions,
    )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

# Get all recipes
def get_recipes(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Recipe).offset(skip).limit(limit).all()

# Get a recipe by ID
def get_recipe_by_id(db: Session, recipe_id: int):
    return db.query(Recipe).filter(Recipe.id == recipe_id).first()

# Update a recipe
def update_recipe(db: Session, recipe_id: int, recipe: RecipeCreate):
    db_recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if db_recipe:
        db_recipe.title = recipe.title
        db_recipe.description = recipe.description
        db_recipe.ingredients = recipe.ingredients
        db_recipe.instructions = recipe.instructions
        db.commit()
        db.refresh(db_recipe)
    return db_recipe

# Delete a recipe
def delete_recipe(db: Session, recipe_id: int):
    db_recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if db_recipe:
        db.delete(db_recipe)
        db.commit()
    return db_recipe
