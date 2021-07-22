from fastapi import FastAPI, Path, HTTPException, status
from typing import Optional
from fastapi.param_functions import Query
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None

class UpdateItem(BaseModel) :
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None

inventory = {

}

@app.get("/get-item/{item_id}") # Using Paths for descriptions and requirements
def get_item(item_id: int = Path(None ,description="The ID of the item", gt=0)) :
    return inventory[item_id]

@app.get("/get-by-name") # Query Parameters
def get_item(*, name: Optional[str] = None, test: int) :
    for item_id in inventory :
        if inventory[item_id].name == name:
            return inventory[item_id]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@app.get("/get-by-name/{item_id}") # Query Parameters & Path Parameters
def get_item(*, item_id: int, name: Optional[str] = None, test: int) :
    for item_id in inventory :
        if inventory[item_id].name == name:
            return inventory[item_id]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item) :
    if item_id in inventory :
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    inventory[item_id] = item

    return inventory[item_id]

@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem) :
    if item_id not in inventory :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if item.name != None :
        inventory[item_id].name = item.name
    if item.price != None :
        inventory[item_id].price = item.price
    if item.brand != None :
        inventory[item_id].brand = item.brand
    return inventory[item_id]

@app.delete("/delete-item")
def delete_item(item_id: int = Query(..., description="The ID of the item to delete", gt=0)) :
    if item_id not in inventory :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    del inventory[item_id]
    raise HTTPException(status_code=status.HTTP_410_GONE)