from app.database import SessionLocal
from app.models import WhalePosition
import time

# Mock function to simulate whale data
def fetch_and_store_mock():
    db = SessionLocal()
    example = WhalePosition(
        user="0x3fd4444154242720c0d0c61c74a240d90c127d33",
        symbol="ETH",
        position_size=12700,
        entry_price=1611.62,
        liq_price=527.2521,
        position_value_usd=21003260,
        position_action=2,
        create_time=int(time.time() * 1000)
    )
    db.add(example)
    db.commit()
    db.close()

if __name__ == "__main__":
    fetch_and_store_mock()

