import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from characters_db import characters_db

app = FastAPI()


@app.get(
    "/characters",
    tags=["Characters"],
    summary="Get all characters"
)
def get_characters():
    return characters_db


@app.get(
    "/characters/{character_id}",
    tags=["Characters"],
    summary="Get character"
)
def get_character_by_id(character_id: int):
    for character in characters_db:
        if character["id"] == character_id:
            return character
    raise HTTPException(status_code=404, detail="Character not found")


class NewCharacter(BaseModel):
    name: str
    hp: int


@app.post(
    "/characters"
)
def create_characters(new_character: NewCharacter):
    characters_db.append({
        "id": len(characters_db) + 1,
        "name": new_character.name,
        "hp": new_character.hp
    })
    return {"success": True, "message": "New Character created!"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
