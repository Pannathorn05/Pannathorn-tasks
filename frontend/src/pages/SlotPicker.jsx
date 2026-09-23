import { useEffect, useState } from 'react'

// ASM-02: "วันนี้" ใช้เขตเวลา Asia/Bangkok รูปแบบ YYYY-MM-DD
function todayInBangkok() {
  return new Intl.DateTimeFormat('en-CA', { timeZone: 'Asia/Bangkok' }).format(new Date())
}

// FR-BKG-01: จัดกลุ่มช่วงเวลาตามวัน เพื่อแสดงช่วงว่างของแต่ละวัน
function groupByDate(slots) {
  const groups = new Map()
  for (const slot of slots) {
    if (!groups.has(slot.slot_date)) groups.set(slot.slot_date, [])
    groups.get(slot.slot_date).push(slot)
  }
  return [...groups.entries()]
}

// FR-BKG-01, FR-BKG-06: หน้าเลือกแพ็กเกจและช่วงเวลา เปลี่ยนแพ็กเกจแล้วโหลดช่วงว่างใหม่
// packages รับเป็น props ไปก่อน เพราะ plan ข้อ 4 ยังไม่มี API รายการแพ็กเกจ (tasks.md ข้อสังเกต 7)
export default function SlotPicker({ client, packages, onSelectSlot }) {
  const [packageCode, setPackageCode] = useState(packages[0])
  const [slots, setSlots] = useState(null)
  const [error, setError] = useState(false)

  useEffect(() => {
    let stale = false
    setSlots(null)
    setError(false)
    client
      .getSlots({ dateFrom: todayInBangkok(), packageCode })
      .then((data) => {
        if (!stale) setSlots(data)
      })
      // T-21: เรียกหลังบ้านไม่สำเร็จ แสดงข้อความแทนการค้างที่ "กำลังโหลด"
      .catch(() => {
        if (!stale) setError(true)
      })
    return () => {
      stale = true
    }
  }, [client, packageCode])

  return (
    <section className="mt-6 space-y-4">
      <label className="block">
        <span className="text-sm font-medium text-slate-700">แพ็กเกจ</span>
        <select
          className="mt-1 block w-full rounded-md border border-slate-300 bg-white p-2"
          value={packageCode}
          onChange={(e) => setPackageCode(e.target.value)}
        >
          {packages.map((code) => (
            <option key={code} value={code}>
              {code}
            </option>
          ))}
        </select>
      </label>

      {error ? (
        <p role="alert" className="rounded-md bg-red-50 p-3 text-red-700">
          โหลดช่วงเวลาไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
        </p>
      ) : slots === null ? (
        <p className="text-slate-500">กำลังโหลดช่วงเวลา...</p>
      ) : (
        groupByDate(slots).map(([date, daySlots]) => (
          <div key={date} className="rounded-lg border border-slate-200 bg-white p-4">
            <h2 className="font-semibold text-teal-800">{date}</h2>
            <ul className="mt-2 grid grid-cols-2 gap-2 sm:grid-cols-3">
              {daySlots.map((slot) => (
                <li key={slot.id}>
                  <button
                    type="button"
                    className="w-full rounded-md border border-teal-600 px-3 py-2 text-left hover:bg-teal-50"
                    onClick={() => onSelectSlot?.(slot)}
                  >
                    <span className="block font-medium">{slot.start_time}</span>
                    <span className="block text-sm text-slate-600">เหลือ {slot.remaining} ที่</span>
                  </button>
                </li>
              ))}
            </ul>
          </div>
        ))
      )}
    </section>
  )
}
