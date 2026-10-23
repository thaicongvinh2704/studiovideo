"""Render a seamless loopable 'Butt & Hip Wiggle Dance' for Mỏ Đen.

Features:
- Perfectly seamless loop cycle of 1.2s (36 frames at 30 fps).
- Front-facing 3/4 view: playful hip sway, bouncy body squash & stretch,
  lively tail whip, pumping front paws (fixed-length 2-bone IK),
  gaze tracking, and joyful cartoon facial expression.
- Multiple export formats:
  * VP9 Transparent WebM (alpha channel) for modern video editors & web.
  * Apple ProRes 4444 MOV (alpha channel) for Premiere/After Effects/DaVinci.
  * Full HD preview MP4 with cheerful stage background and contact shadow.
  * 12-frame contact sheet for immediate inspection.
- Preserves supplied Mỏ Đen original character assets and identity.
"""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import time

import numpy as np
from PIL import Image
from PySide6.QtCore import Qt, QPointF, QRectF
from PySide6.QtGui import (QColor, QFont, QFontDatabase, QGuiApplication, QImage,
                            QLinearGradient, QPainter, QPainterPath, QPainterPathStroker,
                            QPen, QRadialGradient)

ROOT = Path(__file__).resolve().parents[1]
WORK_ARTICULATED = ROOT / "projects/mo_den_motion_demo/articulated_v3"
WORK_BASE = ROOT / "projects/mo_den_motion_demo"
OUT = ROOT / "outputs/mo_den_wiggle_loop"
LIBRARY = ROOT / "assets/characters/mo_den"

FPS = 30
LOOP_SECONDS = 1.2
CYCLE_FRAMES = 36  # 1.2s * 30fps
TOTAL_LOOPS = 8
TOTAL_FRAMES = CYCLE_FRAMES * TOTAL_LOOPS  # 288 frames = 9.6 seconds

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


def to_pil(image):
    rgba = image.convertToFormat(QImage.Format.Format_RGBA8888)
    return Image.frombytes("RGBA", (rgba.width(), rgba.height()), bytes(rgba.constBits()))


def to_qimage(image):
    raw = image.tobytes()
    return QImage(raw, image.width, image.height, image.width * 4,
                  QImage.Format.Format_RGBA8888).copy()


def polyline(points):
    p = QPainterPath(QPointF(*points[0]))
    for pt in points[1:]:
        p.lineTo(*pt)
    return p


def elbow_at(shoulder, wrist, pole, upper=55.0, lower=50.0):
    direction = wrist - shoulder
    distance = float(np.linalg.norm(direction))
    min_d = abs(upper - lower) + 1.5
    max_d = upper + lower - 1.5
    if distance < min_d or distance > max_d:
        target_dist = np.clip(distance, min_d, max_d)
        direction = direction / distance * target_dist
        wrist = shoulder + direction
        distance = target_dist
    unit = direction / distance
    along = (upper * upper - lower * lower + distance * distance) / (2.0 * distance)
    height = math.sqrt(max(0.0, upper * upper - along * along))
    elbow = shoulder + unit * along + np.array([-unit[1], unit[0]]) * height * pole
    return elbow, wrist


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


