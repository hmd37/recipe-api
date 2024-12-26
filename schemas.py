from pydantic import BaseModel
from typing import Optional

# Base schema for Recipe (shared properties)
class RecipeBase(BaseModel):
    title: str
    description: Optional[str] = None
    ingredients: str
    instructions: str

# Schema for creating a recipe
class RecipeCreate(RecipeBase):
    pass

# Schema for reading a recipe (includes id)
class RecipeRead(RecipeBase):
    id: int

    class Config:
        orm_mode = True
