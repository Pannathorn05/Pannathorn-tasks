from datetime import date, time

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from app.auth.idp import Identity, require_identity
from app.db.session import get_session
from app.slots.service import find_available_slots

router = APIRouter()


# FR-BKG-01: ช่วงเวลา 1 รายการพร้อมที่นั่งคงเหลือ (ชื่อฟิลด์ตามตาราง slots ใน plan ข้อ 3)
class SlotOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    slot_date: date
    start_time: time
    package_code: str
    remaining: int


# FR-BKG-01, FR-BKG-06, IF-IDP-01: GET /slots ตาม plan ข้อ 4 ต้องยืนยันตัวตนก่อน
@router.get("/slots", response_model=list[SlotOut])
def get_slots(
    date_from: date,
    package_code: str,
    session: Session = Depends(get_session),
    identity: Identity = Depends(require_identity),
) -> list:
    return find_available_slots(session, date_from, package_code)
