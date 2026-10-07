// TC-BKG-01-2 (AC-BKG-01, FR-BKG-04): หน้าแสดงผลการจองแสดงหมายเลขคิวที่ API ตอบ
// สร้างจาก specs/001-booking/test-cases.md ด้วย /testcases
// ส่ง API จำลองเข้าหน้าจอแทนหลังบ้านจริง ตาม plan.md ข้อ 4 และ src/api/client.js
import { render, screen, fireEvent } from '@testing-library/react'
import ConfirmBooking from '../pages/ConfirmBooking.jsx'

test('TC-BKG-01-2 แสดงหมายเลขคิวหลังยืนยันการจอง', async () => {
  // Given ยืนยันตัวตนแล้ว และ API จำลองตอบ POST /bookings สำเร็จพร้อม booking_id และ queue_no
  const api = {
    createBooking: async () => ({
      status: 201,
      body: { booking_id: 1, slot_id: 10, queue_no: 'Q-TEST-1' },
    }),
  }
  render(<ConfirmBooking api={api} slot={{ id: 10, start_time: '09:00' }} />)

  // When ผู้ใช้กดยืนยันการจองช่วง 09.00 น.
  fireEvent.click(screen.getByRole('button', { name: /ยืนยัน/ }))

  // Then (1) หน้าแสดงผลการจอง (BookingResult) แสดงหมายเลขคิวตามค่า queue_no ที่ API ตอบ
  expect(await screen.findByText(/Q-TEST-1/)).toBeTruthy()
  // รูปแบบของเลขคิวบนหน้าจอยังไม่ตรวจ เพราะรอ Q-02
})
