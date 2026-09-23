from fastapi import FastAPI

from app.slots.router import router as slots_router

# CON-TECH-01: จุดรวม FastAPI app router ของแต่ละ task จะถูกเพิ่มที่นี่ (plan ข้อ 2)
app = FastAPI(title="Booking (SPEC-BKG-001)")

# FR-BKG-01, FR-BKG-06: GET /slots (T-04)
app.include_router(slots_router)
