from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import config

# エンジン生成
DATABASE_URL = config.DATABASE_URL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


# FastAPI依存性注入用
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
