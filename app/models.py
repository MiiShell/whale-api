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