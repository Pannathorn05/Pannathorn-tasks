from collections.abc import Iterator
from functools import lru_cache

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import get_database_url


# CON-TECH-01: สร้าง engine จาก DATABASE_URL ครั้งเดียว (ต่อฐานข้อมูลจริงเมื่อใช้งานครั้งแรก)
@lru_cache
def get_engine() -> Engine:
    return create_engine(get_database_url())


# CON-TECH-01: ให้ router ขอ session ผ่าน Depends(get_session) ตอน test สลับเป็น SQLite ได้
def get_session() -> Iterator[Session]:
    with sessionmaker(bind=get_engine())() as session:
        yield session
