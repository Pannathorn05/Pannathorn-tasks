# Prompt log

บันทึกทุกครั้งที่ใช้ AI กับ repo นี้ เขียนต่อท้ายเรื่อย ๆ ไม่ต้องลบของเก่า

---

## 2569-09-23 15:21 คำสั่ง: /tasks

- เครื่องมือ: Claude Code (VS Code ใน Codespaces)
- คำสั่ง: `/tasks specs/001-booking/spec.md`
- อ่าน: specs/001-booking/spec.md (Draft v2), specs/001-booking/plan.md (plan v1), AGENTS.md
- ผลลัพธ์: specs/001-booking/tasks.md

### สรุปผลลัพธ์

- มีทั้งหมด 21 task (T-01 ถึง T-21) แบ่งเป็นพร้อมทำ 14 task, รอ Q-02 1 task (T-12 ออกหมายเลขคิว) และรอทีมตัดสินใจ 6 task (T-06, T-07, T-10, T-15, T-20, T-21)
- AC-BKG-01 ถึง AC-BKG-06 มี task ตรวจครบทุกตัว และ Constraint ทั้ง 5 ข้อมี task รองรับครบ
- ลำดับงานคือหลังบ้าน (model -> API -> แจ้งเตือน -> audit/HIS -> ตรวจ PostgreSQL และความเร็ว) ส่วนหน้าจอ T-17 เริ่มได้ทันทีด้วย API จำลอง และ T-21 ต่อหน้าจอกับ API จริงเป็นงานสุดท้าย

### สิ่งที่ AI ไม่ได้เดา และบันทึกเป็นข้อสังเกตใน tasks.md (ไม่ได้สร้าง Q ID ใหม่)

1. plan ข้อ 4 ไม่ได้กำหนด response ของ POST /bookings เมื่อถูกปฏิเสธเพราะจองซ้ำ (FR-BKG-02)
2. FR-BKG-03 ยังไม่ได้นิยามว่า "ใกล้ที่สุด" วัดอย่างไร ถ้าระยะเท่ากันจะทำอย่างไร ต้องเป็นแพ็กเกจเดียวกันหรือไม่ และถ้าช่วงว่างไม่ถึง 3 ช่วงจะทำอย่างไร
3. plan เลือก Redis แต่ requirements.txt ยังไม่มี library ของ Redis
4. ยังไม่มีเครื่อง PostgreSQL สำหรับตรวจ CON-TECH-01
5. ยังไม่ได้ระบุวิธีเชื่อมระบบยืนยันตัวตนและ HIS จริง
6. FR-BKG-06 ยังไม่มี AC ส่วน NFR-SEC-01 และ NFR-USE-01 ไม่มีใน plan จึงยังไม่มี task
7. ยังไม่มี API ที่คืนรายการแพ็กเกจ
8. ยังไม่ได้ระบุวิธีเก็บ audit log ให้ครบ 1 ปี

### คำตอบของทีม

- (ยังไม่ได้ตอบ)

---

## 2569-09-23 คำสั่ง: /implement T-01

- เครื่องมือ: Claude Code (VS Code ใน Codespaces)
- คำสั่ง: `/implement T-01 specs/001-booking/tasks.md`
- task: T-01 ตั้งโครง FastAPI app, config และ session ฐานข้อมูล (รองรับ CON-TECH-01)

### ไฟล์ที่สร้างหรือแก้

- สร้าง `backend/app/main.py`, `backend/app/config.py`, `backend/app/db/session.py`, `backend/tests/conftest.py` (ตรงกับช่อง "ไฟล์ที่แตะ")
- สร้าง `backend/tests/test_T01_setup.py` เพิ่ม (ไม่อยู่ในช่อง "ไฟล์ที่แตะ" AI ถามก่อน และทีมอนุญาต)
- แก้ `specs/001-booking/tasks.md` เปลี่ยนสถานะ T-01 เป็น "เสร็จ รอทีมตรวจ"

### ผล test (`cd backend && pytest -v`)

```
tests/test_T01_setup.py::test_T01_config_reads_database_url PASSED
tests/test_T01_setup.py::test_T01_config_requires_database_url PASSED
tests/test_T01_setup.py::test_T01_db_session_is_sqlite_in_memory PASSED
tests/test_T01_setup.py::test_T01_app_created PASSED
4 passed in 0.05s
```

### คำถามที่ AI ถาม และคำตอบของทีม

1. ช่อง "ไฟล์ที่แตะ" ของ T-01 ไม่มีไฟล์ test แต่คำสั่ง /implement ให้เขียน test ยืนยัน "เสร็จเมื่อ" -> ทีมตอบให้เพิ่ม `backend/tests/test_T01_setup.py`

### สิ่งที่ AI เกือบต้องเดาแต่ไม่ได้เดา

