from pydantic import BaseModel


class RecipeCreate(BaseModel):
    name: str
    ingredients: str
    instructions: str
