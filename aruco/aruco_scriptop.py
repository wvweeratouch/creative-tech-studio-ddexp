# aruco_scriptop.py — วางใน Script TOP DAT (TouchDesigner 2023.1+, OpenCV 4.8 bundled)
# Network:  Video Device In TOP (webcam, RGBA) -> Script TOP (โค้ดนี้) -> Out / viewer
# ตั้ง Script TOP: Common page -> Resolution = 1024 x 1024
#
# ทำอะไร: หา ArUco marker 4 อันมุมกระดาษ -> คำนวณ homography -> warp ภาพให้ตรง (top-down)
# verified: docs.derivative.ca (Script_TOP, TOP_Class, OpenCV) + docs.opencv.org (aruco 4.x)

import numpy as np
import cv2

OUT_W = OUT_H = 1024
ARUCO_DICT = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

# build detector ครั้งเดียวตอน load (ArucoDetector ไม่ฟรี — อย่าสร้างทุก cook)
_params   = cv2.aruco.DetectorParameters()
_detector = cv2.aruco.ArucoDetector(ARUCO_DICT, _params)

# ปลายทาง 4 มุม — order ต้องตรงกับ order_by_id(): [TL, TR, BR, BL]
_DST = np.array([[0,         0],
                 [OUT_W - 1, 0],
                 [OUT_W - 1, OUT_H - 1],
                 [0,         OUT_H - 1]], dtype=np.float32)

# fallback: เก็บ warp ล่าสุด เพื่อไม่ให้จอดำเวลา marker หลุดเฟรม
_last_good = np.full((OUT_H, OUT_W, 3), 0.15, dtype=np.float32)


def order_by_id(corners, ids):
    """คืน src points [TL, TR, BR, BL] = marker ID [0,1,2,3] โดยใช้ "center" ของแต่ละ marker
    (center นิ่งกว่ามุม ไม่ต้องสน orientation). คืน None ถ้า ID 0..3 ไม่ครบ."""
    if ids is None:
        return None
    centers = {}
    for marker_corners, marker_id in zip(corners, ids.flatten()):
        centers[int(marker_id)] = marker_corners.reshape(4, 2).mean(axis=0)
    if not all(k in centers for k in (0, 1, 2, 3)):
        return None
    return np.array([centers[0], centers[1], centers[2], centers[3]], dtype=np.float32)


def onCook(scriptOp):
    global _last_good

    # 1) input: TD ให้ float32 RGBA 0..1 shape (H,W,4) origin "ล่างซ้าย"
    src = scriptOp.inputs[0].numpyArray()          # NOTE: ไม่มี delImageData — ใช้ () เฉย ๆ
    if src is None:
        scriptOp.copyNumpyArray(_append_alpha(np.flipud(_last_good)))
        return

    # 2) flip: TD ล่างซ้าย -> OpenCV บนซ้าย
    img = np.flipud(src)

    # 3) -> uint8 RGB ให้ OpenCV (อย่า convert BGR — จะ R/B สลับ)
    rgb_u8 = (np.clip(img[:, :, :3], 0.0, 1.0) * 255.0).astype(np.uint8)
    gray   = cv2.cvtColor(rgb_u8, cv2.COLOR_RGB2GRAY)

    # 4) detect (OpenCV >= 4.7 API)
    corners, ids, _rejected = _detector.detectMarkers(gray)
    pts = order_by_id(corners, ids)

    if pts is None:                                # marker < 4 -> ค้างภาพล่าสุด
        scriptOp.copyNumpyArray(_append_alpha(np.flipud(_last_good)))
        return

    # 5) homography + warp -> 1024x1024 (top-down)
    M = cv2.getPerspectiveTransform(pts, _DST)
    warped_u8 = cv2.warpPerspective(rgb_u8, M, (OUT_W, OUT_H))

    # 6) -> float32 0..1, จำเป็น fallback ครั้งถัดไป
    warped_f = warped_u8.astype(np.float32) / 255.0
    _last_good = warped_f

    # 7) flip กลับ -> origin TD, ใส่ alpha, เขียนออก
    scriptOp.copyNumpyArray(_append_alpha(np.flipud(warped_f)))


def _append_alpha(rgb_f32):
    """ใส่ alpha ทึบ -> (H,W,4) float32 ให้ copyNumpyArray"""
    h, w = rgb_f32.shape[:2]
    alpha = np.ones((h, w, 1), dtype=np.float32)
    return np.ascontiguousarray(np.concatenate([rgb_f32, alpha], axis=2))


# ---- DEBUG (เปิดชั่วคราวตอน test ก่อน workshop) ----
# ใส่บรรทัดนี้ใน onCook หลัง detectMarkers เพื่อเช็คว่าเห็น marker ครบไหม:
#   if ids is not None: print("ids:", sorted(int(i) for i in ids.flatten()))
#   else: print("no markers")
# อยากเห็น [0, 1, 2, 3] นิ่ง ๆ — ถ้าไม่ครบ = แสง/ระยะ/quiet zone (ดู README)
