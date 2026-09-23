from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.auth.idp import Identity, get_verifier
from app.db.session import get_session
from app.main import app

# test ใช้ SQLite ในหน่วยความจำแทน PostgreSQL เพราะ Codespace ไม่มีเครื่องฐานข้อมูล (plan ข้อ 2)
TEST_DATABASE_URL = "sqlite:///:memory:"


# CON-TECH-01: engine SQLite ในหน่วยความจำ แทน PostgreSQL ตอน test (plan ข้อ 2)
@pytest.fixture
def engine() -> Iterator[Engine]:
    # StaticPool ให้ทุก connection ใช้ฐานข้อมูลในหน่วยความจำก้อนเดียวกัน
    eng = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    yield eng
    eng.dispose()


# CON-TECH-01: สลับ get_session ของ app ให้ใช้ SQLite ตอน test โดยไม่แก้โค้ดใน app
@pytest.fixture
def db_session(engine: Engine) -> Iterator[Session]:
    SessionLocal = sessionmaker(bind=engine)

    def override_get_session() -> Iterator[Session]:
        with SessionLocal() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session
    with SessionLocal() as session:
        yield session
    app.dependency_overrides.pop(get_session, None)


TEST_ACTOR_ID = "test-actor"


# IF-IDP-01: client ของ app จริงที่ผ่านการยืนยันตัวตนแล้ว (ตัวตรวจจำลอง) และใช้ฐานข้อมูล SQLite ของ test
@pytest.fixture
def client(db_session: Session) -> Iterator[TestClient]:
    app.dependency_overrides[get_verifier] = lambda: lambda request: Identity(actor_id=TEST_ACTOR_ID)
    yield TestClient(app)
    app.dependency_overrides.pop(get_verifier, None)