def draw_happy_mouth(painter, t, omega):
    # A cheerful, bouncy open smile with tongue & teeth
    width = 118.0 + 8.0 * math.sin(omega * t)
    height = 42.0 + 6.0 * math.cos(2.0 * omega * t)
    cx, cy = 1038.0, 958.0

    path = QPainterPath(QPointF(cx - width / 2.0, cy))
    path.cubicTo(cx - width * 0.22, cy + 7, cx + width * 0.21, cy + 5, cx + width / 2.0, cy - 5)
    path.cubicTo(cx + width * 0.50, cy + height * 0.57, cx + width * 0.31, cy + height, cx, cy + height)
    path.cubicTo(cx - width * 0.32, cy + height, cx - width * 0.50, cy + height * 0.5, cx - width / 2.0, cy)
    path.closeSubpath()

    painter.setPen(QPen(INK, 10, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
    painter.setBrush(QColor("#522522"))
    painter.drawPath(path)

    painter.save()
    painter.setClipPath(path)
    painter.setPen(Qt.PenStyle.NoPen)

    # Tongue
    painter.setBrush(QColor("#ea8f97"))
    painter.drawEllipse(QRectF(cx - width * 0.32, cy + height * 0.45, width * 0.64, height * 0.65))

    # Upper little cat teeth
    painter.setBrush(QColor("#fcf1e3"))
    painter.drawRoundedRect(QRectF(cx - width * 0.42, cy - 10, width * 0.84, 18), 5, 5)

    painter.restore()

    painter.setBrush(Qt.BrushStyle.NoBrush)
    painter.setPen(QPen(INK, 10, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
    painter.drawPath(path)


class WiggleCat:
    def __init__(self, original, cleaned):
        self.original = original
        self.cleaned = cleaned

        # Layer cutouts
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

    def draw_arm(self, painter, side, t, omega):
        cfg = ARM_CONFIG[side]
        shoulder = np.array(cfg["shoulder"], float)

        # Cheerful pumping motion of paws in sync with the wiggle
        if side == "left":
            dx = -16.0 - 12.0 * math.cos(omega * t)
            dy = -14.0 + 10.0 * math.sin(2.0 * omega * t)
        else:
            dx = 16.0 + 12.0 * math.cos(omega * t)
            dy = -14.0 - 10.0 * math.sin(2.0 * omega * t)

        wrist_target = np.array(cfg["wrist"], float) + np.array([dx, dy])
        elbow, wrist = elbow_at(shoulder, wrist_target, cfg["pole"])

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
        rest = cfg["wrist"]
        paw_angle = dx * 0.25
        radians = math.radians(paw_angle)
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
        painter.rotate(paw_angle)
        painter.translate(-rest[0], -rest[1])
        painter.drawImage(0, 0, paw_img)
        painter.restore()

    def face_at(self, t, omega):
        image = self.cleaned.copy()
        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        painter.scale(0.5, 0.5)

        # Gaze tracking: eyes sway happily with the hips
        gaze_x = 11.0 * math.sin(omega * t)
        gaze_y = -3.0 + 3.0 * math.cos(2.0 * omega * t)

        # Periodic cheerful blink (occurring exactly once per loop at t=0.6s)
        # Using a smooth Gaussian-like curve that vanishes strictly at loop edges
        blink_dist = (t % LOOP_SECONDS) - 0.60
        blink_val = math.exp(- (blink_dist / 0.05) ** 2) if abs(blink_dist) < 0.12 else 0.0
        opened = 1.0 - blink_val

        for side in ("left", "right"):
            path = eye_path(side, max(0.015, opened))
            painter.save()
            painter.setClipPath(path)
            painter.drawImage(int(round(gaze_x)), int(round(gaze_y)), self.original)
            painter.restore()
            if opened < 0.99:
                painter.setPen(QPen(INK, 9, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap,
                                    Qt.PenJoinStyle.RoundJoin))
                painter.setBrush(Qt.BrushStyle.NoBrush)
                painter.drawPath(path)

        # Cheerful mouth
        draw_happy_mouth(painter, t, omega)

        # Cute pink blush marks on cheeks
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(234, 130, 140, 85))
        painter.drawEllipse(QPointF(780, 930), 45, 25)
        painter.drawEllipse(QPointF(1290, 915), 45, 25)

        painter.end()
        return to_qimage(to_pil(image))

    def render_cat_sprite(self, t):
        omega = 2.0 * math.pi / LOOP_SECONDS

        sprite = QImage(1024, 1024, QImage.Format.Format_ARGB32_Premultiplied)
        sprite.fill(Qt.GlobalColor.transparent)
        painter = QPainter(sprite)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        # --- 1. BOOTY & TAIL WHIP ---
        # The tail sways dramatically in counter-phase to the hips, creating the wiggle gag!
        tail_angle = 32.0 * math.sin(omega * t - math.pi * 0.25) + 6.0 * math.sin(2.0 * omega * t)
        painter.save()
        painter.translate(708, 840)
        painter.rotate(tail_angle)
        painter.translate(-708, -840)
        painter.drawImage(0, 0, self.layers["tail"])
        painter.restore()

        # --- 2. HIP SWAY & TORSO WIGGLE ---
        # Pivot at top of torso/neck (516, 620).
        # Rotating around this pivot makes the hips and belly swing left and right!
        hip_rot = 8.5 * math.sin(omega * t)
        hip_shift_x = 14.0 * math.sin(omega * t)
        bounce_y = -10.0 * (1.0 - math.cos(2.0 * omega * t)) / 2.0

        painter.save()
        painter.translate(516 + hip_shift_x, 620 + bounce_y)
        painter.rotate(hip_rot)
        painter.translate(-516, -620)
        painter.drawImage(0, 0, self.layers["body"])

        # Two-bone Arms attached to moving torso
        self.draw_arm(painter, "left", t, omega)
        self.draw_arm(painter, "right", t, omega)
        painter.restore()

        # --- 3. FEET TAPPING DANCE ---
        # Feet tap rhythmically on the floor
        foot_tap_l = -5.0 * max(0.0, math.sin(omega * t))
        foot_tap_r = -5.0 * max(0.0, -math.sin(omega * t))
        painter.save()
        painter.translate(0, bounce_y * 0.3)
        painter.drawImage(0, int(round(foot_tap_l)), self.layers["feet"])
        painter.restore()

        # --- 4. HEAD COUNTER-BALANCE & HEAD BOB ---
        # Head counter-tilts to keep eyes focused and cute
        face = self.face_at(t, omega)
        head_img = QImage(1024, 1024, QImage.Format.Format_ARGB32_Premultiplied)
        head_img.fill(Qt.GlobalColor.transparent)
        hp = QPainter(head_img)
        hp.setRenderHint(QPainter.RenderHint.Antialiasing)
        hp.setClipPath(self.head_mask)
        hp.drawImage(0, 0, face)
        hp.end()

        # Soft neck edge
        arr = np.array(to_pil(head_img))
        yy = np.arange(1024)[:, None]
        arr[:, :, 3] = (arr[:, :, 3] * (1.0 - np.clip((yy - 594.0) / 24.0, 0.0, 1.0))).astype(np.uint8)
        soft_head = to_qimage(Image.fromarray(arr))

        head_angle = -4.0 * math.sin(omega * t)
        head_shift_x = 4.0 * math.sin(omega * t)
        head_bob_y = 6.0 * math.cos(2.0 * omega * t)

        painter.save()
        painter.translate(516 + head_shift_x, 596 + head_bob_y)
        painter.rotate(head_angle)
        painter.translate(-516, -596)
        painter.drawImage(0, 0, soft_head)
        painter.restore()

        painter.end()
        return sprite


def render_transparent_frame(cat, t, canvas_w=1920, canvas_h=1080, scale=0.75):
    """Render a pristine transparent frame for Alpha channel export."""
    frame = QImage(canvas_w, canvas_h, QImage.Format.Format_ARGB32_Premultiplied)
    frame.fill(Qt.GlobalColor.transparent)
    painter = QPainter(frame)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

    omega = 2.0 * math.pi / LOOP_SECONDS
    # Overall bouncy squash and stretch
    squash_x = 1.0 + 0.04 * math.cos(2.0 * omega * t)
    squash_y = 1.0 - 0.04 * math.cos(2.0 * omega * t)
    hop_y = -8.0 * (1.0 - math.cos(2.0 * omega * t)) / 2.0

    cx = canvas_w / 2.0
    cy = canvas_h / 2.0 + 50.0

    cat_sprite = cat.render_cat_sprite(t)

    painter.save()
    painter.translate(cx, cy + hop_y)
    painter.scale(scale * squash_x, scale * squash_y)
    painter.translate(-512, -512)
    painter.drawImage(0, 0, cat_sprite)
    painter.restore()

    painter.end()
    return frame


def render_preview_frame(cat, t, canvas_w=1920, canvas_h=1080, scale=0.75):
    """Render a cheerful studio preview frame with background, shadow, and musical notes."""
    frame = QImage(canvas_w, canvas_h, QImage.Format.Format_RGB32)
    painter = QPainter(frame)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

    # Cheerful warm studio gradient background
    grad = QLinearGradient(0, 0, 0, canvas_h)
    grad.setColorAt(0.0, QColor("#fffdf7"))
    grad.setColorAt(0.7, QColor("#faeed9"))
    grad.setColorAt(1.0, QColor("#edd5b3"))
    painter.fillRect(0, 0, canvas_w, canvas_h, grad)

    # Subtle radial spotlight
    spot = QRadialGradient(canvas_w / 2.0, canvas_h / 2.0, 700)
    spot.setColorAt(0.0, QColor(255, 255, 255, 120))
    spot.setColorAt(1.0, QColor(255, 255, 255, 0))
    painter.fillRect(0, 0, canvas_w, canvas_h, spot)

    omega = 2.0 * math.pi / LOOP_SECONDS
    cx = canvas_w / 2.0
    cy = canvas_h / 2.0 + 50.0

    # Contact shadow on the floor
    shadow_w = 260.0 * scale * (1.0 + 0.06 * math.cos(2.0 * omega * t))
    shadow_h = 42.0 * scale
    shadow_x = cx + 18.0 * math.sin(omega * t) * scale
    shadow_y = cy + 340.0 * scale

    painter.save()
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QColor(90, 70, 50, 45))
    painter.drawEllipse(QPointF(shadow_x, shadow_y), shadow_w, shadow_h)
    painter.restore()

    # Musical notes & sparkles for playful atmosphere
    for note_i, (nx, ny, nphase, nchar) in enumerate([
        (cx - 380, cy - 140, 0.0, "♪"),
        (cx + 360, cy - 180, 0.6, "♫"),
        (cx - 300, cy + 40, 1.2, "✨"),
        (cx + 340, cy + 60, 1.8, "♪"),
        (cx - 420, cy - 20, 2.4, "♫"),
    ]):
        float_y = 15.0 * math.sin(omega * (t + nphase))
        painter.setFont(QFont("Segoe UI Emoji", 32))
        painter.setPen(QColor(180, 120, 70, 160))
        painter.drawText(QPointF(nx, ny + float_y), nchar)

    # Render Mỏ Đen
    squash_x = 1.0 + 0.04 * math.cos(2.0 * omega * t)
    squash_y = 1.0 - 0.04 * math.cos(2.0 * omega * t)
    hop_y = -8.0 * (1.0 - math.cos(2.0 * omega * t)) / 2.0

    cat_sprite = cat.render_cat_sprite(t)
    painter.save()
    painter.translate(cx, cy + hop_y)
    painter.scale(scale * squash_x, scale * squash_y)
    painter.translate(-512, -512)
    painter.drawImage(0, 0, cat_sprite)
    painter.restore()

    # Header / Title Tag
    painter.setFont(QFont("Segoe UI Semibold", 22))
    painter.setPen(QColor(100, 80, 60, 200))
    painter.drawText(QRectF(0, 40, canvas_w, 40), Qt.AlignmentFlag.AlignCenter,
                     "MỎ ĐEN · ĐIỆU LẮC MÔNG VUI NHỘN (SEAMLESS LOOP)")

    painter.end()
    return frame


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--previews-only", action="store_true")
    args = parser.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

    app = QGuiApplication.instance() or QGuiApplication([])

    # Load source Mỏ Đen
    manifest = json.loads((LIBRARY / "manifest.json").read_text(encoding="utf-8"))
    entry = next(a for a in manifest["assets"] if a["id"] == "mo_den_01")
    source = LIBRARY / entry["file"]

    original = QImage(str(source))
    cleaned = QImage(str(WORK_BASE / "face_clean_derivative.png")).scaled(
        1024, 1024, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)

    cat = WiggleCat(original, cleaned)

    # 1. Generate Contact Sheet of 12 key phases across 1 cycle (1.2s)
    sheet_w, sheet_h = 1920, 810
    sheet = Image.new("RGB", (sheet_w, sheet_h), "#fffdf7")
    preview_indices = [int(round(i * (CYCLE_FRAMES / 12.0))) for i in range(12)]

    for idx, f in enumerate(preview_indices):
        t = f / FPS
        frame = render_preview_frame(cat, t, 1920, 1080, scale=0.72)
        frame.save(str(OUT / f"frame_{f:03d}.png"))
        pil_frame = to_pil(frame).resize((480, 270), Image.Resampling.LANCZOS)
        col = idx % 4
        row = idx // 4
        sheet.paste(pil_frame, (col * 480, row * 270))

    sheet.save(OUT / "contact_sheet.jpg", quality=94)
    print("Contact sheet created: outputs/mo_den_wiggle_loop/contact_sheet.jpg", flush=True)

    if args.previews_only:
        print("Previews generated successfully.", flush=True)
        return

    # 2. Render Single Cycle 1.2s Transparent WebM (1024x1024 crop)
    single_webm = OUT / "Mo_Den_wiggle_single_cycle_1.2s.webm"
    cmd_single = [
        "C:\\Users\\ADMIN\\ffmpeg\\bin\\ffmpeg.exe",
        "-v", "error", "-y",
        "-f", "rawvideo",
        "-pixel_format", "bgra",
        "-video_size", "1024x1024",
        "-framerate", "30",
        "-i", "pipe:0",
        "-c:v", "libvpx-vp9",
        "-pix_fmt", "yuva420p",
        "-b:v", "2M",
        "-auto-alt-ref", "0",
        str(single_webm)
    ]
    p_single = subprocess.Popen(cmd_single, stdin=subprocess.PIPE)
    for f in range(CYCLE_FRAMES):
        t = f / FPS
        # Render centered 1024x1024
        sprite = cat.render_cat_sprite(t)
        p_single.stdin.write(bytes(sprite.constBits()))
    p_single.stdin.close()
    p_single.wait()
    print(f"Single cycle transparent WebM encoded -> {single_webm}", flush=True)

    # 3. Render 1080p Transparent Apple ProRes 4444 MOV (Universal Industry Standard for Video Editors)
    prores_mov = OUT / "Mo_Den_wiggle_1080p_transparent_ProRes4444.mov"
    cmd_prores = [
        "C:\\Users\\ADMIN\\ffmpeg\\bin\\ffmpeg.exe",
        "-v", "error", "-y",
        "-f", "rawvideo",
        "-pixel_format", "bgra",
        "-video_size", "1920x1080",
        "-framerate", "30",
        "-i", "pipe:0",
        "-c:v", "prores_ks",
        "-profile:v", "4",
        "-pix_fmt", "yuva444p12le",
        str(prores_mov)
    ]
    p_prores = subprocess.Popen(cmd_prores, stdin=subprocess.PIPE)

    # 4. Render 1080p Transparent WebM (VP9 with alpha)
    multi_webm = OUT / "Mo_Den_wiggle_1080p_transparent.webm"
    cmd_multi = [
        "C:\\Users\\ADMIN\\ffmpeg\\bin\\ffmpeg.exe",
        "-v", "error", "-y",
        "-f", "rawvideo",
        "-pixel_format", "bgra",
        "-video_size", "1920x1080",
        "-framerate", "30",
        "-i", "pipe:0",
        "-c:v", "libvpx-vp9",
        "-pix_fmt", "yuva420p",
        "-b:v", "3M",
        "-auto-alt-ref", "0",
        str(multi_webm)
    ]
    p_multi = subprocess.Popen(cmd_multi, stdin=subprocess.PIPE)

    # 5. Render 1080p Preview MP4 with background
    preview_mp4 = OUT / "Mo_Den_wiggle_preview_fun.mp4"
    cmd_preview = [
        "C:\\Users\\ADMIN\\ffmpeg\\bin\\ffmpeg.exe",
        "-v", "error", "-y",
        "-f", "rawvideo",
        "-pixel_format", "rgb32",
        "-video_size", "1920x1080",
        "-framerate", "30",
        "-i", "pipe:0",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        str(preview_mp4)
    ]
    p_preview = subprocess.Popen(cmd_preview, stdin=subprocess.PIPE)

    started = time.monotonic()
    for f in range(TOTAL_FRAMES):
        t = f / FPS
        # Write transparent frame to ProRes & WebM
        trans_frame = render_transparent_frame(cat, t, 1920, 1080, scale=0.75)
        raw_bytes = bytes(trans_frame.constBits())
        p_prores.stdin.write(raw_bytes)
        p_multi.stdin.write(raw_bytes)

        # Write preview frame to MP4
        prev_frame = render_preview_frame(cat, t, 1920, 1080, scale=0.75)
        p_preview.stdin.write(bytes(prev_frame.constBits()))

        if f % 72 == 0:
            print(f"Wiggle frame {f}/{TOTAL_FRAMES}: {time.monotonic() - started:.1f}s", flush=True)

    p_prores.stdin.close()
    p_prores.wait()
    p_multi.stdin.close()
    p_multi.wait()
    p_preview.stdin.close()
    p_preview.wait()

    total_time = round(time.monotonic() - started, 2)
    print(f"All wiggle assets rendered in {total_time}s!", flush=True)

    # Metadata manifest
    manifest_data = {
        "character": "mo_den",
        "action": "butt_and_hip_wiggle_dance",
        "action_vi": "Lắc mông & đánh hông vui nhộn (vòng lặp hoàn hảo)",
        "loop_cycle_seconds": LOOP_SECONDS,
        "loop_cycle_frames": CYCLE_FRAMES,
        "fps": FPS,
        "total_loops_in_clip": TOTAL_LOOPS,
        "total_duration_seconds": TOTAL_FRAMES / FPS,
        "files": {
            "prores_transparent_mov": str(prores_mov.relative_to(ROOT)),
            "full_hd_transparent_webm": str(multi_webm.relative_to(ROOT)),
            "single_cycle_transparent_webm": str(single_webm.relative_to(ROOT)),
            "full_hd_preview_mp4": str(preview_mp4.relative_to(ROOT)),
            "contact_sheet": str((OUT / "contact_sheet.jpg").relative_to(ROOT))
        },
        "seamless_loop_guarantee": "All motion equations use pure integer harmonic sine/cosine functions with zero boundary delta.",
        "usage_guide_vi": "File ProRes4444 (.mov) và WebM (.webm) có sẵn kênh Alpha trong suốt. Chỉ cần kéo thả thẳng vào track trên timeline của bất kỳ phần mềm dựng phim nào (Premiere, CapCut, DaVinci, Studio) là nhân vật sẽ nổi trên nền video. Nhân bản (Ctrl+D / Alt+Drag) bao nhiêu lần tùy thích mà không lo bị khựng."
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
