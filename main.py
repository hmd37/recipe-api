from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import RecipeCreate, RecipeRead
from crud import create_recipe, get_recipes, get_recipe_by_id, update_recipe, delete_recipe
from database import SessionLocal

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a new recipe
@app.post("/recipes/", response_model=RecipeRead)
def create_new_recipe(recipe: RecipeCreate, db: Session = Depends(get_db)):
    return create_recipe(db=db, recipe=recipe)

# Get all recipes
@app.get("/recipes/", response_model=list[RecipeRead])
def read_recipes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_recipes(db=db, skip=skip, limit=limit)

# Get a recipe by ID
@app.get("/recipes/{recipe_id}", response_model=RecipeRead)
def read_recipe(recipe_id: int, db: Session = Depends(get_db)):
    db_recipe = get_recipe_by_id(db=db, recipe_id=recipe_id)
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return db_recipe

# Update a recipe
@app.put("/recipes/{recipe_id}", response_model=RecipeRead)
def update_recipe_data(recipe_id: int, recipe: RecipeCreate, db: Session = Depends(get_db)):
    db_recipe = update_recipe(db=db, recipe_id=recipe_id, recipe=recipe)
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return db_recipe

# Delete a recipe
@app.delete("/recipes/{recipe_id}", response_model=RecipeRead)
def delete_recipe_data(recipe_id: int, db: Session = Depends(get_db)):
    db_recipe = delete_recipe(db=db, recipe_id=recipe_id)
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return db_recipe
