# RTM: จองคิวตรวจสุขภาพ (Booking)
อ้างอิง: spec.md SPEC-BKG-001 Draft v2 | tasks.md (เสร็จ T-01 ถึง T-03) | test-cases.md (AC-BKG-01 6 แถว)
สร้างด้วย /verify เมื่อ 2569-10-07 09.06 | test: 8 ผ่าน 1 ไม่ผ่าน
(หลังบ้าน pytest 7 ผ่าน 0 ไม่ผ่าน / หน้าจอ vitest 1 ผ่าน 1 ไม่ผ่าน: TC-BKG-01-2.test.jsx หาไฟล์ pages/ConfirmBooking.jsx ไม่เจอ เพราะ T-11 ยังไม่ได้ทำ และ T-06 รอ Q-02)

## 1. ตามรอยไปข้างหน้า (requirement ไป โค้ด ไป test)
| ID | AC | task | โค้ด (ไฟล์: ฟังก์ชัน) | test (ผล) | สถานะ |
|---|---|---|---|---|---|
| FR-BKG-01 | AC-BKG-05 (ตรวจแค่ความเร็ว) | T-02 เสร็จ, T-10 พร้อมทำ, T-12 พร้อมทำ | slots/router.py: get_slots, slots/service.py: list_available_slots | test_AC_BKG_05 (ผ่าน) ตรวจแค่ status 200 และเวลา | ช่องโหว่ (F-03, F-06) |
| FR-BKG-02 | AC-BKG-02 | T-04 พร้อมทำ | ยังไม่มี | ยังไม่มี | ยังไม่ถึง |
| FR-BKG-03 | AC-BKG-03 | T-05, T-11, T-12 พร้อมทำ | booking/router.py: create_booking ตอบ 409 "ช่วงเวลาเต็ม" แล้ว แต่ยังไม่เสนอ 3 ช่วง | test_TC_BKG_01_3_no_seat_left (ผ่าน) ตรวจแค่ส่วน "ไม่สร้างรายการจอง" | ยังไม่ถึง |
| FR-BKG-04 | AC-BKG-01 | T-03 เสร็จ, T-06 รอ Q-02, T-07 พร้อมทำ (ส่วนส่งข้อความ) | booking/router.py: create_booking, booking/service.py: create_booking, next_queue_no | test_AC_BKG_01 (ผ่าน), test_TC_BKG_01_1_book_last_seat (ผ่าน), test_TC_BKG_01_3_no_seat_left (ผ่าน), test_TC_BKG_01_4_not_authenticated (ผ่าน), TC-BKG-01-2.test.jsx (ไม่ผ่าน: ยังไม่ได้สร้างหน้าจอ) | ช่องโหว่ (F-04, F-05, F-09, F-10) |
| FR-BKG-05 | AC-BKG-04 | T-07 พร้อมทำ | ยังไม่มี (GET /bookings/{id} ใน plan ข้อ 4 ยังไม่มีโค้ด และไม่มี task ใดสร้าง) | ยังไม่มี | ยังไม่ถึง |
| FR-BKG-06 | ไม่มี AC | T-02 เสร็จ, T-10 พร้อมทำ | slots/service.py: list_available_slots (กรองตาม package_code) | ไม่มี test ที่ตรวจการเปลี่ยนแพ็กเกจ | ช่องโหว่ (F-07) |
| NFR-PERF-01 | AC-BKG-05 | T-02 เสร็จ | slots/service.py: list_available_slots | test_AC_BKG_05 (ผ่าน) แบบย่อส่วน | ช่องโหว่ (F-08) |
| NFR-SEC-01 | ไม่มี AC | ไม่มี task | ไม่มี (TLS เป็นเรื่องการติดตั้งเครื่อง) | ไม่มี | ช่องโหว่ (F-11) |
| NFR-REL-02 | AC-BKG-04 | T-07 พร้อมทำ | ยังไม่มี | ยังไม่มี | ยังไม่ถึง |
| NFR-USE-01 | ไม่มี AC | ไม่มี task | ไม่มี | ไม่มี | ช่องโหว่ (F-12) |
| CON-TECH-01 | ไม่มี AC ตรง ๆ (tasks.md ระบุไว้) | T-01 เสร็จ | config.py: DATABASE_URL, db/session.py, requirements.txt มี psycopg | test_T01_tables_created (ผ่าน) รันบน SQLite ตาม plan ข้อ 2 | ครบ |
| DOM-PDPA-01 | AC-BKG-06 | T-01 เสร็จ (ตาราง audit_logs), T-08 พร้อมทำ | db/models.py: AuditLog (ยังไม่มีโค้ดที่เขียน log) | test_T01_tables_created (ผ่าน) ตรวจแค่ว่ามีตาราง | ยังไม่ถึง |
| IF-IDP-01 | ไม่มี AC ตรง ๆ (ตรวจผ่าน TC-BKG-01-4) | T-03 เสร็จ | auth/idp.py: get_verified_hn | test_TC_BKG_01_4_not_authenticated (ผ่าน) | ช่องโหว่ (F-02) |
| IF-HIS-01 | ไม่มี AC ตรง ๆ | T-01 เสร็จ, T-09 พร้อมทำ | db/models.py: Booking ไม่มี national_id | test_T01_no_national_id (ผ่าน) | ช่องโหว่ (F-01) |
| IF-NOT-01 | ไม่มี AC ตรง ๆ (ตรวจผ่าน AC-BKG-04) | T-07 พร้อมทำ | ยังไม่มี | ยังไม่มี | ยังไม่ถึง |

