from datetime import date, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Slot

# FR-BKG-01: "ภายใน 30 วันข้างหน้า" = date_from ถึง date_from+29 (ทีมตัดสินใจ 2569-09-23)
WINDOW_DAYS = 30


# FR-BKG-01, FR-BKG-06: ช่วงที่ว่าง (remaining > 0 ตามที่ทีมตัดสินใจ) ของแพ็กเกจที่เลือก ภายใน 30 วัน
def find_available_slots(session: Session, date_from: date, package_code: str) -> list[Slot]:
    date_to = date_from + timedelta(days=WINDOW_DAYS - 1)
    stmt = (
        select(Slot)
        .where(
            Slot.package_code == package_code,
            Slot.slot_date >= date_from,
            Slot.slot_date <= date_to,
            Slot.remaining > 0,
        )
        .order_by(Slot.slot_date, Slot.start_time)
    )
    return list(session.scalars(stmt))
