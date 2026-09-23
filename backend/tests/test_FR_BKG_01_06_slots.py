import importlib
from datetime import date, time, timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine
from sqlalchemy.orm import Session

from app.db.models import Slot
from app.main import app

migration = importlib.import_module("app.db.migrations.001_init")

DATE_FROM = date(2026, 10, 1)


@pytest.fixture
def slots(engine: Engine, db_session: Session) -> None:
    migration.upgrade(engine)

    def add(days: int, hour: int, package: str, remaining: int) -> None:
        db_session.add(
            Slot(
                slot_date=DATE_FROM + timedelta(days=days),
                start_time=time(hour, 0),
                package_code=package,
                capacity=5,
                remaining=remaining,
            )
        )

    add(0, 10, "PKG-A", 2)   # วันแรก 10.00 อยู่ในช่วง
    add(0, 9, "PKG-A", 3)    # วันแรก 09.00 อยู่ในช่วง
    add(29, 9, "PKG-A", 1)   # วันที่ 30 (date_from+29) อยู่ในช่วง
    add(30, 9, "PKG-A", 4)   # date_from+30 เกิน 30 วัน
    add(-1, 9, "PKG-A", 4)   # ก่อน date_from
    add(1, 9, "PKG-A", 0)    # เต็มแล้ว ไม่ว่าง
    add(1, 13, "PKG-B", 5)   # แพ็กเกจอื่น
    db_session.commit()


def get(client: TestClient, package: str):
    return client.get("/slots", params={"date_from": DATE_FROM.isoformat(), "package_code": package})


# T-04 / FR-BKG-01: คืนเฉพาะช่วงว่างภายใน date_from ถึง date_from+29 พร้อม remaining เรียงตามวันและเวลา
def test_FR_BKG_01_slots_within_30_days_with_remaining(client: TestClient, slots: None) -> None:
    res = get(client, "PKG-A")

    assert res.status_code == 200
    body = res.json()
    assert [(s["slot_date"], s["start_time"], s["remaining"]) for s in body] == [
        ("2026-10-01", "09:00:00", 3),
        ("2026-10-01", "10:00:00", 2),
        ("2026-10-30", "09:00:00", 1),
    ]


# T-04 / FR-BKG-01: ช่วงที่เหลือ 0 ที่ไม่ถูกคืน (ทีมตัดสินใจ "ที่ว่าง" = remaining > 0)
def test_FR_BKG_01_full_slot_not_returned(client: TestClient, slots: None) -> None:
    body = get(client, "PKG-A").json()
    assert all(s["remaining"] > 0 for s in body)
    assert "2026-10-02" not in {s["slot_date"] for s in body}


# T-04 / FR-BKG-06: เปลี่ยน package_code แล้วได้ช่วงของแพ็กเกจนั้น
def test_FR_BKG_06_slots_by_package(client: TestClient, slots: None) -> None:
    body = get(client, "PKG-B").json()
    assert [(s["package_code"], s["slot_date"], s["start_time"]) for s in body] == [
        ("PKG-B", "2026-10-02", "13:00:00"),
    ]


# T-04 / IF-IDP-01: GET /slots ไม่มีผลยืนยันตัวตนถูกปฏิเสธ
def test_IF_IDP_01_slots_requires_identity(db_session: Session, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("AUTH_MODE", raising=False)
    res = TestClient(app).get("/slots", params={"date_from": DATE_FROM.isoformat(), "package_code": "PKG-A"})
    assert res.status_code == 401
