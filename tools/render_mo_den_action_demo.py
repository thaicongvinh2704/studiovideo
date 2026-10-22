"""Render a 15-second animated action demo of Mỏ Đen acting inside scenes.

Features:
- Mỏ Đen lip sync (phonetic visemes from H narration excerpt).
- Dynamic movement, scene transitions, and expressive gestures (explaining, pointing, thinking, shrugging).
- Gaze tracking, head tilts, tail wagging, natural blinking, and hop/bounce physics.
- Real Maya backgrounds and water filtration diagram from project assets.
- Fixed-length two-bone forelimb IK (55px / 50px) preserving character standards.
- Preserves all original assets and custom H narration.
"""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import time
import wave

import numpy as np
from PIL import Image, ImageFilter
from scipy.ndimage import gaussian_filter1d
from PySide6.QtCore import Qt, QPointF, QRectF
from PySide6.QtGui import (QColor, QFont, QFontDatabase, QGuiApplication, QImage,
                            QLinearGradient, QPainter, QPainterPath, QPainterPathStroker,
                            QPen, QRadialGradient)

ROOT = Path(__file__).resolve().parents[1]
WORK_ARTICULATED = ROOT / "projects/mo_den_motion_demo/articulated_v3"
WORK_BASE = ROOT / "projects/mo_den_motion_demo"
OUT = ROOT / "outputs/mo_den_action_demo_15s"
LIBRARY = ROOT / "assets/characters/mo_den"

FPS = 30
DURATION_SECONDS = 15.0
TOTAL_FRAMES = 450
CANVAS_SIZE = (1920, 1080)
INK = QColor("#080807")

# Arm IK configuration (anchored to 1024x1024 cat local coordinates)
ARM_CONFIG = {
    "left": {
        "shoulder": (410.0, 644.0),
        "wrist": (419.0, 716.0),
        "pole": 1.0,
        "paw_box": (382, 682, 487, 785)
    },
    "right": {
        "shoulder": (623.0, 644.0),
        "wrist": (591.0, 718.0),
        "pole": -1.0,
        "paw_box": (515, 683, 619, 788)
    }
}

SHAPES = {
    "X": (108, 0, 0),
    "A": (102, 2, 0),
    "B": (123, 20, 0.8),
    "C": (119, 47, 0.25),
    "D": (130, 87, 0.1),
    "E": (75, 65, 0.05),
    "F": (53, 47, 0.05),
    "G": (110, 15, 0.9),
    "H": (110, 37, 0.12)
}


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def save_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def smooth(a, b, value):
    val = np.clip((value - a) / (b - a), 0.0, 1.0)
    return val * val * (3.0 - 2.0 * val)


def key_value(keys, t):
    for (a, va), (b, vb) in zip(keys, keys[1:]):
        if a <= t <= b:
            s = float(smooth(a, b, t))
            return va + (vb - va) * s
    return keys[0][1] if t < keys[0][0] else keys[-1][1]


def to_pil(image):
    rgba = image.convertToFormat(QImage.Format.Format_RGBA8888)
    return Image.frombytes("RGBA", (rgba.width(), rgba.height()), bytes(rgba.constBits()))


def to_qimage(image):
    raw = image.tobytes()
    return QImage(raw, image.width, image.height, image.width * 4,
                  QImage.Format.Format_RGBA8888).copy()


def elbow_at(shoulder, wrist, pole, upper=55.0, lower=50.0):
    direction = wrist - shoulder
    distance = float(np.linalg.norm(direction))
    if not (abs(upper - lower) + 1.0 < distance < upper + lower - 1.0):
        # Graceful clamp to keep distance strictly valid
        target_dist = np.clip(distance, abs(upper - lower) + 1.5, upper + lower - 1.5)
        direction = direction / distance * target_dist
        wrist = shoulder + direction
        distance = target_dist
    unit = direction / distance
    along = (upper * upper - lower * lower + distance * distance) / (2.0 * distance)
    height = math.sqrt(max(0.0, upper * upper - along * along))
    elbow = shoulder + unit * along + np.array([-unit[1], unit[0]]) * height * pole
    return elbow, wrist


