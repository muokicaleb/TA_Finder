from fastapi import FastAPI
from pydantic import BaseModel
from .core.core import run

class Item(BaseModel):
    twitterUser: str
    email: str 

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/tafinder")
async def get_ta(item: Item):
    
    return run(item)