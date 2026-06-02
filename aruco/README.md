# ArUco scan — คู่มือสั้น (Wave อ่านก่อนสอน — ไม่เคยทำมาก่อน)

ทำ "scan รูปจากกระดาษให้ตรง" ด้วย ArUco marker + homography ใน TouchDesigner

## ไฟล์
- `generate_markers.py` — รันนอก TD สร้าง marker 4 อัน (ID 0-3) เอาไปพิมพ์
- `aruco_scriptop.py` — โค้ดวางใน Script TOP (verified, มี fallback ในตัว)

## ✅ ข่าวดี: ไม่ต้องลง OpenCV
TD 2023.1+ มี **OpenCV 4.8 + contrib + Python 3.11** มาให้แล้ว → `import cv2` ได้เลย
เช็คใน Textport: `import cv2; print(cv2.__version__)` ควรเห็น `4.8.0`
และ `print(hasattr(cv2.aruco,'ArucoDetector'))` ควรเห็น `True`
> ถ้าใครเผลอ `pip install opencv-python` ทับ → `cv2.aruco` หาย (ต้องเป็น contrib)

## ⚠️ 3 เรื่องที่พังบ่อยสุด
1. **API เก่า/ใหม่** — ต้องใช้ของใหม่ (≥4.7): `getPredefinedDictionary` / `DetectorParameters()` / `ArucoDetector` / `detectMarkers`.
   โค้ดเก่าจากเน็ต (`Dictionary_get`, `DetectorParameters_create`) **พัง** → error `module 'cv2.aruco' has no attribute 'Dictionary_get'`
2. **Origin flip** — TD origin ล่างซ้าย, OpenCV บนซ้าย → ต้อง `np.flipud` ทั้งขาเข้า-ออก (ลืม = ภาพกลับหัว/มิเรอร์)
3. **dtype / สี** — TD float32 0..1 RGBA → OpenCV uint8 0..255. และ **อย่า convert BGR** (R/B สลับ) — โค้ดนี้ใช้ RGB ตลอด
   - หมายเหตุ: `numpyArray(delImageData=True)` **ไม่มีจริง** — ใช้ `numpyArray()` เฉย ๆ

## marker setup
- **DICT_4X4_50** (cell ใหญ่ detect ง่ายที่ระยะ webcam) — generate กับ detect ต้อง dict เดียวกัน
- ติด 4 มุม: **ID0=บนซ้าย · ID1=บนขวา · ID2=ล่างขวา · ID3=ล่างซ้าย** · วาดตรงกลาง
- ต้องมี **quiet zone** (ขอบขาวรอบ marker) · กระดาษแบน · แสงนุ่มไม่สะท้อน · marker ~3-4 ซม.

## 🧪 Test 15 นาที ก่อน workshop
1. รัน `generate_markers.py` → พิมพ์ → ติดมุมกระดาษ + วาดรูป
2. Textport: เช็ค `cv2.__version__` = 4.8.0
3. ต่อ `Video Device In TOP` → `Script TOP` (paste `aruco_scriptop.py`) → viewer · ตั้ง res 1024x1024
4. เปิด DEBUG (ท้ายไฟล์) → ส่องกระดาษ อยากเห็น `ids: [0,1,2,3]` นิ่ง ๆ
5. ปิด DEBUG → เห็นภาพ flatten · เอียงกระดาษแล้วภาพยังตรง = ผ่าน

## Fallback หน้างาน (มีในโค้ดแล้ว / เตรียมไว้)
1. **marker < 4** → ค้างภาพ scan ล่าสุด (`_last_good`) ไม่ดำวูบ — อยู่ในโค้ดแล้ว
2. **detect ไม่ติดสด** → manual 4-corner pick: แก้แค่ตัวแปร `pts` (warp ไม่สนว่าจุดมาจากไหน)
3. **ฉุกเฉิน** → เปิดรูป pre-warped ที่ทำไว้ก่อน (Movie File In) เล่นบทเรียนต่อ
> พังเพราะ **แสง** มากกว่าโค้ด — เอาไฟ LED แสงนุ่มไปด้วย = ตัวช่วยคุ้มสุด

## ปรับจูน (ถ้า detect ไม่ค่อยติด)
`DetectorParameters()` มีปุ่ม: `adaptiveThreshWinSizeMin/Max/Step` (แสงยาก), `minMarkerPerimeterRate` (marker เล็ก),
`cornerRefinementMethod = cv2.aruco.CORNER_REFINE_SUBPIX` (มุมแม่นขึ้น = homography นิ่ง). default พอสำหรับ tabletop ปกติ

_(ที่มา: docs.derivative.ca Script_TOP/TOP_Class/OpenCV · docs.opencv.org aruco 4.x · verified 2026-06-02)_
