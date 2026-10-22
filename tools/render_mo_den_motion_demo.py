"""Render a 15s *draft* Mỏ Đen mesh/face animation from preserved supplied art.

No generated artwork or replacement speaker. Separate from production exporter:
this is a prototype/QC preview, not a bypass or implementation of production rig QC.
Requires the existing Qt/Pillow/numpy/scipy environment, FFmpeg and Rhubarb cues.
"""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import time
import wave

import numpy as np
from PIL import Image, ImageFilter
from scipy.ndimage import gaussian_filter1d
from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import (QColor, QFont, QFontDatabase, QGuiApplication, QImage, QPainter,
                           QPainterPath, QPen, QRadialGradient)

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "projects/mo_den_motion_demo"
OUT = ROOT / "outputs/mo_den_motion_demo_15s"
LIBRARY = ROOT / "assets/characters/mo_den"
FPS, SECONDS, SIZE = 30, 15, (1920, 1080)
INK = QColor("#080807")
HEAD_KEYS = [(0, -.8), (.6, 0), (1.8, .6), (3.0, -.4), (4.8, 1.1),
             (6.5, .2), (8.5, -.4), (9.3, -1.8), (11.5, -2.0),
             (12.4, -1.8), (13.5, -.6), (15, -.4)]
SHAPES = {"X": (108, 0, 0), "A": (102, 2, 0), "B": (123, 20, .8),
          "C": (119, 47, .25), "D": (130, 87, .1), "E": (75, 65, .05),
          "F": (53, 47, .05), "G": (110, 15, .9), "H": (110, 37, .12)}


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def save_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def smooth(a, b, value):
    value = np.clip((value - a) / (b - a), 0, 1)
    return value * value * (3 - 2 * value)


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


def eye_path(side, opened=1.):
    # Traced *supplied cat* outline coordinates; no new character design.
    if side == "left":
        points = [(754, 802), (809, 780), (889, 754), (936, 784),
                  (953, 832), (946, 882), (900, 904),
                  (852, 925), (804, 911), (779, 886),
                  (762, 861), (756, 832), (754, 802)]
        center = lambda x: 847 - .10 * (x - 846)
    else:
        points = [(1098, 761), (1145, 735), (1227, 707), (1278, 734),
                  (1299, 780), (1283, 837), (1235, 860),
                  (1189, 882), (1143, 875), (1115, 844),
                  (1101, 820), (1098, 791), (1098, 761)]
        center = lambda x: 803 - .14 * (x - 1192)
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


