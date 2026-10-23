"""Render the complete, user-approved authentic Back-View Butt & Tail Wiggle Dance for Mỏ Đen.

Uses the genuine 2D cartoon rear-view illustration created for Mỏ Đen.
Produces:
1. Mo_Den_back_wiggle_1080p_transparent_ProRes4444.mov (1920x1080 ProRes 4444, yuva444p12le alpha, 9.6s seamless loop)
2. Mo_Den_back_wiggle_1080p_transparent.webm (1920x1080 WebM VP9, yuva420p alpha, 9.6s seamless loop)
3. Mo_Den_back_wiggle_single_cycle_1.2s.webm (1024x1024 WebM VP9, 1.2s single cycle)
4. Mo_Den_back_wiggle_preview_fun.mp4 (1920x1080 H.264 preview with soft studio floor shadow)
5. contact_sheet.jpg (12-frame contact sheet)
"""
import math
import os
from pathlib import Path
import subprocess
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from PySide6.QtCore import Qt, QPointF, QRectF
from PySide6.QtGui import (QPainter, QImage, QColor, QPen, QRadialGradient,
                           QLinearGradient, QBrush)

ROOT = Path(__file__).resolve().parents[1]
WORKDIR = ROOT / "projects/mo_den_motion_demo/back_wiggle"
OUTDIR = ROOT / "outputs/mo_den_back_wiggle_loop"
OUTDIR.mkdir(parents=True, exist_ok=True)

TEMP_FRAMES_ALPHA = WORKDIR / "render_alpha_frames"
TEMP_FRAMES_PREVIEW = WORKDIR / "render_preview_frames"
TEMP_FRAMES_SQUARE = WORKDIR / "render_square_frames"

TEMP_FRAMES_ALPHA.mkdir(exist_ok=True)
TEMP_FRAMES_PREVIEW.mkdir(exist_ok=True)
TEMP_FRAMES_SQUARE.mkdir(exist_ok=True)

FFMPEG = r"C:\Users\ADMIN\ffmpeg\bin\ffmpeg.exe"

FPS = 30
CYCLE_FRAMES = 36  # 1.2s @ 30fps
TOTAL_LOOPS = 8
TOTAL_FRAMES = CYCLE_FRAMES * TOTAL_LOOPS  # 288 frames = 9.6s

def render_character_frame(phase, scale=0.62, canvas_w=1920, canvas_h=1080, center_x=960, floor_y=920, bg_mode="transparent"):
    """Render a single frame of Mỏ Đen back wiggle dance."""
    body_img = QImage(str(WORKDIR / "test_symmetric_body.png"))
    tail_img = QImage(str(WORKDIR / "layer_tail_vector.png"))

    out = QImage(canvas_w, canvas_h, QImage.Format.Format_ARGB32_Premultiplied)
    
    if bg_mode == "preview":
        # Cheerful clean studio background
        p = QPainter(out)
        p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        bg_grad = QLinearGradient(0, 0, 0, canvas_h)
        bg_grad.setColorAt(0.0, QColor("#fcfaf6"))
        bg_grad.setColorAt(0.7, QColor("#f5efe5"))
        bg_grad.setColorAt(1.0, QColor("#e8ded0"))
        p.fillRect(0, 0, canvas_w, canvas_h, bg_grad)

        # Ambient floor glow
        floor_grad = QRadialGradient(center_x, floor_y - 20, 600)
        floor_grad.setColorAt(0.0, QColor(255, 255, 255, 120))
        floor_grad.setColorAt(1.0, QColor(255, 255, 255, 0))
        p.fillRect(0, 0, canvas_w, canvas_h, floor_grad)
        p.end()
    else:
        out.fill(Qt.GlobalColor.transparent)

    p = QPainter(out)
    p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    p.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)

    # Motion Harmonics (Seamless 1.2s Loop)
    # 1. Hip / Body lateral sway & tilt
    body_tilt = 6.2 * math.sin(phase)
    hip_drift_x = 24.0 * math.sin(phase)
    
    # 2. Vertical bounce (double frequency: bobs twice per loop)
    bounce_y = -12.0 * (1.0 - math.cos(2.0 * phase)) / 2.0
    
    # 3. Squash & Stretch
    squash_x = 1.0 + 0.045 * math.cos(2.0 * phase)
    squash_y = 1.0 - 0.040 * math.cos(2.0 * phase)

    # 4. Furious Tail Whip (lagged phase + 2nd harmonic)
    tail_whip = -36.0 * math.sin(phase - 0.42) + 11.0 * math.sin(2.0 * phase)

    # --- Draw Soft Contact Floor Shadow (for preview or subtle grounding) ---
    if bg_mode == "preview":
        shadow_w = 400.0 * squash_x * scale
        shadow_h = 46.0 * squash_y * scale
        shadow_x = center_x + hip_drift_x * 0.4 * scale
        shadow_y = floor_y - 8.0

        shadow_grad = QRadialGradient(shadow_x, shadow_y, shadow_w / 2.0)
        shadow_grad.setColorAt(0.0, QColor(40, 25, 20, 75))
        shadow_grad.setColorAt(0.5, QColor(40, 25, 20, 35))
        shadow_grad.setColorAt(1.0, QColor(40, 25, 20, 0))
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(shadow_grad)
        p.drawEllipse(QPointF(shadow_x, shadow_y), shadow_w / 2.0, shadow_h / 2.0)

    # --- Draw Character ---
    p.save()
    # Position overall character on floor:
    # Character base in 1024x1024 sprite is at y ≈ 910
    p.translate(center_x, floor_y)
    p.scale(scale, scale)
    # Origin now at floor contact point (512, 910)
    p.translate(-512, -910)

    # Character body sway pivoted at neck (512, 380)
    p.save()
    p.translate(512 + hip_drift_x, 380 + bounce_y)
    p.rotate(body_tilt)
    p.scale(squash_x, squash_y)
    p.translate(-512, -380)

    # 1. Body
    p.drawImage(0, 0, body_img)

    # 2. Tail attached at rump cleft (512, 750)
    p.translate(512, 750)
    p.rotate(tail_whip)
    # Tail vector sprite root is at (45, 425)
    p.translate(-45, -425)
    p.drawImage(0, 0, tail_img)
    p.restore()

    p.restore()
    p.end()

    # Convert to PIL Image
    rgba = out.convertToFormat(QImage.Format.Format_RGBA8888)
    return Image.frombytes("RGBA", (canvas_w, canvas_h), bytes(rgba.constBits()))

