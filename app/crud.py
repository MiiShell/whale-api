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