- ค่าเริ่มต้นของ `DATABASE_URL`: spec และ plan ไม่ได้กำหนด จึงไม่ได้ตั้งค่าเริ่มต้นไว้ ถ้าไม่ได้ตั้งตัวแปรนี้ `get_database_url()` จะแจ้ง error แทนการเดาค่าเอง

---

## 2569-09-23 แก้งาน T-01 รอบที่ 2 (ตรวจ checklist 5 ข้อ)

- เครื่องมือ: Claude Code (VS Code ใน Codespaces)
- แก้อะไร: เพิ่มคอมเมนต์อ้าง ID 1 บรรทัดเหนือ fixture `engine` และ `db_session` ใน `backend/tests/conftest.py` และเหนือ `test_T01_config_requires_database_url` กับ `test_T01_app_created` ใน `backend/tests/test_T01_setup.py` ไม่ได้แก้ตัวโค้ด
- เพราะอะไร: checklist ข้อ 5 พบว่า 4 ฟังก์ชันนี้ยังไม่มีคอมเมนต์อ้าง FR/CON ผิดกติกาข้อ 7 ใน AGENTS.md
- ผล test หลังแก้: 4 passed

---

## 2569-09-23 แก้ tasks.md รอบที่ 3 (ใส่ไฟล์ test ของ T-01 กลับ)

- เครื่องมือ: Claude Code (VS Code ใน Codespaces)
- ไฟล์: specs/001-booking/tasks.md
- แก้อะไร: ใส่ `backend/tests/test_T01_setup.py` กลับเข้าช่อง "ไฟล์ที่แตะ" ของ T-01 (หลัง "แก้ tasks.md รอบที่ 1" ช่องนี้ถูกย้อนกลับเป็นแบบเดิม 1 ครั้ง)
- เพราะอะไร: checklist ข้อ 1 พบว่าไฟล์ test ยังอยู่จริงแต่ไม่อยู่ในช่อง "ไฟล์ที่แตะ" ทีมเลือกใส่กลับแทนการลบไฟล์ เพราะ (1) T-01 ต้องมี test ยืนยัน "เสร็จเมื่อ" (2) ให้ตรงกับบันทึกรอบที่ 1 (3) เป็นรูปแบบเดียวกับ T-02, T-11, T-14 ที่มีไฟล์ test อยู่ในช่องแล้ว
- ไม่ได้แก้ task อื่น

---

## 2569-09-23 คำสั่ง: /implement T-17

- เครื่องมือ: Claude Code (VS Code ใน Codespaces)
- คำสั่ง: `/implement T-17 specs/001-booking/tasks.md` (ขั้นเสริม: task หน้าจอ React + Tailwind)
- task: T-17 สร้างหน้าเลือกแพ็กเกจและช่วงเวลา (SlotPicker) รองรับ FR-BKG-01, FR-BKG-06

### ไฟล์ที่สร้างหรือแก้ (ตรงกับช่อง "ไฟล์ที่แตะ")

- สร้าง `frontend/src/pages/SlotPicker.jsx`
- สร้าง `frontend/src/__tests__/FR-BKG-06.test.jsx`
- แก้ `frontend/src/App.jsx` ให้แสดง SlotPicker ด้วย client จำลอง (ข้อมูล DEMO-A, DEMO-B ไม่ได้มาจาก spec)
- แก้ `specs/001-booking/tasks.md` เปลี่ยนสถานะ T-17 เป็น "เสร็จ รอทีมตรวจ"

### ผล test (`cd frontend && npx vitest run --reporter=verbose`)

```
✓ FR-BKG-06.test.jsx > FR-BKG-01 แสดงช่วงเวลาพร้อมที่นั่งคงเหลือ
✓ FR-BKG-06.test.jsx > FR-BKG-06 เปลี่ยนแพ็กเกจแล้วโหลดช่วงเวลาใหม่
✓ setup.test.jsx > โครงหน้าจอเปิดได้
Test Files 2 passed (2) | Tests 3 passed (3)
```

- `setup.test.jsx` (test เดิมของโครงรายวิชา) ขึ้น warning `act(...)` เพราะตอนนี้ App โหลดช่วงเวลาแบบ async แต่ยังผ่าน ไม่ได้แก้เพราะไฟล์นี้ไม่อยู่ในช่อง "ไฟล์ที่แตะ"
- `npm run build` ผ่าน (ลบโฟลเดอร์ `dist/` ทิ้งหลัง build เพราะ .gitignore ไม่ได้กันไว้)

### สิ่งที่ AI เกือบต้องเดาแต่ไม่ได้เดา