def polyline(points):
    p = QPainterPath(QPointF(*points[0]))
    for pt in points[1:]:
        p.lineTo(*pt)
    return p


def eye_path(side, opened=1.0):
    if side == "left":
        points = [(754, 802), (809, 780), (889, 754), (936, 784),
                  (953, 832), (946, 882), (900, 904),
                  (852, 925), (804, 911), (779, 886),
                  (762, 861), (756, 832), (754, 802)]
        center = lambda x: 847.0 - 0.10 * (x - 846.0)
    else:
        points = [(1098, 761), (1145, 735), (1227, 707), (1278, 734),
                  (1299, 780), (1283, 837), (1235, 860),
                  (1189, 882), (1143, 875), (1115, 844),
                  (1101, 820), (1098, 791), (1098, 761)]
        center = lambda x: 803.0 - 0.14 * (x - 1192.0)
    points = [(x, center(x) + (y - center(x)) * opened) for x, y in points]
    path = QPainterPath(QPointF(*points[0]))
    for i in range(1, len(points), 3):
        path.cubicTo(QPointF(*points[i]), QPointF(*points[i + 1]), QPointF(*points[i + 2]))
    path.closeSubpath()
    return path


def original_mouth():
    path = QPainterPath(QPointF(985, 970))
    path.cubicTo(1001, 977, 1018, 969, 1033, 963)
    path.cubicTo(1054, 970, 1073, 966, 1089, 959)
    return path


def draw_mouth(painter, width, height, teeth):
    painter.setPen(QPen(INK, 10, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap,
                        Qt.PenJoinStyle.RoundJoin))
    if height < 3.5:
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(original_mouth())
        return
    cx, cy = 1038, 958
    path = QPainterPath(QPointF(cx - width / 2.0, cy))
    path.cubicTo(cx - width * 0.22, cy + 7, cx + width * 0.21, cy + 5, cx + width / 2.0, cy - 5)
    path.cubicTo(cx + width * 0.50, cy + height * 0.57, cx + width * 0.31, cy + height, cx, cy + height)
    path.cubicTo(cx - width * 0.32, cy + height, cx - width * 0.50, cy + height * 0.5, cx - width / 2.0, cy)
    path.closeSubpath()
    painter.setBrush(QColor("#522522"))
    painter.drawPath(path)
    painter.save()
    painter.setClipPath(path)
    painter.setPen(Qt.PenStyle.NoPen)
    if height > 24:
        painter.setBrush(QColor("#e98e96"))
        painter.drawEllipse(QRectF(cx - width * 0.32, cy + height * 0.63, width * 0.64, height * 0.49))
    if teeth > 0.22:
        painter.setBrush(QColor("#fbefe0"))
        painter.drawRoundedRect(QRectF(cx - width * 0.47, cy - 11, width * 0.94, 12 + teeth * 10), 5, 5)
    painter.restore()
    painter.setBrush(Qt.BrushStyle.NoBrush)
    painter.setPen(QPen(INK, 10, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap,
                        Qt.PenJoinStyle.RoundJoin))
    painter.drawPath(path)


def blink(t):
    closed = 0.0
    for center in (0.45, 1.85, 3.65, 5.85, 8.40, 10.90, 13.50):
        if center - 0.09 <= t <= center:
            amount = float(smooth(center - 0.09, center, t))
        elif center < t <= center + 0.025:
            amount = 1.0
        elif center + 0.025 < t <= center + 0.17:
            amount = 1.0 - float(smooth(center + 0.025, center + 0.17, t))
        else:
            amount = 0.0
        closed = max(closed, amount)
    return 1.0 - closed