def feature_mask(path, stroke):
    image = QImage(2048, 2048, QImage.Format.Format_RGBA8888)
    image.fill(Qt.GlobalColor.transparent)
    painter = QPainter(image)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setBrush(Qt.GlobalColor.white)
    painter.setPen(QPen(Qt.GlobalColor.white, stroke, Qt.PenStyle.SolidLine,
                        Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
    painter.drawPath(path)
    painter.end()
    return np.asarray(to_pil(image))[:, :, 3] > 0


def clean_feature(original, mask):
    """Deterministic local colour-surface repair; never touches the original PNG.

    A quadratic fit to adjacent brown fur removes baked-in eye/mouth ink. This
    prototype repair is kept separately and must be visually checked in close-up.
    """
    yy, xx = np.nonzero(mask)
    x0, x1 = max(0, xx.min() - 25), min(2048, xx.max() + 26)
    y0, y1 = max(0, yy.min() - 25), min(2048, yy.max() + 26)
    roi = original[y0:y1, x0:x1].copy()
    local = mask[y0:y1, x0:x1]
    y, x = np.mgrid[y0:y1, x0:x1].astype(float)
    x = (x - (x0 + x1) / 2) / max(1, x1 - x0)
    y = (y - (y0 + y1) / 2) / max(1, y1 - y0)
    design = np.stack([np.ones_like(x), x, y, x*x, x*y, y*y], axis=-1)
    # Exclude white eye pixels, outline and cream fur from background samples.
    skin = (~local) & (roi[:, :, 0] > 60) & (roi[:, :, 0] < 177) & (roi[:, :, 2] < 125)
    coefficients = np.linalg.lstsq(design[skin], roi[:, :, :3][skin], rcond=None)[0]
    repaired = np.clip(design @ coefficients, 0, 255)
    soft = np.asarray(Image.fromarray((local * 255).astype(np.uint8)).filter(
        ImageFilter.GaussianBlur(2)), dtype=float)[:, :, None] / 255
    roi[:, :, :3] = np.clip(roi[:, :, :3] * (1-soft) + repaired * soft, 0, 255).astype(np.uint8)
    original[y0:y1, x0:x1] = roi
    return original


def prepare_texture(source):
    original = np.array(Image.open(source).convert("RGBA"))
    for side in ("left", "right"):
        original = clean_feature(original, feature_mask(eye_path(side), 27))
    original = clean_feature(original, feature_mask(original_mouth(), 27))
    cleaned = Image.fromarray(original)
    cleaned.save(WORK / "face_clean_derivative.png")
    cleaned = cleaned.resize((1024, 1024), Image.Resampling.LANCZOS)
    return to_qimage(cleaned)


def blink(t):
    closed = 0.
    for center in (1.72, 5.94, 9.02, 13.45):
        if center-.09 <= t <= center:
            amount = float(smooth(center-.09, center, t))
        elif center < t <= center+.025:
            amount = 1.
        elif center+.025 < t <= center+.17:
            amount = 1-float(smooth(center+.025, center+.17, t))
        else:
            amount = 0.
        closed = max(closed, amount)
    return 1-closed


class MouthTrack:
    def __init__(self):
        document = json.loads((WORK / "mouth_cues_raw.json").read_text(encoding="utf-8"))
        self.cues = document["mouthCues"]
        self.times = np.arange(SECONDS * 1000 + 1) / 1000
        values = np.tile(np.array(SHAPES["X"], float), (len(self.times), 1))
        for cue in self.cues:
            selected = (self.times >= cue["start"]) & (self.times < cue["end"])
            values[selected] = SHAPES[cue["value"]]
        # Geometric interpolation of one mouth, not a dissolve between two mouths.
        self.values = gaussian_filter1d(values, sigma=22, axis=0, mode="nearest")
        with wave.open(str(WORK / "audio_H_excerpt_15s.wav")) as stream:
            rate = stream.getframerate()
            samples = np.frombuffer(stream.readframes(stream.getnframes()), dtype="<i2").astype(float)/32768
        win = round(rate*.01)
        envelope = np.sqrt(np.mean(samples[:len(samples)//win*win].reshape(-1, win)**2, axis=1))
        self.envelope = gaussian_filter1d(envelope, sigma=2)
        self.envelope_time = np.arange(len(envelope))*.01 + .005

    def at(self, t):
        v = np.array([np.interp(t, self.times, self.values[:, i]) for i in range(3)])
        rms = float(np.interp(t, self.envelope_time, self.envelope))
        gate = float(smooth(.002, .018, rms))
        v[1] *= gate * (.65 + .35 * float(smooth(.015, .09, rms)))
        v[2] *= gate
        return v


def draw_mouth(painter, width, height, teeth):
    painter.setPen(QPen(INK, 10, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap,
                        Qt.PenJoinStyle.RoundJoin))
    if height < 3.5:
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(original_mouth())
        return
    cx, cy = 1038, 958
    path = QPainterPath(QPointF(cx-width/2, cy))
    path.cubicTo(cx-width*.22, cy+7, cx+width*.21, cy+5, cx+width/2, cy-5)
    path.cubicTo(cx+width*.50, cy+height*.57, cx+width*.31, cy+height, cx, cy+height)
    path.cubicTo(cx-width*.32, cy+height, cx-width*.50, cy+height*.5, cx-width/2, cy)
    path.closeSubpath()
    painter.setBrush(QColor("#522522"))
    painter.drawPath(path)
    painter.save()
    painter.setClipPath(path)
    painter.setPen(Qt.PenStyle.NoPen)
    if height > 24:
        painter.setBrush(QColor("#e98e96"))
        painter.drawEllipse(QRectF(cx-width*.32, cy+height*.63, width*.64, height*.49))
    if teeth > .22:
        painter.setBrush(QColor("#fbefe0"))
        painter.drawRoundedRect(QRectF(cx-width*.47, cy-11, width*.94, 12+teeth*10), 5, 5)
    painter.restore()
    painter.setBrush(Qt.BrushStyle.NoBrush)
    painter.setPen(QPen(INK, 10, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap,
                        Qt.PenJoinStyle.RoundJoin))
    painter.drawPath(path)


def texture_at(cleaned, original, mouth, t):
    image = cleaned.copy()
    painter = QPainter(image)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
    painter.scale(.5, .5)
    opened = blink(t)
    for side in ("left", "right"):
        path = eye_path(side, max(.015, opened))
        painter.save()
        painter.setClipPath(path)
        painter.drawImage(0, 0, original)
        painter.restore()
        if opened < .99:
            painter.setPen(QPen(INK, 9, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap,
                                Qt.PenJoinStyle.RoundJoin))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawPath(path)
    draw_mouth(painter, *mouth.at(t))
    painter.end()
    return to_pil(image)


GRID = np.arange(0, 1025, 32)
GX, GY = np.meshgrid(GRID, GRID)


def mesh_at(t):
    x, y = GX.astype(float).copy(), GY.astype(float).copy()
    # Inverse continuous deformation; neck, paws and tail stay connected.
    head = (1-smooth(565, 642, y)) * (1-smooth(665, 738, x)*smooth(535, 580, y))
    angle = math.radians(key_value(HEAD_KEYS, t))*head
    nod = 1.4*math.sin(t*2.2) + 1.2*math.sin(t*3.7)*float(smooth(.5, 1.3, t))
    px, py = x-520, y-601-nod*head
    x, y = 520+np.cos(angle)*px+np.sin(angle)*py, 601-np.sin(angle)*px+np.cos(angle)*py
    tail = smooth(683, 732, x) * (1-smooth(839, 878, y))
    angle = math.radians(2.4*math.sin(t*1.1+.3)+.55*math.sin(t*2.2))*tail
    px, py = x-704, y-847
    x, y = 704+np.cos(angle)*px+np.sin(angle)*py, 847-np.sin(angle)*px+np.cos(angle)*py
    for cx, phase in ((432, .2), (576, 1.6)):
        weight = np.exp(-((x-cx)/68)**4-((y-733)/81)**4)
        gesture = .8*math.sin(t*1.2+phase) + 1.3*math.exp(-((t-9.9)/1.1)**2)
        x -= gesture*weight
        y -= 1.8*math.sin(t*1.25+phase)*weight
    breath = .0038*math.sin(t*1.55)
    torso = np.exp(-((y-745)/139)**4)*(1-head)
    x = 528+(x-528)/(1+breath*torso)
    y = 890+(y-890)/(1+breath*torso)
    mesh = []
    for row in range(len(GRID)-1):
        for col in range(len(GRID)-1):
            quad = (x[row,col], y[row,col], x[row+1,col], y[row+1,col],
                    x[row+1,col+1], y[row+1,col+1], x[row,col+1], y[row,col+1])
            mesh.append(((int(GRID[col]), int(GRID[row]), int(GRID[col+1]), int(GRID[row+1])), quad))
    return mesh


def stage():
    image = QImage(*SIZE, QImage.Format.Format_RGB888)
    image.fill(QColor("#faf7ef"))
    painter = QPainter(image)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QColor("#f0eee3"))
    painter.drawEllipse(QRectF(556, 190, 810, 745))
    font = QFont("Segoe UI", 17)
    font.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 5)
    painter.setFont(font)
    painter.setPen(QColor("#727a72"))
    painter.drawText(QRectF(0, 49, 1920, 38), Qt.AlignmentFlag.AlignCenter, "MỎ ĐEN KỂ CHUYỆN")
    painter.setFont(QFont("Segoe UI Semibold", 26))
    painter.setPen(QColor("#343d37"))
    painter.drawText(QRectF(0, 957, 1920, 55), Qt.AlignmentFlag.AlignCenter,
                     "Vì sao người Maya rời thành phố?")
    painter.end()
    return image


def render_frame(cleaned, original, track, background, t):
    texture = texture_at(cleaned, original, track, t)
    # Premultiplied interpolation avoids dark/cream fringes on transparent edges.
    warped = texture.convert("RGBa").transform((1024,1024), Image.Transform.MESH,
                     mesh_at(t), Image.Resampling.BICUBIC).convert("RGBA")
    image = background.copy()
    painter = QPainter(image)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
    painter.save()
    painter.translate(965, 925)
    painter.scale(1, .08)
    gradient = QRadialGradient(QPointF(0,0), 230)
    gradient.setColorAt(0, QColor(77,61,37,65))
    gradient.setColorAt(1, QColor(77,61,37,0))
    painter.setBrush(gradient)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawEllipse(QRectF(-230,-230,460,460))
    painter.restore()
    painter.drawImage(410, 28, to_qimage(warped))
    painter.end()
    return image, warped.getbbox()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--previews-only", action="store_true")
    args = parser.parse_args()
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    app = QGuiApplication.instance() or QGuiApplication([])
    # Offscreen Qt does not reliably discover Windows fonts in this environment.
    for filename in ("segoeui.ttf", "seguisb.ttf"):
        font_path = Path(os.environ.get("WINDIR", "C:/Windows"))/"Fonts"/filename
        if QFontDatabase.addApplicationFont(str(font_path)) < 0:
            raise RuntimeError(f"Cannot load required Vietnamese font: {font_path}")
    manifest = json.loads((LIBRARY/"manifest.json").read_text(encoding="utf-8"))
    entry = next(a for a in manifest["assets"] if a["id"]=="mo_den_01")
    source = LIBRARY/entry["file"]
    if sha(source) != entry["sha256"]:
        raise RuntimeError("Supplied original changed; refusing to use mismatched identity.")
    original = QImage(str(source))
    cleaned = prepare_texture(source)
    track = MouthTrack()
    background = stage()
    preview_times = [0, 1.72, 3.0, 5.94, 7.0, 9.02, 10.8, 13.45, 14.7]
    for t in preview_times:
        frame, _ = render_frame(cleaned, original, track, background, t)
        frame.save(str(OUT/f"preview_{t:05.2f}.png"))
    clean_preview, _ = render_frame(cleaned, original, track, background, 0)
    clean_preview.save(str(OUT/"poster.png"))
    sheet = Image.new("RGB", (1440,810), "white")
    for i, t in enumerate(preview_times):
        with Image.open(OUT/f"preview_{t:05.2f}.png") as frame:
            sheet.paste(frame.resize((480,270), Image.Resampling.LANCZOS), ((i%3)*480,(i//3)*270))
    sheet.save(OUT/"contact_sheet.jpg", quality=94)
    details = {
        "kind": "character_animation_draft_preview", "role": "character",
        "asset_id": "mo_den_01_mesh_demo_v1", "production_approved": False,
        "source": str(source.relative_to(ROOT)), "source_sha256": sha(source),
        "audio": "projects/mo_den_motion_demo/audio_H_excerpt_15s.wav",
        "audio_sha256": sha(WORK/"audio_H_excerpt_15s.wav"),
        "audio_source": "projects/mo_den_maya/assets/audio/narration.wav",
        "audio_source_range_seconds": [0, 11.82], "intro_silence_seconds": .55,
        "speed_reapplied": False, "speaker": "custom H, Northern Vietnamese, already 1.25x",
        "cues_sha256": sha(WORK/"mouth_cues_raw.json"),
        "code_sha256": sha(Path(__file__)), "fps": FPS, "duration_seconds": SECONDS,
        "method": "supplied-texture continuous quad mesh, separately painted vector mouth and clipped original eye textures",
        "image_generation_model": None, "lip_sync": "Rhubarb 1.14.0 phonetic; unverified Vietnamese phonetic accuracy",
        "not_implemented": ["production Studio rig importer/export-QC integration", "large body pose changes", "automatic Vietnamese listening QC"],
        "original_preserved": sha(source)==entry["sha256"],
    }
    save_json(WORK/"demo_manifest.json", details)
    if args.previews_only:
        print("Previews ready", flush=True)
        return
    video = OUT/"Mo_Den_demo_15s.mp4"
    command = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pixel_format", "rgb24",
               "-video_size", "1920x1080", "-framerate", str(FPS), "-i", "pipe:0",
               "-i", str(WORK/"audio_H_excerpt_15s.wav"), "-map", "0:v:0", "-map", "1:a:0",
               "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
               "-c:a", "aac", "-b:a", "192k", "-t", str(SECONDS), "-movflags", "+faststart", str(video)]
    started = time.monotonic()
    boxes = []
    with (OUT/"encode.log").open("w") as log:
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=log)
        try:
            for frame_number in range(FPS*SECONDS):
                frame, bounds = render_frame(cleaned, original, track, background, frame_number/FPS)
                boxes.append(bounds)
                process.stdin.write(bytes(frame.constBits()))
                if frame_number % 60 == 0:
                    print(f"Frame {frame_number}/{FPS*SECONDS}: {time.monotonic()-started:.1f}s", flush=True)
            process.stdin.close()
            if process.wait():
                raise RuntimeError("FFmpeg encode failed; see encode.log")
        except BaseException:
            process.kill()
            process.wait()
            raise
    if any(b is None or b[0]<5 or b[1]<5 or b[2]>1019 or b[3]>1019 for b in boxes):
        raise RuntimeError("Unexpected empty or cropped character; review preview before delivery.")
    details.update(video=str(video.relative_to(ROOT)), video_sha256=sha(video),
                   rendered_frames=FPS*SECONDS, render_seconds=round(time.monotonic()-started,2),
                   source_unchanged_after_render=sha(source)==entry["sha256"],
                   visual_qc="Pending inspection of rendered previews", listening_qc="Not independently certified")
    save_json(WORK/"demo_manifest.json", details)
    print(f"Rendered {video}", flush=True)


if __name__ == "__main__":
    main()
