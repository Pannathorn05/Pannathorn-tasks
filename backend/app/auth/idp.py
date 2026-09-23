import os
from collections.abc import Callable
from dataclasses import dataclass

from fastapi import Depends, HTTPException, Request, status


# IF-IDP-01: ผลยืนยันตัวตนที่ได้จากระบบยืนยันตัวตน actor_id ใช้เป็นผู้เข้าถึงใน audit log (DOM-PDPA-01)
@dataclass(frozen=True)
class Identity:
    actor_id: str


# IF-IDP-01: ตัวตรวจรับ request แล้วคืน Identity หรือ None ถ้าไม่มีผลยืนยันตัวตน
Verifier = Callable[[Request], Identity | None]

# ผู้ใช้ทดสอบของตัวตรวจจำลองตอนพัฒนา (ทีมตัดสินใจ 2569-09-23 ไม่ได้มาจาก spec)
DEV_ACTOR_ID = "dev-user"


# IF-IDP-01: ค่าเริ่มต้นปฏิเสธทุก request เพราะ spec/plan ยังไม่ระบุวิธีเชื่อมระบบยืนยันตัวตนจริง (tasks.md ข้อสังเกต 5)
def reject_all(request: Request) -> Identity | None:
    return None


# IF-IDP-01: ตัวตรวจจำลองเฉพาะตอนพัฒนา เปิดด้วย AUTH_MODE=dev เท่านั้น ห้ามใช้ในระบบจริง
def dev_verifier(request: Request) -> Identity | None:
    return Identity(actor_id=DEV_ACTOR_ID)


# IF-IDP-01: เลือกตัวตรวจตาม AUTH_MODE ตอน test สลับเป็นตัวจำลองผ่าน dependency_overrides
def get_verifier() -> Verifier:
    if os.environ.get("AUTH_MODE") == "dev":
        return dev_verifier
    return reject_all


# IF-IDP-01: ใส่ใน endpoint ด้วย Depends(require_identity) ไม่มีผลยืนยันตัวตนตอบ 401
def require_identity(request: Request, verifier: Verifier = Depends(get_verifier)) -> Identity:
    identity = verifier(request)
    if identity is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="ยังไม่ได้ยืนยันตัวตน")
    return identity
