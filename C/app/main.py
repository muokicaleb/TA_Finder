from fastapi import FastAPI
from pydantic import BaseModel
from .core.core import multiple_query_similar

class Item(BaseModel):
    sentences: list[str]   


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/semanticsearch")
async def get_ta(item: Item):
    
    return {"topics":multiple_query_similar(item.sentences)}