## 2. ตามรอยย้อนกลับ (โค้ด ไป requirement)
1 แถวต่อ 1 endpoint หรือฟังก์ชันหลัก
| โค้ด (ไฟล์: ฟังก์ชัน หรือ endpoint) | อ้าง ID | ตรงกับข้อความใน spec ไหม | หมายเหตุ |
|---|---|---|---|
| GET /slots (slots/router.py: get_slots) | FR-BKG-01, FR-BKG-06 | บางส่วน | แสดงช่วงว่างพร้อม remaining และกรองตามแพ็กเกจตรงกับ FR แต่ช่วงวันใช้ 14 วัน spec บอก 30 วัน (F-03) |
| slots/service.py: list_available_slots, DAYS_AHEAD = 14 | FR-BKG-01, FR-BKG-06 | ไม่ตรง | ตัวเลข 14 ขัดกับ "30 วันข้างหน้า" (F-03) |
| POST /bookings (booking/router.py: create_booking) | FR-BKG-04, IF-IDP-01 | บางส่วน | ตัดที่นั่ง บันทึก คืน queue_no ตรงกับ FR-BKG-04 แต่ request มีฟิลด์ national_id ที่ plan ข้อ 4 ไม่ได้กำหนด (in: slot_id อย่างเดียว) และเขียน national_id ลง log (F-01) |
| booking/service.py: create_booking | FR-BKG-04 | ตรง | หลังแก้บรรทัด 26 เป็น remaining <= 0 แล้วไม่จองเกินโควตา ข้อสังเกต: อ่าน remaining แล้วค่อยลด โดยไม่ล็อกแถว ถ้าผู้ใช้ 2 คนจองที่นั่งสุดท้ายพร้อมกันอาจเกิดการจองซ้อน เรื่องนี้เป็นของ AC-BKG-03 ซึ่ง T-05 ยังไม่ได้ทำ จึงยังไม่นับเป็นข้อค้นพบ |
| booking/service.py: next_queue_no (รูปแบบ A001 นับใหม่ทุกวัน) | FR-BKG-04 | ไม่ตรง | FR-BKG-04 สั่งให้ออกหมายเลขคิว แต่รูปแบบและการรีเซ็ตเป็น Q-02 ที่ยังไม่มีคำตอบ (F-05) |
| DELETE /bookings/{id} (booking/router.py: cancel_booking) | FR-BKG-04 | ไม่ตรง | การยกเลิกคิวคือ UC-02 อยู่ใน Out of scope ส่วน FR-BKG-04 พูดเรื่องยืนยันการจอง ไม่ใช่ยกเลิก (F-04) |
| booking/service.py: cancel_booking | FR-BKG-04 | ไม่ตรง | เหมือนแถวบน และมีค่า status "CANCELLED" ที่ไม่มีใน spec (F-04) |
| auth/idp.py: get_verified_hn | IF-IDP-01 | บางส่วน | ปฏิเสธเมื่อไม่มี token ตรงกับ IF-IDP-01 แต่ยอมรับทุก token ที่ขึ้นต้น "Bearer verified:" แล้วใช้ HN ที่ผู้เรียกพิมพ์มาเอง ไม่ได้ถามระบบยืนยันตัวตน (F-02) |
| db/models.py: Slot, Booking, AuditLog | CON-TECH-01, DOM-PDPA-01, IF-HIS-01, FR-BKG-04 | ตรง | Booking ไม่มี national_id ตรงกับ IF-HIS-01 ฟิลด์ตรงกับ plan ข้อ 3 |
| db/migrations/001_init.py: upgrade | CON-TECH-01 | ตรง | |
| config.py: DATABASE_URL, db/session.py | CON-TECH-01 | ตรง | ค่าเริ่มต้นเป็น SQLite (dev.db) ไว้รันใน Codespace ตาม plan ข้อ 2 ระบบจริงต้องตั้ง DATABASE_URL เป็น PostgreSQL |
| main.py: lifespan, app | ไม่อ้าง (T-02, T-03) | ตรง | สร้างตารางตอนเปิดหลังบ้าน และรวม router |
| frontend/src/api/client.js: getSlots, createBooking | plan ข้อ 4 | ตรงกับสัญญา API | ข้อสังเกต: createBooking ไม่ได้ส่ง Authorization ถ้าต่อกับหลังบ้านจริงจะได้ 401 เรื่องนี้เป็นของ T-12 ที่ยังไม่ได้ทำ จึงยังไม่นับเป็นข้อค้นพบ |
| frontend/src/App.jsx, main.jsx | ไม่อ้าง | ไม่มีเรื่องของ spec | โครงเริ่มต้นของรายวิชา ยังไม่มีหน้าจอของ task ใด |