- รายการแพ็กเกจ: plan ไม่มี API จึงรับเป็น props ตามข้อสังเกต 7 ใน tasks.md และแสดงเป็นรหัสแพ็กเกจอย่างเดียว ไม่ได้ตั้งชื่อหรือรายละเอียดแพ็กเกจเอง
- ชื่อฟิลด์ของ GET /slots: plan ข้อ 4 บอกแค่ "รายการช่วงเวลา + ที่นั่งคงเหลือ" จึงใช้ชื่อฟิลด์ตามตาราง slots ใน plan ข้อ 3 (`id`, `slot_date`, `start_time`, `package_code`, `remaining`) ทีมควรยืนยันตอนทำ T-04
- `date_from`: ใช้ "วันนี้" ตามเขตเวลา Asia/Bangkok (ASM-02) รูปแบบ YYYY-MM-DD
- ไม่ได้กรองหรือปิดปุ่มช่วงที่ remaining เป็น 0 เพราะ spec ไม่ได้บอก หน้าจอแสดงตามที่ API ส่งมา
- ปุ่มเลือกช่วงเวลาเรียก `onSelectSlot` อย่างเดียว ยังไม่ได้ทำหน้ายืนยัน เพราะเป็นงานของ T-18

---

## 2569-09-23 ทีมอนุมัติ T-01, T-17 และตอบคำถามก่อนทำขั้นเสริม 2 (เชื่อมหน้าจอกับหลังบ้านจริง)

- เครื่องมือ: Claude Code (VS Code ใน Codespaces)
- คำสั่ง: ทำตามเอกสาร "ขั้นเสริม 2 เชื่อมหน้าจอกับหลังบ้านจริง"
- AI แจ้งว่าเลข task ในเอกสารตัวอย่างไม่ตรงกับ tasks.md ของเรา: GET /slots คือ T-04 (ต้องทำหลัง T-02, T-03) และ task เชื่อมคือ T-21

### คำถามที่ AI ถาม และคำตอบของทีม

1. T-01 และ T-17 ตรวจผ่านแล้วหรือยัง -> ตรวจแล้ว เปลี่ยนสถานะเป็น "เสร็จ" (ผ่าน checklist 5 ข้อและ commit แล้ว)
2. หน้าจอส่งผลยืนยันตัวตน (IF-IDP-01) มาอย่างไรตอนทดลองเชื่อมครบวงจร (ข้อสังเกต 5) -> ใช้ตัวตรวจจำลองเฉพาะตอนพัฒนา เปิดด้วยตัวแปรสภาพแวดล้อม ค่าเริ่มต้นยังปฏิเสธ request ที่ไม่มีผลยืนยันตัวตน
3. แยก T-21 อย่างไร -> T-21 แคบลงเหลือ "ต่อหน้าเลือกช่วงเวลากับ GET /slots จริง พร้อมข้อมูลตัวอย่าง" และสร้าง T-22 "ต่อหน้ายืนยันและหน้าผลการจองกับ POST /bookings จริง"
4. วิธีทำงาน -> ทำ T-02, T-03, T-04, แยก T-21, ทำ T-21 ตามลำดับ commit + push ทีละ task ถ้าเจอสิ่งที่ต้องเดาให้หยุดถาม
5. FR-BKG-01 "ภายใน 30 วันข้างหน้า" -> GET /slots คืนช่วงของวัน date_from ถึง date_from+29 (รวม 30 วัน)
6. ช่วงที่เหลือ 0 ที่ -> ไม่คืนใน GET /slots ("ที่ว่าง" หมายถึง remaining > 0)
7. ฐานข้อมูลตอนทดลองเชื่อมครบวงจร (ข้อสังเกต 4) -> SQLite ไฟล์ `DATABASE_URL=sqlite:///./dev.db` (ยังไม่ใช่การตรวจ CON-TECH-01 ซึ่งเป็นงานของ T-15)

### สิ่งที่แก้ใน tasks.md

- สถานะ T-01 และ T-17: "เสร็จ รอทีมตรวจ" -> "เสร็จ"

---

## 2569-09-23 คำสั่ง: /implement T-02

- เครื่องมือ: Claude Code (VS Code ใน Codespaces)
- task: T-02 สร้างตาราง slots, bookings, audit_logs และ migration 001_init (รองรับ CON-TECH-01, DOM-PDPA-01, IF-HIS-01, FR-BKG-04)
- ไฟล์ที่สร้าง (ตรงกับช่อง "ไฟล์ที่แตะ"): `backend/app/db/models.py`, `backend/app/db/migrations/001_init.py`, `backend/tests/test_IF_HIS_01_schema.py`
- ผล test (`cd backend && pytest -v`): 9 passed (ของ T-02 5 ตัว: test_T02_upgrade_creates_three_tables, test_IF_HIS_01_bookings_has_hn_and_no_national_id, test_T02_queue_no_is_nullable, test_DOM_PDPA_01_audit_logs_columns, test_T02_slots_columns)
- สิ่งที่เกือบต้องเดาแต่ไม่ได้เดา:
  - ค่าของ `status` ใน bookings (เช่น "ยังไม่ได้ใช้" ตาม FR-BKG-02) spec ไม่ได้กำหนด จึงสร้างเป็นคอลัมน์ข้อความเปล่า ๆ ไม่มีค่าเริ่มต้น ให้ T-05 และ T-06 ตัดสินใจ
  - ความยาวของข้อความ และ index เพื่อความเร็ว plan ไม่ได้ระบุ จึงไม่ได้กำหนด (ตอนแรกใส่ index ไว้ แล้วเอาออกเพราะไม่มีใน plan)