def main():
    print(f"Rendering {CYCLE_FRAMES} unique master cycle frames...")
    cycle_alpha = []
    cycle_preview = []
    cycle_square = []

    for f in range(CYCLE_FRAMES):
        phase = 2.0 * math.pi * (f / CYCLE_FRAMES)
        
        # 1. Full HD Alpha Frame (1920x1080)
        im_alpha = render_character_frame(phase, scale=0.62, canvas_w=1920, canvas_h=1080, center_x=960, floor_y=930, bg_mode="transparent")
        cycle_alpha.append(im_alpha)

        # 2. Full HD Preview Frame (1920x1080)
        im_prev = render_character_frame(phase, scale=0.62, canvas_w=1920, canvas_h=1080, center_x=960, floor_y=930, bg_mode="preview")
        cycle_preview.append(im_prev)

        # 3. Square Single Cycle Frame (1024x1024)
        im_sq = render_character_frame(phase, scale=0.92, canvas_w=1024, canvas_h=1024, center_x=512, floor_y=970, bg_mode="transparent")
        cycle_square.append(im_sq)

    # Save Square Single Cycle Frames
    print("Saving square 1.2s single cycle frames...")
    for f in range(CYCLE_FRAMES):
        cycle_square[f].save(TEMP_FRAMES_SQUARE / f"frame_{f:03d}.png")

    # Save Full 9.6s Loop Frames (TOTAL_FRAMES = 288)
    print(f"Writing {TOTAL_FRAMES} looped frames for video encoding...")
    for loop_idx in range(TOTAL_LOOPS):
        for f in range(CYCLE_FRAMES):
            frame_num = loop_idx * CYCLE_FRAMES + f
            cycle_alpha[f].save(TEMP_FRAMES_ALPHA / f"frame_{frame_num:04d}.png")
            cycle_preview[f].save(TEMP_FRAMES_PREVIEW / f"frame_{frame_num:04d}.png")

    # --- 1. Export ProRes 4444 with Alpha ---
    prores_out = OUTDIR / "Mo_Den_back_wiggle_1080p_transparent_ProRes4444.mov"
    print(f"Encoding ProRes 4444 -> {prores_out}...")
    cmd_prores = [
        FFMPEG, "-y",
        "-r", str(FPS),
        "-i", str(TEMP_FRAMES_ALPHA / "frame_%04d.png"),
        "-c:v", "prores_ks",
        "-profile:v", "4",
        "-pix_fmt", "yuva444p12le",
        "-r", str(FPS),
        str(prores_out)
    ]
    subprocess.run(cmd_prores, check=True)

    # --- 2. Export Full HD WebM with Alpha ---
    webm_out = OUTDIR / "Mo_Den_back_wiggle_1080p_transparent.webm"
    print(f"Encoding Full HD WebM -> {webm_out}...")
    cmd_webm = [
        FFMPEG, "-y",
        "-r", str(FPS),
        "-i", str(TEMP_FRAMES_ALPHA / "frame_%04d.png"),
        "-c:v", "libvpx-vp9",
        "-pix_fmt", "yuva420p",
        "-b:v", "2M",
        "-auto-alt-ref", "0",
        "-r", str(FPS),
        str(webm_out)
    ]
    subprocess.run(cmd_webm, check=True)

    # --- 3. Export Single Cycle Square WebM (1.2s) ---
    sq_webm_out = OUTDIR / "Mo_Den_back_wiggle_single_cycle_1.2s.webm"
    print(f"Encoding Single Cycle WebM -> {sq_webm_out}...")
    cmd_sq_webm = [
        FFMPEG, "-y",
        "-r", str(FPS),
        "-i", str(TEMP_FRAMES_SQUARE / "frame_%03d.png"),
        "-c:v", "libvpx-vp9",
        "-pix_fmt", "yuva420p",
        "-b:v", "2M",
        "-auto-alt-ref", "0",
        "-r", str(FPS),
        str(sq_webm_out)
    ]
    subprocess.run(cmd_sq_webm, check=True)

    # --- 4. Export Preview MP4 (H.264, yuv420p) ---
    mp4_out = OUTDIR / "Mo_Den_back_wiggle_preview_fun.mp4"
    print(f"Encoding Preview MP4 -> {mp4_out}...")
    cmd_mp4 = [
        FFMPEG, "-y",
        "-r", str(FPS),
        "-i", str(TEMP_FRAMES_PREVIEW / "frame_%04d.png"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "18",
        "-preset", "medium",
        "-r", str(FPS),
        str(mp4_out)
    ]
    subprocess.run(cmd_mp4, check=True)

    # --- 5. Generate 12-Frame Contact Sheet ---
    contact_path = OUTDIR / "contact_sheet.jpg"
    print(f"Generating Contact Sheet -> {contact_path}...")
    # 4 columns x 3 rows
    cols, rows = 4, 3
    sample_indices = [int(i * CYCLE_FRAMES / 12) for i in range(12)]
    cell_w, cell_h = 360, 360
    sheet = Image.new("RGB", (cols * cell_w, rows * cell_h + 60), color=(248, 246, 242))
    draw = ImageDraw.Draw(sheet)

    for idx, frame_idx in enumerate(sample_indices):
        c = idx % cols
        r = idx // cols
        x_pos = c * cell_w
        y_pos = r * cell_h + 60
        
        # Crop cat area from preview frame
        frame_img = cycle_preview[frame_idx]
        # Crop center (700..1220, 480..1000)
        cropped = frame_img.crop((700, 480, 1220, 1000)).resize((cell_w - 10, cell_h - 10), Image.Resampling.LANCZOS)
        sheet.paste(cropped, (x_pos + 5, y_pos + 5))
        
        # Label
        time_sec = frame_idx / FPS
        label = f"#{frame_idx:02d} ({time_sec:.2f}s)"
        draw.rectangle([x_pos + 10, y_pos + 10, x_pos + 110, y_pos + 32], fill=(20, 20, 20, 200))
        draw.text((x_pos + 15, y_pos + 12), label, fill=(255, 255, 255))

    # Header text
    header = "MO DEN - QUAY LUNG LAC MONG VUI NHON (SEAMLESS 1.2S LOOP CONTACT SHEET)"
    draw.text((30, 20), header, fill=(30, 30, 30))
    sheet.save(contact_path, quality=92)

    # Cleanup temp frame folders to save disk space
    shutil.rmtree(TEMP_FRAMES_ALPHA, ignore_errors=True)
    shutil.rmtree(TEMP_FRAMES_PREVIEW, ignore_errors=True)
    shutil.rmtree(TEMP_FRAMES_SQUARE, ignore_errors=True)

    print("All exports generated successfully!")

if __name__ == "__main__":
    main()
