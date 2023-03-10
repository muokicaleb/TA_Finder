from fastapi import FastAPI
from pydantic import BaseModel
from .core.core import run, get_ta_result

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

@app.get("/taresults/{transaction_id}")
async def read_user_item(transaction_id: str):
    return get_ta_result(transaction_id)