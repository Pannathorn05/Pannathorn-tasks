import os


# CON-TECH-01: ระบบจริงชี้ DATABASE_URL ไป PostgreSQL ตอน test ใช้ SQLite ได้โดยไม่แก้โค้ด (plan ข้อ 2)
def get_database_url() -> str:
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError("ยังไม่ได้ตั้งค่าตัวแปร DATABASE_URL")
    return url
