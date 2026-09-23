import { api } from './api/client.js'
import SlotPicker from './pages/SlotPicker.jsx'

// รหัสแพ็กเกจตัวอย่าง ต้องตรงกับ backend/app/db/seed.py (ไม่ได้มาจาก spec เพราะ plan ยังไม่มี API รายการแพ็กเกจ ข้อสังเกต 7)
const DEMO_PACKAGES = ['DEMO-A', 'DEMO-B']

// FR-BKG-01, FR-BKG-06: หน้าแรกแสดงหน้าเลือกแพ็กเกจและช่วงเวลา ดึงข้อมูลจาก GET /slots จริง (T-21)
export default function App() {
  return (
    <main className="mx-auto max-w-2xl p-6">
      <h1 className="text-2xl font-bold text-teal-800">ระบบจองคิวตรวจสุขภาพ</h1>
      <SlotPicker client={api} packages={DEMO_PACKAGES} />
    </main>
  )
}
