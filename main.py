from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str

app = FastAPI()


@app.post("/image/")
async def create_item(item: Item):
  return item.name