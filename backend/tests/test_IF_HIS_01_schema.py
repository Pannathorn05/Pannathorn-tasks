import importlib

from sqlalchemy import Engine, inspect

# ชื่อโมดูลขึ้นต้นด้วยตัวเลข จึง import ผ่าน importlib
migration = importlib.import_module("app.db.migrations.001_init")


# T-02 / CON-TECH-01: upgrade(engine) สร้างครบ 3 ตารางตาม plan ข้อ 3
def test_T02_upgrade_creates_three_tables(engine: Engine) -> None:
    migration.upgrade(engine)
    assert set(inspect(engine).get_table_names()) == {"slots", "bookings", "audit_logs"}


# T-02 / IF-HIS-01: ตาราง bookings อ้างอิงด้วย hn และไม่มีคอลัมน์เลขบัตรประชาชน
def test_IF_HIS_01_bookings_has_hn_and_no_national_id(engine: Engine) -> None:
    migration.upgrade(engine)
    columns = {c["name"] for c in inspect(engine).get_columns("bookings")}
    assert columns == {"id", "hn", "slot_id", "booking_date", "queue_no", "status", "created_at"}
    assert not any("national" in name or "citizen" in name or "id_card" in name for name in columns)


# T-02 / FR-BKG-04: queue_no ว่างได้ เพราะรูปแบบเลขคิวรอ Q-02
def test_T02_queue_no_is_nullable(engine: Engine) -> None:
    migration.upgrade(engine)
    queue_no = next(c for c in inspect(engine).get_columns("bookings") if c["name"] == "queue_no")
    assert queue_no["nullable"] is True


# T-02 / DOM-PDPA-01: audit_logs มีผู้เข้าถึง เวลา และรหัสผู้รับบริการ
def test_DOM_PDPA_01_audit_logs_columns(engine: Engine) -> None:
    migration.upgrade(engine)
    columns = {c["name"] for c in inspect(engine).get_columns("audit_logs")}
    assert {"actor_id", "accessed_at", "hn"} <= columns


# T-02 / FR-BKG-01, ASM-01: slots มีโควตาและที่นั่งคงเหลือต่อแพ็กเกจ
def test_T02_slots_columns(engine: Engine) -> None:
    migration.upgrade(engine)
    columns = {c["name"] for c in inspect(engine).get_columns("slots")}
    assert columns == {"id", "slot_date", "start_time", "package_code", "capacity", "remaining"}
