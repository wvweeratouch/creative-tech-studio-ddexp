# generate_markers.py — สร้าง marker 4 อัน (ID 0-3) สำหรับติดมุมกระดาษ
# รันนอก TD ได้เลย (เครื่องไหนก็ได้ที่มี opencv):  pip install opencv-contrib-python
#   python generate_markers.py     -> ได้ marker_0.png .. marker_3.png เอาไปพิมพ์
#
# วาง: ID0=บนซ้าย  ID1=บนขวา  ID2=ล่างขวา  ID3=ล่างซ้าย  (ตรงกับ order ใน aruco_scriptop.py)
import cv2
import numpy as np

DICT    = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
SIDE_PX = 600          # ขนาด marker (px) — พิมพ์ใหญ่ ๆ ~3-4 ซม. บนกระดาษ
QUIET   = 120          # ขอบขาว (quiet zone) รอบ marker — จำเป็น! ไม่งั้น detect ไม่ติด

for marker_id in range(4):
    img = cv2.aruco.generateImageMarker(DICT, marker_id, SIDE_PX)   # OpenCV >= 4.7
    img = cv2.copyMakeBorder(img, QUIET, QUIET, QUIET, QUIET,
                             cv2.BORDER_CONSTANT, value=255)         # เติม quiet zone
    cv2.imwrite(f"marker_{marker_id}.png", img)
print("wrote marker_0.png .. marker_3.png — print + ติดมุมกระดาษ ID0=TL,1=TR,2=BR,3=BL")
