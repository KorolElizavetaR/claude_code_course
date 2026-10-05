
from fastapi import FastAPI, HTTPException
from fastapi_pagination import Page, add_pagination, paginate

from dto.ItemDto import ItemDto
from mapper.ItemMapper import ItemMapper
from model.Item import Item

app = FastAPI()
items: list = []
    
@app.post("/item")
def create_item(dto: ItemDto) -> list:
    storedItem = ItemMapper.dto_to_entity(dto)
    items.append(storedItem)
    return items

@app.get("/items", response_model=Page[Item])
def get_items():
    return paginate(items)

@app.get("/items/{item_id}")
def get_item(item_id: int)->Item:
    for item in items:
        if item.id == item_id:
            return item 
    raise HTTPException(status_code=404, detail="Item not found")

add_pagination(app)