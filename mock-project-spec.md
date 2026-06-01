# Mock Project Spec — "Draw → Scan → Touch"

**Locked**: 2026-05-29 (Wave: **ONE mock project**, down from 2)
**Type**: Single integrated flow using BOTH motion tracking + kiosk skills
**Scope**: **1 ชิ้นเดียว** — ทุกทีมทำตัวเดียวกันนี้ (ไม่แยก 2 mock แล้ว)
**Inspiration**: teamLab Sketch Aquarium pattern

---

## User Flow

```
┌─────────┐   ┌────────┐   ┌──────────┐   ┌──────────────┐   ┌────────┐
│ 1. DRAW │ → │ 2.SCAN │ → │ 3. LOAD  │ → │ 4. INTERACT  │ → │ 5.SAVE │
│         │   │        │   │          │   │              │   │        │
│ กระดาษ  │   │ webcam │   │ auto-    │   │ particles +  │   │ data + │
│ + crayon│   │ +ArUco │   │ open ใน  │   │ MediaPipe    │   │ image  │
│         │   │ markers│   │ TD       │   │ hand swipe   │   │ archive│
└─────────┘   └────────┘   └──────────┘   └──────────────┘   └────────┘
```

## Step-by-step

### 1. Draw
- User วาดบนกระดาษ template (มี **4 ArUco markers ที่มุม**)
- พื้นที่วาด = ภายในกรอบ markers
- ใช้สี/ปากกา/ดินสอ — ทุกอย่างที่ contrast กับขาว

### 2. Scan
- Webcam + ArUco detection (Python OpenCV ใน TD Script TOP)
- ตรวจ 4 markers → คำนวณ homography → warp ภาพให้เป็นสี่เหลี่ยมตรง
- Extract canvas (ภายใน markers) → save เป็น PNG ไฟล์

### 3. Load
- TD watches folder → ไฟล์ใหม่เข้า = auto-load
- Movie File In TOP → texture
- (Optional: transition animation = paper "บินขึ้นจอ")

### 4. Interact
- Drawing → particle system (GPU TOP)
  - Method A (simple): texture เป็น initial color/position ของ particles
  - Method B (meaningful): edge detect → particles emerge ตามเส้นที่วาด
- MediaPipe webcam → hand tracking
- Hand position/velocity → push force ต่อ particles
- ปัดมือ → particles กระจาย, ลอย, follow มือ

### 5. Save
- Drawing original (PNG) → archive folder
- (Optional) Session metadata: timestamp, duration, interaction stats
- (Optional) Screenshot ตอน peak interaction → gallery

## Tech Stack

| Stage | Tool |
|-------|------|
| Drawing template | PDF generator (Python `cv2.aruco.drawMarker`) — Wave print หรือส่งให้ client print |
| ArUco detection | OpenCV `cv2.aruco` ใน TD Script TOP (RintaroFujita repo reference) |
| Homography warp | `cv2.warpPerspective` |
| Image archive | OS Watch DAT + Movie File In |
| Particles | GPU Particle TOP / GLSL TOP feedback |
| Hand tracking | mediapipe-touchdesigner plugin (Torin Blankensmith) |
| Output | Window COMP fullscreen |

## Equipment (locked by Wave 2026-05-28)

### Space (venue provides)
- Projector ห้องเรียน
- ปลั๊กพ่วง

### Personal (each participant brings)
- Computer
- Adapter

### Workshop Device (Wave brings)
- Webcam — อย่างน้อย 2 ตัว (เพื่อทำ installation), ถ้าเยอะกว่านี้ = หลายคน prototype พร้อมกันได้
- สาย extender for webcam
- Printer
- Scanner

### Workshop Equipment / Consumables (Wave brings)
- Cardboard
- กรรไกร / คัทเตอร์
- Post-it
- สีเทียน
- Marker หลากสี
- กระดาษ

## Physical Build Element (Day 1 morning)

ทีม assemble **cardboard scan station** เอง — tactile warm-up ก่อนเข้าโค้ด:
- Cardboard mount สำหรับวาง webcam มองลง
- Cardboard frame ครอบพื้นที่วาง paper template
- กลายเป็น "ของทีม" — เก็บไว้ใช้ต่อหลัง workshop ได้

= craft + tech ผสมกัน, breaks the "all-screen" workshop format

## Invoice Structure (locked)

- **ในนาม Wave personal** (ไม่เกี่ยว Centerline)
- ค่าวิทยากร 3 วัน × 25,000 = 75,000
- ค่าอุปกรณ์ Physical Prototype = 3,000
- **Total: 78,000 บาท**
- Payment: **100% post Day 3**
- หัก ณ ที่จ่าย 3% ของค่าวิทยากร = 2,250 บาท → รับจริง 75,750 บาท

## 3-Day arc (locked 2026-05-29 — see `workshop-schedule.html`)

- **Day 1 — Concept + Tutorial → Interactive sketches**: concept → TD fundamentals (tutorial หนักๆ) → paint (mouse + feedback) → audio interactive → particle interactive ง่ายๆ. ไต่ทักษะทีละขั้น ไม่กระโดดเข้า ArUco
- **Day 2 — Input Systems & Integration**: MediaPipe (motion) → ArUco + webcam (scan) → เก็บข้อมูล save ลงไฟล์ + auto-load → **Web → Interactive (TD as Server)** (Web Render TOP + Web Server DAT phone-controller + WebSocket/LINE/backend; OSC/Serial แค่กล่าวถึง — ตรง web-stack ของ DDEXP)
- **Day 3 — Real Build**: ทำ mock จริง (stitch ทุกส่วน) → TD UI → installation experience + placemaking → install จริง ทดลองงาน → present

## Day 3 Build Sequence (ภาพรวม)

| Time | Build |
|------|-------|
| เช้า | brief mock → stitch scan→particle→hand เป็นชิ้นเดียว |
| กลางวัน | TD UI / control panel + presets |
| บ่าย | installation experience + placemaking → install จริง ยิง projector ทดลองงาน |
| เย็น | present + retro |

## Optional stretch (ถ้าทีมไหนไวพอ — ไม่บังคับ)

ตัวหลัก = Drawing → particle fullscreen + **hand swipe** (ทุกทีมทำตัวนี้)

Stretch สำหรับทีมที่เสร็จเร็ว: เปลี่ยนจาก hand pose → **body pose**, particle emit ตามรูปร่างคน (body silhouette). ไม่ใช่ deliverable หลัก — เป็นของแถมให้คนที่ไวพอลองต่อ

## Open questions

- [ ] Particle method A vs B — เลือกอันไหนสอน Day 2 (B meaningful กว่าแต่ยากกว่า)
- [ ] Archive scope — แค่ PNG, หรือมี gallery UI ด้วย?
- [ ] Template design — กี่ ArUco IDs, ขนาดกระดาษ, layout?
- [ ] Scan trigger — auto (file watch) หรือ manual button?
