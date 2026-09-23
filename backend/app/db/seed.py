"""ใส่ข้อมูลช่วงเวลาตัวอย่างสำหรับทดลองเปิดระบบ (T-21) ข้อมูลนี้ไม่ได้มาจาก spec

รัน: cd backend && DATABASE_URL=sqlite:///./dev.db python -m app.db.seed
"""

import importlib
from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.models import Slot
from app.db.session import get_engine

migration = importlib.import_module("app.db.migrations.001_init")

# รหัสแพ็กเกจตัวอย่าง ต้องตรงกับรายการแพ็กเกจใน frontend/src/App.jsx (tasks.md ข้อสังเกต 7)
DEMO_TIMES = {"DEMO-A": [9, 10, 11], "DEMO-B": [13, 14]}
DEMO_DAYS = 7
DEMO_CAPACITY = 5


# FR-BKG-01, ASM-01: ใส่ช่วงเวลาตัวอย่าง 7 วันนับจาก today ถ้าตาราง slots ยังว่าง คืนจำนวนที่ใส่
def seed(session: Session, today: date) -> int:
    if session.scalar(select(func.count()).select_from(Slot)):
        return 0
    added = 0
    for offset in range(DEMO_DAYS):
        for package_code, hours in DEMO_TIMES.items():
            for i, hour in enumerate(hours):
                session.add(
                    Slot(
                        slot_date=today + timedelta(days=offset),
                        start_time=time(hour, 0),
                        package_code=package_code,
                        capacity=DEMO_CAPACITY,
                        # บางช่วงเป็น 0 เพื่อให้เห็นว่าช่วงเต็มไม่ถูกแสดง
                        remaining=(offset + i) % (DEMO_CAPACITY + 1),
                    )
                )
                added += 1
    session.commit()
    return added


# ASM-02: "วันนี้" ตามเขตเวลา Asia/Bangkok
def main() -> None:
    engine = get_engine()
    migration.upgrade(engine)
    with Session(engine) as session:
        added = seed(session, datetime.now(ZoneInfo("Asia/Bangkok")).date())
    print(f"ใส่ข้อมูลช่วงเวลาตัวอย่าง {added} รายการ" if added else "มีข้อมูลอยู่แล้ว ไม่ได้ใส่เพิ่ม")


if __name__ == "__main__":
    main()
