import SlotPicker from './pages/SlotPicker.jsx'

// ข้อมูลจำลองสำหรับเปิดดูหน้าจอก่อนมีหลังบ้าน (ไม่ได้มาจาก spec) T-21 จะเปลี่ยนไปใช้ api จริงใน api/client.js
const DEMO_PACKAGES = ['DEMO-A', 'DEMO-B']

// FR-BKG-01, FR-BKG-06: client จำลองตามสัญญา GET /slots ใน plan ข้อ 4
const demoClient = {
  async getSlots({ dateFrom, packageCode }) {
    const day = (offset) => {
      const d = new Date(`${dateFrom}T00:00:00`)
      d.setDate(d.getDate() + offset)
      return d.toLocaleDateString('en-CA')
    }
    const times = packageCode === 'DEMO-A' ? ['09:00', '10:00', '11:00'] : ['13:00', '14:00']
    return [1, 2].flatMap((offset) =>
      times.map((start_time, i) => ({
        id: `${packageCode}-${offset}-${i}`,
        slot_date: day(offset),
        start_time,
        package_code: packageCode,
        remaining: (offset + i) % 4,
      })),
    )
  },
}

// FR-BKG-01, FR-BKG-06: หน้าแรกแสดงหน้าเลือกแพ็กเกจและช่วงเวลา (T-17)
export default function App() {
  return (
    <main className="mx-auto max-w-2xl p-6">
      <h1 className="text-2xl font-bold text-teal-800">ระบบจองคิวตรวจสุขภาพ</h1>
      <SlotPicker client={demoClient} packages={DEMO_PACKAGES} />
    </main>
  )
}
