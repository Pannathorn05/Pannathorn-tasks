from datetime import date, datetime, time

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Time
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


# FR-BKG-01, FR-BKG-06, ASM-01: ช่วงเวลาต่อแพ็กเกจ พร้อมโควตา (capacity) และที่นั่งคงเหลือ (remaining)
class Slot(Base):
    __tablename__ = "slots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slot_date: Mapped[date] = mapped_column(Date)
    start_time: Mapped[time] = mapped_column(Time)
    package_code: Mapped[str] = mapped_column(String)
    capacity: Mapped[int] = mapped_column(Integer)
    remaining: Mapped[int] = mapped_column(Integer)


# FR-BKG-02, FR-BKG-04, IF-HIS-01: การจองอ้างอิงผู้รับบริการด้วย hn เท่านั้น ไม่มีคอลัมน์เลขบัตรประชาชน
class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    hn: Mapped[str] = mapped_column(String)
    slot_id: Mapped[int] = mapped_column(ForeignKey("slots.id"))
    booking_date: Mapped[date] = mapped_column(Date)
    # รูปแบบและวิธีออกเลขคิวรอ Q-02 จึงยังว่างได้ (plan ข้อ 3)
    queue_no: Mapped[str | None] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


# DOM-PDPA-01: audit log ผู้เข้าถึง เวลา และรหัสผู้รับบริการ (hn)
class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    actor_id: Mapped[str] = mapped_column(String)
    action: Mapped[str] = mapped_column(String)
    hn: Mapped[str] = mapped_column(String)
    accessed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
