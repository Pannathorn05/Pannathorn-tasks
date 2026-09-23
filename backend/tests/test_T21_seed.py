import importlib
from datetime import date

from fastapi.testclient import TestClient
from sqlalchemy import Engine
from sqlalchemy.orm import Session

from app.db.seed import DEMO_DAYS, DEMO_TIMES, seed

migration = importlib.import_module("app.db.migrations.001_init")

TODAY = date(2026, 10, 1)


# T-21 / FR-BKG-01: ใส่ข้อมูลตัวอย่างแล้ว GET /slots ของแพ็กเกจตัวอย่างมีช่วงว่างให้หน้าจอแสดง
def test_T21_seed_makes_slots_visible(engine: Engine, db_session: Session, client: TestClient) -> None:
    migration.upgrade(engine)
    added = seed(db_session, TODAY)

    assert added == DEMO_DAYS * sum(len(h) for h in DEMO_TIMES.values())
    for package_code in DEMO_TIMES:
        res = client.get("/slots", params={"date_from": TODAY.isoformat(), "package_code": package_code})
        assert res.status_code == 200
        assert len(res.json()) > 0


# T-21: รันซ้ำไม่ใส่ข้อมูลซ้ำ
def test_T21_seed_twice_does_not_duplicate(engine: Engine, db_session: Session) -> None:
    migration.upgrade(engine)
    seed(db_session, TODAY)
    assert seed(db_session, TODAY) == 0
