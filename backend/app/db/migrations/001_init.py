from sqlalchemy import Engine

from app.db.models import Base


# CON-TECH-01, DOM-PDPA-01, IF-HIS-01: สร้างตาราง slots, bookings, audit_logs ตาม plan ข้อ 3
def upgrade(engine: Engine) -> None:
    Base.metadata.create_all(engine)
