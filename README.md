# whale-api


### Project Structure
# crypto-whale-api/
# ├── app/
# │   ├── main.py
# │   ├── models.py
# │   ├── database.py
# │   ├── schemas.py
# │   ├── crud.py
# │   └── fetcher.py
# ├── Dockerfile
# ├── docker-compose.yml
# ├── requirements.txt

# ==== app/main.py ====
from fastapi import FastAPI, Query
from app import models, database, crud
from typing import List

app = FastAPI()
database.init_db()

@app.get("/api/whales")
def get_whale_positions(symbol: str = None, action: int = None, since: int = None, limit: int = 50):
    data = crud.fetch_positions(symbol, action, since, limit)
    return {"code": "0", "msg": "success", "data": data}


# ==== app/models.py ====
from sqlalchemy import Column, String, Float, Integer, BigInteger
from app.database import Base

class WhalePosition(Base):
    __tablename__ = "whale_positions"
    id = Column(Integer, primary_key=True, index=True)
    user = Column(String, index=True)
    symbol = Column(String)
    position_size = Column(Float)
    entry_price = Column(Float)
    liq_price = Column(Float)
    position_value_usd = Column(Float)
    position_action = Column(Integer)
    create_time = Column(BigInteger)


# ==== app/database.py ====
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./whales.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    Base.metadata.create_all(bind=engine)


# ==== app/crud.py ====
from app.database import SessionLocal
from app.models import WhalePosition

def fetch_positions(symbol=None, action=None, since=None, limit=50):
    db = SessionLocal()
    query = db.query(WhalePosition)
    if symbol:
        query = query.filter(WhalePosition.symbol == symbol)
    if action:
        query = query.filter(WhalePosition.position_action == action)
    if since:
        query = query.filter(WhalePosition.create_time >= since)
    results = query.order_by(WhalePosition.create_time.desc()).limit(limit).all()
    db.close()
    return [row.__dict__ for row in results]


# ==== Dockerfile ====
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


# ==== docker-compose.yml ====
version: '3.9'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    restart: unless-stopped


# ==== requirements.txt ====
fastapi
uvicorn
sqlalchemy
requests
web3