## 3. ข้อค้นพบ
ชนิด: AC ไม่มี test / test อ่อน / โค้ดไม่มี FR / FR ไม่มี AC / เดา Q-xx / ละเมิด Constraint / ตัวเลขไม่ตรง spec / อ้าง ID ผิดเรื่อง
ทีมตัดสิน: แก้โค้ด / แก้ spec / เพิ่ม Q-xx / ไม่ใช่ปัญหา (พร้อมเหตุผล 1 บรรทัด)

| F-ID | ชนิด | อยู่ที่ | ขัดกับ | รายละเอียด | ทีมตัดสิน |
|---|---|---|---|---|---|
| F-01 | ละเมิด Constraint | backend/app/booking/router.py บรรทัด 19, 25 | IF-HIS-01, plan ข้อ 4 | BookingRequest รับฟิลด์ national_id (คอมเมนต์บอกว่า "เผื่อใช้ค้น HN") และ logger.info เขียนเลขบัตรประชาชนลง log ทุกครั้งที่จอง IF-HIS-01 ให้อ้างอิงภายในด้วย HN และไม่เก็บเลขบัตรประชาชน ส่วน plan ข้อ 4 กำหนดให้ POST /bookings รับแค่ slot_id การค้น HN ด้วยเลขบัตรเป็นหน้าที่ของ GET /patients/lookup (T-09) วิธีแก้ที่เป็นไปได้: ลบฟิลด์ national_id และเอาออกจากข้อความ log | |
| F-02 | ละเมิด Constraint | backend/app/auth/idp.py บรรทัด 13-15 | IF-IDP-01 | ยอมรับทุก token ที่ขึ้นต้น "Bearer verified:" แล้วใช้ HN ที่อยู่ท้าย token ซึ่งผู้เรียกพิมพ์เองได้ ไม่ได้ส่งไปตรวจกับระบบยืนยันตัวตน ใครก็จองในนาม HN ของคนอื่นได้ คอมเมนต์ในโค้ดยอมรับว่าเป็นตัวจำลอง แต่ T-03 ขึ้นสถานะ "เสร็จ" โดยอ้างว่ารองรับ IF-IDP-01 และไม่มี task ใดรับไปต่อกับระบบยืนยันตัวตนจริง | |
| F-03 | ตัวเลขไม่ตรง spec | backend/app/slots/service.py บรรทัด 10 | FR-BKG-01, Scope | DAYS_AHEAD = 14 แต่ FR-BKG-01 และ Scope บอก "ภายใน 30 วันข้างหน้า" ช่วงเวลาวันที่ 15 ถึง 30 จึงไม่แสดง และไม่มี test ใดจับได้ (ดู F-06) | |
| F-04 | โค้ดไม่มี FR | backend/app/booking/router.py บรรทัด 35-41, backend/app/booking/service.py บรรทัด 43-51 | Out of scope (UC-02), plan ข้อ 4 | DELETE /bookings/{id} และ cancel_booking ยกเลิกการจองและคืนที่นั่ง การยกเลิกคิวอยู่ใน Out of scope ไม่มีใน plan ข้อ 4 และไม่มี task รองรับ prompt-log บันทึกว่า AI เพิ่มเอง "เพื่อความสมบูรณ์ของระบบ" ตอนทำ T-03 นอกจากนี้คอมเมนต์ยังอ้าง FR-BKG-04 ซึ่งพูดเรื่องยืนยันการจอง ไม่ใช่การยกเลิก (อ้าง ID ผิดเรื่อง) | |
| F-05 | เดา Q-02 | backend/app/booking/service.py บรรทัด 13-18 | Q-02, plan ข้อ 1 และข้อ 3 | next_queue_no ออกเลขรูปแบบ "A001" และนับใหม่ทุกวัน ซึ่งเป็นการตอบ Q-02 แทนเจ้าหน้าที่เวชระเบียน และ "A001" คือตัวอย่างในวงเล็บของ Q-02 เอง plan บอกว่า "ยังไม่กำหนดวิธีออกเลข จนกว่า Q-02 จะได้คำตอบ" และ T-06 ยังมีสถานะรอ Q-02 | |
| F-06 | FR ไม่มี AC | spec.md หมวด Acceptance Criteria | FR-BKG-01 | AC เดียวที่อ้าง FR-BKG-01 คือ AC-BKG-05 ซึ่งตรวจแค่ความเร็ว ไม่มี AC ที่ตรวจว่าแสดงช่วงเวลาภายใน 30 วันและจำนวนที่นั่งคงเหลือถูกต้อง F-03 จึงหลุดมาได้ ควรเสนอ AC ใหม่ให้ทีม (ห้าม AI ตั้ง ID เอง) | |
| F-07 | FR ไม่มี AC | spec.md หมวด Acceptance Criteria | FR-BKG-06 | ไม่มี AC อ้าง FR-BKG-06 เลย plan ข้อ 6 ก็ระบุไว้แล้วว่า "ควรเสนอทีมเพิ่ม AC" โค้ดกรองตามแพ็กเกจแล้ว แต่ไม่มี test ที่ตรวจ | |
| F-08 | test อ่อน | backend/tests/test_AC_BKG_05.py | AC-BKG-05, NFR-PERF-01 | เรียก GET /slots ทีละครั้งต่อกัน 200 ครั้ง ไม่ได้ยิงพร้อมกัน 200 คน บน SQLite ในหน่วยความจำและมีข้อมูลแค่ 10 ช่วง ผล p95 จึงบอกไม่ได้ว่าระบบจริงผ่าน Given "ผู้ใช้พร้อมกัน 200 คน" plan ข้อ 6 เขียนไว้เองว่าผลจริงต้องวัดบนเครื่องทดสอบ แต่ยังไม่มี task หรือแถว "คน" ที่ทำส่วนนั้น | |
| F-09 | AC ไม่มี test | specs/001-booking/test-cases.md แถว TC-BKG-01-5 | AC-BKG-01 | แถว TC-BKG-01-5 สถานะ "ใช้ได้" แต่ไม่มี test ในโค้ด ทีมสั่งลบ test_TC_BKG_01_5_slot_not_found เพราะช่อง Then ทุกส่วนเป็น "spec ไม่ได้บอก" และยังไม่ได้ตัดสินว่าจะลบแถว เปลี่ยนเป็น "ร่าง" หรือเติม Then | |
| F-10 | test อ่อน | backend/tests/test_AC_BKG_01.py บรรทัด 6-12 | AC-BKG-01 | test_AC_BKG_01 ใช้ชื่อ AC แต่ assert แค่ status 201 ไม่ได้ดูว่าบันทึกจริง มีหมายเลขคิว หรือที่นั่งเหลือ 0 ส่วนเหล่านี้ test_TC_BKG_01_1_book_last_seat ตรวจครบแล้ว จึงร้ายแรงน้อย แต่ชื่อ test ทำให้เข้าใจว่า AC-BKG-01 ถูกตรวจครบด้วย test ตัวนี้ | |
| F-11 | FR ไม่มี AC | spec.md หมวด Quality Requirements | NFR-SEC-01 | ไม่มี AC และไม่มี task ที่ตรวจว่ารับส่งด้วย TLS 1.2 ขึ้นไป | |
| F-12 | FR ไม่มี AC | spec.md หมวด Quality Requirements | NFR-USE-01 | ไม่มี AC และไม่มี task สำหรับทดสอบกับผู้ใช้ใหม่ 10 คน (ASM-05) ต้องเป็นการทดสอบโดยคน | |

## 4. แก้แล้ว
| F-ID | แก้อย่างไร | รู้ได้อย่างไร |
|---|---|---|
| - | rtm.md สร้างครั้งแรก ยังไม่มีข้อค้นพบเดิม (หมายเหตุ: บั๊กจองได้เมื่อเหลือ 0 ที่ ถูกแก้ไปก่อนสร้าง rtm.md ที่ service.py บรรทัด 26 ตามที่ทีมสั่ง และ test_TC_BKG_01_3_no_seat_left ผ่านแล้ว) | |