class MouthTrack:
    def __init__(self):
        cues_path = WORK_BASE / "mouth_cues_raw.json"
        document = json.loads(cues_path.read_text(encoding="utf-8"))
        self.cues = document["mouthCues"]
        self.times = np.arange(int(DURATION_SECONDS * 1000) + 1) / 1000.0
        values = np.tile(np.array(SHAPES["X"], float), (len(self.times), 1))
        for cue in self.cues:
            selected = (self.times >= cue["start"]) & (self.times < cue["end"])
            values[selected] = SHAPES[cue["value"]]
        self.values = gaussian_filter1d(values, sigma=22, axis=0, mode="nearest")

        wav_path = WORK_BASE / "audio_H_excerpt_15s.wav"
        with wave.open(str(wav_path)) as stream:
            rate = stream.getframerate()
            samples = np.frombuffer(stream.readframes(stream.getnframes()), dtype="<i2").astype(float) / 32768.0
        win = round(rate * 0.01)
        envelope = np.sqrt(np.mean(samples[:len(samples) // win * win].reshape(-1, win) ** 2, axis=1))
        self.envelope = gaussian_filter1d(envelope, sigma=2)
        self.envelope_time = np.arange(len(envelope)) * 0.01 + 0.005

    def at(self, t):
        v = np.array([np.interp(t, self.times, self.values[:, i]) for i in range(3)])
        rms = float(np.interp(t, self.envelope_time, self.envelope))
        gate = float(smooth(0.002, 0.018, rms))
        v[1] *= gate * (0.65 + 0.35 * float(smooth(0.015, 0.09, rms)))
        v[2] *= gate
        return v


# Trajectories across the 4 beats
# Left arm track: (time, dx, dy)
TRACK_LEFT = [
    (0.0, 0.0, 0.0),
    (3.2, 0.0, 0.0),
    (3.8, -26.0, -18.0),   # Beat 2: Pointing up-left towards water filtration graphic
    (6.8, -26.0, -18.0),
    (7.4, 0.0, 0.0),
    (8.0, 16.0, -24.0),    # Beat 3: Hand to chin (thinking / puzzled)
    (10.5, 16.0, -24.0),
    (11.0, 0.0, 0.0),
    (11.8, -25.0, -15.0),  # Beat 4: Shrug gesture outward
    (14.2, -25.0, -15.0),
    (14.8, -6.0, -4.0),
    (15.0, -6.0, -4.0)
]

# Right arm track: (time, dx, dy)
TRACK_RIGHT = [
    (0.0, 0.0, 0.0),
    (0.9, 0.0, 0.0),
    (1.7, 24.0, -16.0),    # Beat 1: Pointing right towards temple
    (2.6, 24.0, -16.0),
    (3.2, 0.0, 0.0),
    (3.8, 8.0, -4.0),      # Beat 2: Arm resting slightly on hip
    (7.4, 8.0, -4.0),
    (8.0, 0.0, 4.0),       # Beat 3: Supporting arm lowered
    (10.5, 0.0, 4.0),
    (11.0, 0.0, 0.0),
    (11.8, 25.0, -15.0),   # Beat 4: Shrug gesture outward
    (14.2, 25.0, -15.0),
    (14.8, 6.0, -4.0),
    (15.0, 6.0, -4.0)
]

# Head tilt & rotation: (time, degrees)
HEAD_KEYS = [
    (0.0, 0.0),
    (0.8, 2.5),
    (1.6, 2.0),
    (2.6, -1.0),
    (3.2, 0.0),
    (4.2, -3.0),
    (5.4, 2.0),
    (6.6, -2.0),
    (7.4, 0.0),
    (8.2, -4.5),   # Beat 3: Thoughtful tilt
    (9.6, -3.5),
    (10.8, -1.0),
    (11.6, 3.0),   # Beat 4: Questioning wobble
    (12.8, -2.5),
    (13.8, 2.0),
    (14.6, 0.0),
    (15.0, 0.0)
]

# Eye gaze offset: (time, dx, dy)
GAZE_KEYS = [
    (0.0, 14.0, -4.0),   # Looking right at temple
    (0.8, 14.0, -4.0),
    (1.2, 0.0, 0.0),     # Look at viewer
    (3.2, 0.0, 0.0),
    (3.8, -12.0, -4.0),  # Look at water graphic
    (5.8, -12.0, -4.0),
    (6.4, 0.0, 0.0),     # Look at viewer
    (7.5, 0.0, 0.0),
    (8.2, -6.0, 6.0),    # Look down/inward (puzzled)
    (10.2, -6.0, 6.0),
    (10.8, 0.0, 0.0),    # Look at viewer
    (15.0, 0.0, 0.0)
]

# Character Position X, Y and Scale on 1920x1080 canvas
CAT_X_KEYS = [
    (0.0, 220.0),
    (3.2, 220.0),
    (3.8, 1180.0),  # Hop across to right
    (7.4, 1180.0),
    (8.0, 680.0),   # Hop to center-left
    (10.9, 680.0),
    (11.8, 520.0),  # Step forward close-up
    (15.0, 520.0)
]

CAT_Y_KEYS = [
    (0.0, 390.0),
    (3.2, 390.0),
    (3.8, 390.0),
    (7.4, 390.0),
    (8.0, 390.0),
    (10.9, 390.0),
    (11.8, 280.0),  # Move up for closer framing
    (15.0, 280.0)
]

CAT_SCALE_KEYS = [
    (0.0, 0.65),
    (3.2, 0.65),
    (3.8, 0.65),
    (7.4, 0.65),
    (8.0, 0.65),
    (10.9, 0.65),
    (11.8, 0.78),  # Closer framing in Beat 4
    (15.0, 0.78)
]


class AnimatedMoDen:
    def __init__(self, original, cleaned, track):
        self.original = original
        self.cleaned = cleaned
        self.track = track

        # Load separate layers
        self.layers = {
            "body": QImage(str(WORK_BASE / "rigid_v2/body.png")),
            "feet": QImage(str(WORK_BASE / "rigid_v2/feet.png")),
            "tail": QImage(str(WORK_BASE / "rigid_v2/tail.png")),
            "left_paw": QImage(str(WORK_ARTICULATED / "left_supplied_paw.png")),
            "right_paw": QImage(str(WORK_ARTICULATED / "right_supplied_paw.png"))
        }

        # Head mask
        head_path = QPainterPath(QPointF(0, 0))
        for segment in [(1024, 0), (1024, 560), (690, 560),
                        (666, 581, 630, 588, 612, 588), (604, 616),
                        (426, 616), (422, 593),
                        (355, 592, 322, 579, 300, 560), (0, 560)]:
            if len(segment) == 2:
                head_path.lineTo(*segment)
            else:
                head_path.cubicTo(*segment)
        head_path.closeSubpath()
        self.head_mask = head_path

    def geometry(self, side, t):
        config = ARM_CONFIG[side]
        track = TRACK_LEFT if side == "left" else TRACK_RIGHT
        shoulder = np.array(config["shoulder"], float)
        wrist_target = np.array(config["wrist"], float) + np.array([
            key_value([(a, x) for a, x, y in track], t),
            key_value([(a, y) for a, x, y in track], t)
        ])
        elbow, wrist = elbow_at(shoulder, wrist_target, config["pole"])
        disp_x = key_value([(a, x) for a, x, y in track], max(0.0, t - 0.11))
        angle = float(disp_x) * 0.22
        return shoulder, elbow, wrist, angle

    def draw_arm(self, painter, side, t):
        shoulder, elbow, wrist, angle = self.geometry(side, t)
        centerline = QPainterPath(QPointF(*shoulder))
        centerline.quadTo(QPointF(*elbow), QPointF(*wrist))

        stroker = QPainterPathStroker()
        stroker.setWidth(59)
        stroker.setCapStyle(Qt.PenCapStyle.RoundCap)
        stroker.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        outline = stroker.createStroke(centerline).simplified()

        gradient = QLinearGradient(390, 630, 630, 750)
        gradient.setColorAt(0, self.layers["body"].pixelColor(425, 640))
        gradient.setColorAt(1, self.layers["body"].pixelColor(590, 740))

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(gradient)
        painter.drawPath(outline)

        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(INK, 8.5, Qt.PenStyle.SolidLine,
                            Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))

        a = np.linspace(0, 1, 60)[:, None]
        center = (1 - a) ** 2 * shoulder + 2 * (1 - a) * a * elbow + a * a * wrist
        tangent = 2 * (1 - a) * (elbow - shoulder) + 2 * a * (wrist - elbow)
        normal = np.stack([-tangent[:, 1], tangent[:, 0]], axis=1)
        normal /= np.linalg.norm(normal, axis=1)[:, None]
        edge = center + normal * 29.5 * (1 if side == "left" else -1)
        painter.drawPath(polyline(edge))

        # Crease connection
        rest = ARM_CONFIG[side]["wrist"]
        radians = math.radians(angle)
        rotate = np.array([[math.cos(radians), -math.sin(radians)],
                           [math.sin(radians), math.cos(radians)]])
        contact = np.array((443, 691) if side == "left" else (568, 691), float)
        contact = wrist + rotate @ (contact - np.array(rest))
        crease_start = shoulder + np.array((22, 11) if side == "left" else (-33, 6))
        crease = QPainterPath(QPointF(*crease_start))
        crease.quadTo(QPointF(float(crease_start[0]), float(contact[1])), QPointF(*contact))
        painter.drawPath(crease)

        # Draw paw
        paw_img = self.layers[f"{side}_paw"]
        painter.save()
        painter.translate(float(wrist[0]), float(wrist[1]))
        painter.rotate(angle)
        painter.translate(-rest[0], -rest[1])
        painter.drawImage(0, 0, paw_img)
        painter.restore()

    def face_at(self, t):
        image = self.cleaned.copy()
        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        painter.scale(0.5, 0.5)

        opened = blink(t)
        gaze_x = key_value([(a, x) for a, x, y in GAZE_KEYS], t)
        gaze_y = key_value([(a, y) for a, x, y in GAZE_KEYS], t)

        for side in ("left", "right"):
            path = eye_path(side, max(0.015, opened))
            painter.save()
            painter.setClipPath(path)
            # Offset original image to move pupils inside eye sockets
            painter.drawImage(int(round(gaze_x)), int(round(gaze_y)), self.original)
            painter.restore()
            if opened < 0.99:
                painter.setPen(QPen(INK, 9, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap,
                                    Qt.PenJoinStyle.RoundJoin))
                painter.setBrush(Qt.BrushStyle.NoBrush)
                painter.drawPath(path)

        draw_mouth(painter, *self.track.at(t))
        painter.end()
        return to_qimage(to_pil(image))

    def render_cat_sprite(self, t):
        image = QImage(1024, 1024, QImage.Format.Format_ARGB32_Premultiplied)
        image.fill(Qt.GlobalColor.transparent)
        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        # 1. Tail with lively sin-wave wag
        tail_angle = 4.5 * math.sin(t * 2.2) + 1.5 * math.sin(t * 4.4)
        painter.save()
        painter.translate(708, 840)
        painter.rotate(tail_angle)
        painter.translate(-708, -840)
        painter.drawImage(0, 0, self.layers["tail"])
        painter.restore()

        # 2. Body and Feet
        painter.drawImage(0, 0, self.layers["body"])
        painter.drawImage(0, 0, self.layers["feet"])

        # 3. Two-bone Forelimbs
        self.draw_arm(painter, "left", t)
        self.draw_arm(painter, "right", t)

        # 4. Animated Face with Head Tilt
        face = self.face_at(t)
        # Cutout head
        head_img = QImage(1024, 1024, QImage.Format.Format_ARGB32_Premultiplied)
        head_img.fill(Qt.GlobalColor.transparent)
        hp = QPainter(head_img)
        hp.setRenderHint(QPainter.RenderHint.Antialiasing)
        hp.setClipPath(self.head_mask)
        hp.drawImage(0, 0, face)
        hp.end()

        # Soft neck blend
        arr = np.array(to_pil(head_img))
        yy = np.arange(1024)[:, None]
        arr[:, :, 3] = (arr[:, :, 3] * (1.0 - smooth(594, 618, yy))).astype(np.uint8)
        soft_head = to_qimage(Image.fromarray(arr))

        head_angle = key_value(HEAD_KEYS, t)
        painter.save()
        painter.translate(516, 596)
        painter.rotate(head_angle)
        painter.translate(-516, -596)
        painter.drawImage(0, 0, soft_head)
        painter.restore()

        painter.end()
        return image


# Subtitles specification
SUBTITLES = [
    (0.55, 3.10, "Giữa rừng nhiệt đới, những ngôi đền vẫn đứng đó."),
    (3.20, 7.45, "Người xây chúng biết quan sát bầu trời, trữ nước, thậm chí dùng khoáng vật để lọc nước uống."),
    (7.55, 10.75, "Vậy mà rồi, nhiều người vẫn phải rời thành phố."),
    (10.85, 14.75, "Nếu đã làm được từng ấy việc, vì sao họ không thể tiếp tục sống ở đây?")
]


class SceneDirector:
    def __init__(self):
        # Backgrounds
        bg1_path = ROOT / "assets/reusable/mo_den/maya_48/Mo_Den_Maya_48_Anh_151_198_v1/01_boi_canh/quyen_luc/178_quyen_luc_duoc_duy_tri.png"
        bg2_path = ROOT / "assets/reusable/mo_den/maya_48/Mo_Den_Maya_48_Anh_151_198_v1/01_boi_canh/ho_chua/157_ho_chua_day_nuoc.png"
        bg3_path = ROOT / "assets/reusable/mo_den/maya_48/Mo_Den_Maya_48_Anh_151_198_v1/01_boi_canh/do_thi/152_do_thi_xuong_cap.png"
        diag_path = ROOT / "projects/mo_den_maya/source_materials/Mo_Den_Maya_Tu_Lieu_That_Va_Phan_Canh_v1/02_Do_hoa_SVG_PNG/G03_Nuoc_Tikal.png"

        self.bg1 = QImage(str(bg1_path)).scaled(1920, 1080, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
        self.bg2 = QImage(str(bg2_path)).scaled(1920, 1080, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
        self.bg3 = QImage(str(bg3_path)).scaled(1920, 1080, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
        self.diag = QImage(str(diag_path)).scaled(920, 518, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

        self.font = QFont("Segoe UI Semibold", 27)

    def draw_background(self, painter, t):
        # Beat 1: 0.0 -> 3.2s
        # Beat 2: 3.2 -> 7.5s
        # Beat 3: 7.5 -> 11.0s
        # Beat 4: 11.0 -> 15.0s
        if t < 3.2:
            # Beat 1: Temple with subtle slow pan
            pan_x = int(-20 + t * 6)
            painter.drawImage(pan_x, 0, self.bg1)
        elif t < 7.5:
            # Beat 2: Water reservoir + diagram card
            painter.drawImage(0, 0, self.bg2)
            # Tint overlay for diagram readability
            painter.fillRect(0, 0, 1920, 1080, QColor(20, 25, 22, 60))

            # Filtration diagram card on the left
            diag_x, diag_y = 110, 160
            painter.save()
            card_rect = QRectF(diag_x - 10, diag_y - 10, 940, 538)
            painter.setPen(QPen(QColor(0, 0, 0, 80), 2))
            painter.setBrush(QColor(250, 247, 239, 235))
            painter.drawRoundedRect(card_rect, 16, 16)
            painter.drawImage(diag_x, diag_y, self.diag)
            painter.restore()
        elif t < 11.0:
            # Beat 3: Decaying city
            painter.drawImage(0, 0, self.bg3)
            # Soft melancholy grading
            painter.fillRect(0, 0, 1920, 1080, QColor(45, 30, 20, 55))
        else:
            # Beat 4: Dramatic close-up with pyramid in background and soft depth-of-field vignette
            painter.save()
            # Zoom into the pyramid background for cinematic framing
            painter.translate(-192, -108)
            painter.scale(1.2, 1.2)
            painter.drawImage(0, 0, self.bg3)
            painter.restore()

            # Atmospheric cinematic vignette emphasizing Mỏ Đen
            grad = QRadialGradient(QPointF(960, 500), 850)
            grad.setColorAt(0.0, QColor(0, 0, 0, 30))
            grad.setColorAt(0.65, QColor(25, 20, 15, 90))
            grad.setColorAt(1.0, QColor(10, 8, 5, 190))
            painter.fillRect(0, 0, 1920, 1080, grad)

    def draw_subtitles(self, painter, t):
        current_text = None
        for start, end, text in SUBTITLES:
            if start <= t <= end:
                current_text = text
                break

        if not current_text:
            return

        painter.save()
        painter.setFont(self.font)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)

        metrics = painter.fontMetrics()
        text_width = metrics.horizontalAdvance(current_text)
        text_height = metrics.height()

        box_width = text_width + 60
        box_height = text_height + 24
        box_x = (1920 - box_width) / 2.0
        box_y = 960.0

        # Semi-transparent pill background
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(15, 15, 18, 205))
        painter.drawRoundedRect(QRectF(box_x, box_y, box_width, box_height), box_height / 2.0, box_height / 2.0)

        # Crisp white text with subtle shadow
        painter.setPen(QColor(0, 0, 0, 160))
        painter.drawText(QRectF(box_x, box_y + 2, box_width, box_height), Qt.AlignmentFlag.AlignCenter, current_text)
        painter.setPen(QColor(255, 255, 255, 245))
        painter.drawText(QRectF(box_x, box_y, box_width, box_height), Qt.AlignmentFlag.AlignCenter, current_text)
        painter.restore()

    def render_frame(self, cat, t):
        frame = QImage(1920, 1080, QImage.Format.Format_RGB32)
        painter = QPainter(frame)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        # 1. Background scene
        self.draw_background(painter, t)

        # 2. Character Position & Hop Physics
        base_x = key_value(CAT_X_KEYS, t)
        base_y = key_value(CAT_Y_KEYS, t)
        scale = key_value(CAT_SCALE_KEYS, t)

        # Hop / bounce curves during moves
        hop_y = 0.0
        squash_x, squash_y = 1.0, 1.0
        if 3.2 <= t <= 3.8:
            phase = (t - 3.2) / 0.6
            hop_y = -math.sin(phase * math.pi) * 55.0
            squash_x = 1.0 + 0.08 * math.sin(phase * math.pi)
            squash_y = 1.0 - 0.08 * math.sin(phase * math.pi)
        elif 7.4 <= t <= 8.0:
            phase = (t - 7.4) / 0.6
            hop_y = -math.sin(phase * math.pi) * 45.0
            squash_x = 1.0 + 0.06 * math.sin(phase * math.pi)
            squash_y = 1.0 - 0.06 * math.sin(phase * math.pi)
        elif 10.9 <= t <= 11.6:
            phase = (t - 10.9) / 0.7
            hop_y = -math.sin(phase * math.pi) * 35.0
            squash_x = 1.0 + 0.05 * math.sin(phase * math.pi)
            squash_y = 1.0 - 0.05 * math.sin(phase * math.pi)
        else:
            # Idle breathing bob
            hop_y = math.sin(t * 3.2) * 3.0

        # Contact shadow beneath cat
        shadow_cx = base_x + 512 * scale
        shadow_cy = base_y + 880 * scale + hop_y * 0.2
        painter.save()
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(10, 12, 10, int(70 * (1.0 - abs(hop_y) / 90.0))))
        painter.drawEllipse(QPointF(shadow_cx, shadow_cy), 180 * scale, 28 * scale)
        painter.restore()

        # Render Mỏ Đen sprite
        cat_sprite = cat.render_cat_sprite(t)

        painter.save()
        painter.translate(base_x + 512 * scale, base_y + 512 * scale + hop_y)
        painter.scale(scale * squash_x, scale * squash_y)
        painter.translate(-512, -512)
        painter.drawImage(0, 0, cat_sprite)
        painter.restore()

        # 3. Synchronized Subtitles
        self.draw_subtitles(painter, t)

        painter.end()
        return frame


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--previews-only", action="store_true")
    args = parser.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

    app = QGuiApplication.instance() or QGuiApplication([])
    for filename in ("segoeui.ttf", "seguisb.ttf"):
        font_path = Path("C:/Windows/Fonts") / filename
        if font_path.exists():
            QFontDatabase.addApplicationFont(str(font_path))

    manifest = json.loads((LIBRARY / "manifest.json").read_text(encoding="utf-8"))
    entry = next(a for a in manifest["assets"] if a["id"] == "mo_den_01")
    source = LIBRARY / entry["file"]
    if sha(source) != entry["sha256"]:
        raise RuntimeError("Supplied original changed; refusing to use mismatched identity.")

    original = QImage(str(source))
    cleaned = QImage(str(WORK_BASE / "face_clean_derivative.png")).scaled(
        1024, 1024, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)

    track = MouthTrack()
    cat = AnimatedMoDen(original, cleaned, track)
    director = SceneDirector()

    # Previews at key storytelling moments
    preview_times = [0.4, 1.8, 2.8, 3.5, 4.8, 6.2, 7.7, 9.2, 10.4, 11.5, 12.8, 14.5]
    sheet = Image.new("RGB", (1920, 810), "#faf7ef")
    for i, t in enumerate(preview_times):
        frame = director.render_frame(cat, t)
        frame.save(str(OUT / f"preview_{t:05.2f}.png"))
        pil_frame = to_pil(frame).resize((480, 270), Image.Resampling.LANCZOS)
        sheet.paste(pil_frame, ((i % 4) * 480, (i // 4) * 270))
    sheet.save(OUT / "contact_sheet.jpg", quality=94)

    if args.previews_only:
        print("Previews rendered successfully.", flush=True)
        return

    # Verify bone lengths for all 450 frames
    bone_evidence = []
    for f in range(TOTAL_FRAMES):
        t = f / FPS
        for side in ARM_CONFIG:
            shoulder, elbow, wrist, angle = cat.geometry(side, t)
            upper_len = float(np.linalg.norm(elbow - shoulder))
            lower_len = float(np.linalg.norm(wrist - elbow))
            if not np.allclose([upper_len, lower_len], [55.0, 50.0], atol=1e-5):
                raise RuntimeError(f"Bone stretch violation on frame {f} ({side}): {[upper_len, lower_len]}")
            bone_evidence.append({
                "frame": f,
                "side": side,
                "lengths": [upper_len, lower_len]
            })

    # Render full MP4 video
    video_path = OUT / "Mo_Den_action_demo_15s.mp4"
    audio_path = WORK_BASE / "audio_H_excerpt_15s.wav"

    command = [
        "C:\\Users\\ADMIN\\ffmpeg\\bin\\ffmpeg.exe",
        "-v", "error", "-y",
        "-f", "rawvideo",
        "-pixel_format", "rgb32",
        "-video_size", "1920x1080",
        "-framerate", "30",
        "-i", "pipe:0",
        "-i", str(audio_path),
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-t", "15",
        "-movflags", "+faststart",
        str(video_path)
    ]

    started = time.monotonic()
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    try:
        for f in range(TOTAL_FRAMES):
            t = f / FPS
            frame = director.render_frame(cat, t)
            process.stdin.write(bytes(frame.constBits()))
            if f % 90 == 0:
                print(f"Render frame {f}/{TOTAL_FRAMES}: {time.monotonic() - started:.1f}s", flush=True)
        process.stdin.close()
        if process.wait() != 0:
            raise RuntimeError("FFmpeg encoding failed.")
    except BaseException:
        process.kill()
        process.wait()
        raise

    render_dur = round(time.monotonic() - started, 2)
    print(f"Video encoded successfully in {render_dur}s -> {video_path}", flush=True)

    manifest_data = {
        "role": "character",
        "kind": "animated_character_action_demo_15s",
        "source": str(source.relative_to(ROOT)),
        "source_sha256": sha(source),
        "source_preserved": True,
        "video": str(video_path.relative_to(ROOT)),
        "video_sha256": sha(video_path),
        "audio": str(audio_path.relative_to(ROOT)),
        "audio_sha256": sha(audio_path),
        "speaker": "custom H, Northern Vietnamese, 1.25x (preserved)",
        "fps": 30,
        "frames": 450,
        "duration_seconds": 15.0,
        "resolution": [1920, 1080],
        "render_seconds": render_dur,
        "features": [
            "Vietnamese lip sync matching custom H narration",
            "Storytelling gestures: pointing, explaining, thinking, shrugging",
            "Pupil gaze tracking & organic blinking",
            "Animated character motion & hop physics across 4 story beats",
            "Actual Maya backgrounds and water filtration diagram",
            "Synchronized styled subtitles"
        ]
    }
    save_json(OUT / "manifest.json", manifest_data)


if __name__ == "__main__":
    main()