---

## 2569-09-23 คำสั่ง: /implement T-03

- เครื่องมือ: Claude Code (VS Code ใน Codespaces)
- task: T-03 ตรวจผลยืนยันตัวตนก่อนเข้าถึงทุก endpoint (รองรับ IF-IDP-01)
- ไฟล์ที่สร้างหรือแก้ (ตรงกับช่อง "ไฟล์ที่แตะ"): สร้าง `backend/app/auth/idp.py`, `backend/tests/test_IF_IDP_01.py` แก้ `backend/tests/conftest.py` (เพิ่ม fixture `client` ที่ยืนยันตัวตนแล้วด้วยตัวตรวจจำลอง)
- ผล test (`cd backend && pytest -v`): 13 passed (ของ T-03 4 ตัว: test_IF_IDP_01_rejects_request_without_identity, test_IF_IDP_01_accepts_request_with_identity, test_IF_IDP_01_default_rejects_all, test_IF_IDP_01_dev_mode_accepts_dev_user) มี warning 1 ตัวจาก library (StarletteDeprecationWarning เรื่อง httpx) ไม่ได้มาจากโค้ดของเรา
- ตามคำตอบข้อ 2 ของทีม: ค่าเริ่มต้นปฏิเสธทุก request (ยังไม่มีการเชื่อมระบบยืนยันตัวตนจริง) และมีตัวตรวจจำลองเปิดด้วย `AUTH_MODE=dev` ที่ถือว่าเป็นผู้ใช้ `dev-user`
- สิ่งที่เกือบต้องเดาแต่ไม่ได้เดา: รูปแบบที่หน้าจอส่งผลยืนยันตัวตน (header, token) ไม่มีใน spec/plan จึงไม่ได้สร้าง ตัวตรวจจริงยังรอข้อสังเกต 5
- สถานะ: T-02 เปลี่ยนเป็น "เสร็จ" (ทีมอนุมัติให้ถือว่าเสร็จหลัง commit ตามคำตอบข้อ 4) T-03 เป็น "เสร็จ รอทีมตรวจ"

---

## 2569-09-23 คำสั่ง: /implement T-04

- เครื่องมือ: Claude Code (VS Code ใน Codespaces)
- task: T-04 สร้าง GET /slots แสดงช่วงว่าง 30 วันตามแพ็กเกจ (รองรับ FR-BKG-01, FR-BKG-06)
- ไฟล์ที่สร้างหรือแก้ (ตรงกับช่อง "ไฟล์ที่แตะ"): สร้าง `backend/app/slots/router.py`, `backend/app/slots/service.py`, `backend/tests/test_FR_BKG_01_06_slots.py` แก้ `backend/app/main.py` (รวม router)
- ผล test (`cd backend && pytest -v`): 17 passed (ของ T-04 4 ตัว: test_FR_BKG_01_slots_within_30_days_with_remaining, test_FR_BKG_01_full_slot_not_returned, test_FR_BKG_06_slots_by_package, test_IF_IDP_01_slots_requires_identity) มี warning 1 ตัวจาก library เหมือนเดิม
- ใช้คำตอบของทีม: ขอบเขต date_from ถึง date_from+29 และไม่คืนช่วงที่ remaining เป็น 0
- สิ่งที่เกือบต้องเดาแต่ไม่ได้เดา:
  - ไม่ได้บังคับว่า date_from ต้องไม่ก่อนวันนี้ เพราะ spec/plan ไม่ได้บอก หน้าจอเป็นคนส่ง "วันนี้" ตาม Asia/Bangkok (ASM-02)
  - `start_time` ส่งออกเป็นรูปแบบมาตรฐาน `09:00:00` ไม่ได้ตัดให้เหลือ `09:00` เพราะไม่มีข้อกำหนดเรื่องรูปแบบการแสดงเวลา
  - ไม่ได้ส่ง `capacity` ออกไป เพราะ plan ข้อ 4 ระบุแค่ "รายการช่วงเวลา + ที่นั่งคงเหลือ"
- สถานะ: T-03 เปลี่ยนเป็น "เสร็จ" (อนุมัติหลัง commit ตามคำตอบข้อ 4) T-04 เป็น "เสร็จ รอทีมตรวจ"
