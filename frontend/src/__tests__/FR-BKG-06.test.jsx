// T-17: FR-BKG-01, FR-BKG-06 ยังไม่มี AC ใน spec จึงตั้งชื่อตาม FR (tasks.md ข้อสังเกต 6)
import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { vi } from 'vitest'
import SlotPicker from '../pages/SlotPicker.jsx'

// client จำลองตามสัญญา GET /slots ใน plan ข้อ 4 (ฟิลด์ตามตาราง slots ใน plan ข้อ 3)
function mockClient() {
  const slotsByPackage = {
    'PKG-TEST-1': [
      { id: 1, slot_date: '2026-10-01', start_time: '09:00', package_code: 'PKG-TEST-1', remaining: 3 },
      { id: 2, slot_date: '2026-10-01', start_time: '10:00', package_code: 'PKG-TEST-1', remaining: 1 },
    ],
    'PKG-TEST-2': [
      { id: 3, slot_date: '2026-10-02', start_time: '13:00', package_code: 'PKG-TEST-2', remaining: 5 },
    ],
  }
  return {
    getSlots: vi.fn(async ({ packageCode }) => slotsByPackage[packageCode]),
  }
}

// FR-BKG-01: แสดงช่วงเวลาที่ว่างพร้อมจำนวนที่นั่งคงเหลือ
test('FR-BKG-01 แสดงช่วงเวลาพร้อมที่นั่งคงเหลือ', async () => {
  const client = mockClient()
  render(<SlotPicker client={client} packages={['PKG-TEST-1', 'PKG-TEST-2']} />)

  expect(await screen.findByText('09:00')).toBeTruthy()
  expect(screen.getByText('เหลือ 3 ที่')).toBeTruthy()
  expect(screen.getByText('10:00')).toBeTruthy()
  expect(screen.getByText('เหลือ 1 ที่')).toBeTruthy()
  expect(client.getSlots).toHaveBeenCalledWith(expect.objectContaining({ packageCode: 'PKG-TEST-1' }))
})

// FR-BKG-06: เปลี่ยนแพ็กเกจแล้วเรียก getSlots ใหม่ด้วย package_code ใหม่
test('FR-BKG-06 เปลี่ยนแพ็กเกจแล้วโหลดช่วงเวลาใหม่', async () => {
  const client = mockClient()
  render(<SlotPicker client={client} packages={['PKG-TEST-1', 'PKG-TEST-2']} />)
  await screen.findByText('09:00')

  fireEvent.change(screen.getByRole('combobox'), { target: { value: 'PKG-TEST-2' } })

  await waitFor(() =>
    expect(client.getSlots).toHaveBeenLastCalledWith(expect.objectContaining({ packageCode: 'PKG-TEST-2' })),
  )
  expect(await screen.findByText('13:00')).toBeTruthy()
  expect(screen.getByText('เหลือ 5 ที่')).toBeTruthy()
  expect(screen.queryByText('09:00')).toBeNull()
})
