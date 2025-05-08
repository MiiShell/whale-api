from fastapi import FastAPI, Query
from app import models, database, crud
from typing import List

app = FastAPI()
database.init_db()

@app.get("/api/whales")
def get_whale_positions(symbol: str = None, action: int = None, since: int = None, limit: int = 50):
    data = crud.fetch_positions(symbol, action, since, limit)
    return {"code": "0", "msg": "success", "data": data}
