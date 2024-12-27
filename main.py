from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db
from schemas import RecipeCreate
from typing import List


app = FastAPI()

@app.post("/recipes/")
def create_recipe(recipe: RecipeCreate, db: Session = Depends(get_db)):
    sql = text("INSERT INTO recipes (name, ingredients, instructions) VALUES (:name, :ingredients, :instructions)")
    result = db.execute(sql, recipe.model_dump())
    db.commit()
    return {"id": result.lastrowid, **recipe.model_dump()}

@app.get("/recipes/", response_model=List[dict])
def get_recipes(db: Session = Depends(get_db)):
    sql = text("SELECT * FROM recipes")
    result = db.execute(sql)
    return [dict(row._mapping) for row in result.fetchall()]

@app.get("/recipes/{recipe_id}")
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    sql = text("SELECT * FROM recipes WHERE id = :recipe_id")
    result = db.execute(sql, {"recipe_id": recipe_id}).fetchone()
    if result is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return dict(result._mapping)

@app.delete("/recipes/{recipe_id}")
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    sql = text("DELETE FROM recipes WHERE id = :recipe_id")
    result = db.execute(sql, {"recipe_id": recipe_id})
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return {"message": "Recipe deleted successfully"}