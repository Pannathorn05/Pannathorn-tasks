# test ของ T-03: จองคิวสำเร็จ
# AC-BKG-01 (FR-BKG-04)
from tests.conftest import AUTH


def test_AC_BKG_01(client, make_slot):
    """AC-BKG-01: ยืนยันตัวตนแล้ว และช่วง 09.00 น. มีที่นั่งว่าง จองแล้วต้องสำเร็จ"""
    slot = make_slot(start="09:00", remaining=1)

    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    assert res.status_code == 201


# ---- test จาก test-cases.md (สร้างด้วย /testcases) ----
from sqlalchemy import select

from app.db.models import Booking, Slot


def test_TC_BKG_01_1_book_last_seat(client, db, make_slot):
    """TC-BKG-01-1 (AC-BKG-01, FR-BKG-04): จองช่วง 09.00 น. ที่ว่าง 1 ที่ แล้วตรวจครบ 3 ส่วนของ Then"""
    # Given ยืนยันตัวตนแล้ว (HN 0001234) และช่วง 09.00 น. มีที่นั่งว่าง 1 ที่
    slot = make_slot(start="09:00", remaining=1)

    # When POST /bookings ด้วย slot_id ของช่วง 09.00 น.
    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    # Then (1) บันทึกสำเร็จ: ตอบ 201 และมีรายการจองของ HN 0001234 ที่ช่วงนั้นในตาราง bookings 1 รายการ
    assert res.status_code == 201
    bookings = db.scalars(
        select(Booking).where(Booking.hn == "0001234", Booking.slot_id == slot.id)
    ).all()
    assert len(bookings) == 1

    # Then (2) หมายเลขคิว: คำตอบมี booking_id และ queue_no ที่ไม่ว่าง
    body = res.json()
    assert body.get("booking_id")
    assert body.get("queue_no")
    # รูปแบบและค่าของ queue_no ยังไม่ตรวจ เพราะรอ Q-02

    # Then (3) remaining ของช่วงนั้นเป็น 0
    db.expire_all()
    assert db.get(Slot, slot.id).remaining == 0


def test_TC_BKG_01_3_no_seat_left(client, db, make_slot):
    """TC-BKG-01-3 (AC-BKG-01 ขอบ, FR-BKG-03, FR-BKG-04): ช่วง 09.00 น. เหลือ 0 ที่ ต้องจองไม่ได้"""
    # Given ยืนยันตัวตนแล้ว และช่วง 09.00 น. มีที่นั่งว่าง 0 ที่ (ขยับจาก 1 ที่ใน Given)
    slot = make_slot(start="09:00", remaining=0, capacity=1)

    # When POST /bookings ด้วย slot_id ของช่วง 09.00 น.
    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    # Then (1) ไม่บันทึก: ตอบ 409 และไม่มีรายการจองใหม่ในตาราง bookings
    assert res.status_code == 409
    assert db.scalars(select(Booking).where(Booking.slot_id == slot.id)).all() == []

    # Then (2) remaining ของช่วงนั้นยังเป็น 0 ไม่ติดลบ
    db.expire_all()
    assert db.get(Slot, slot.id).remaining == 0

    # Then (3) ไม่มี queue_no ในคำตอบ
    assert "queue_no" not in res.json()
    # การเสนอ 3 ช่วงใกล้เคียงตรวจใน test ของ AC-BKG-03


def test_TC_BKG_01_4_not_authenticated(client, db, make_slot):
    """TC-BKG-01-4 (AC-BKG-01 ทางผิด, IF-IDP-01): ยังไม่ยืนยันตัวตน ต้องไม่เกิดการจอง"""
    # Given ยังไม่ยืนยันตัวตน (ไม่ส่ง Authorization) และช่วง 09.00 น. มีที่นั่งว่าง 1 ที่
    slot = make_slot(start="09:00", remaining=1)

    # When POST /bookings ด้วย slot_id ของช่วง 09.00 น.
    res = client.post("/bookings", json={"slot_id": slot.id})

    # Then (1) ไม่มีรายการจองใหม่ในตาราง bookings
    assert db.scalars(select(Booking).where(Booking.slot_id == slot.id)).all() == []

    # Then (2) remaining ของช่วงนั้นยังเป็น 1
    db.expire_all()
    assert db.get(Slot, slot.id).remaining == 1

    # Then (3) รหัสตอบกลับและข้อความที่แสดง: spec ไม่ได้บอก จึงยังไม่ตรวจ (ไม่ assert res.status_code)
