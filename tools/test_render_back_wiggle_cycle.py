"""Test rendering a 36-frame (1.2s) cycle of Mỏ Đen back wiggle dance."""
import math
import os
from pathlib import Path
from PIL import Image
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter, QImage, QColor

WORKDIR = Path("projects/mo_den_motion_demo/back_wiggle")
FRAMES_DIR = WORKDIR / "test_frames"
FRAMES_DIR.mkdir(exist_ok=True)

FPS = 30
CYCLE_FRAMES = 36
CYCLE_SECONDS = 1.2

def main():
    body_img = QImage(str(WORKDIR / "test_symmetric_body.png"))
    tail_img = QImage(str(WORKDIR / "layer_tail_vector.png"))
    upper_img = QImage(str(WORKDIR / "layer_upper_head.png"))
    rump_img = QImage(str(WORKDIR / "layer_rump.png"))
    paws_img = QImage(str(WORKDIR / "layer_paws.png"))

    W, H = 1024, 1024

    for frame in range(CYCLE_FRAMES):
        t = frame / FPS
        phase = 2.0 * math.pi * (frame / CYCLE_FRAMES)

        # 1. Hip motion (Butt Wiggle)
        # Lateral sway: 38px amplitude
        hip_x = 38.0 * math.sin(phase)
        # Hip tilt: 10 degrees amplitude
        hip_rot = 10.0 * math.sin(phase)
        # Bouncy vertical drop: double frequency (two wiggles per cycle)
        # Drops at the extreme swings, rises at center
        bounce_y = -14.0 * (1.0 - math.cos(2.0 * phase)) / 2.0
        # Squash & Stretch of the buttocks
        # When hip swings wide, it squashes vertically and bulges horizontally
        stretch_x = 1.0 + 0.06 * math.cos(2.0 * phase)
        stretch_y = 1.0 - 0.05 * math.cos(2.0 * phase)

        # 2. Tail motion
        # Whips in counter-phase with delay (0.45 rad lag) + harmonic secondary flick
        tail_angle = -38.0 * math.sin(phase - 0.45) + 12.0 * math.sin(2.0 * phase)

        # 3. Head & upper body motion
        # Counter-balances hips: subtle opposite tilt and micro-shift
        head_rot = -4.5 * math.sin(phase)
        head_x = -10.0 * math.sin(phase)
        head_y = bounce_y * 0.4

        # Canvas
        out = QImage(W, H, QImage.Format.Format_ARGB32_Premultiplied)
        out.fill(Qt.GlobalColor.transparent)

        p = QPainter(out)
        p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        p.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)

        # --- A. Draw Hind Paws on floor ---
        # Subtle tap / foot squash
        paw_lift_l = max(0.0, -math.sin(phase)) * 6.0
        paw_lift_r = max(0.0, math.sin(phase)) * 6.0
        p.drawImage(0, 0, paws_img)

        # --- B. Draw Rump / Buttocks ---
        p.save()
        # Pivot at waist center (512, 590)
        p.translate(512 + hip_x, 590 + bounce_y)
        p.rotate(hip_rot)
        p.scale(stretch_x, stretch_y)
        p.translate(-512, -590)
        p.drawImage(0, 0, rump_img)
        p.restore()

        # --- C. Draw Tail ---
        # Tail attaches to the cleft of the buttocks
        # Since rump has (hip_x, bounce_y, hip_rot), calculate tail root in canvas
        # Root is at (512, 730) on the rump
        p.save()
        p.translate(512 + hip_x, 590 + bounce_y)
        p.rotate(hip_rot)
        p.translate(-512, -590)
        # Now at rump local coordinates:
        p.translate(512, 730)
        p.rotate(tail_angle)
        # Tail sprite root is (45, 425)
        p.translate(-45, -425)
        p.drawImage(0, 0, tail_img)
        p.restore()

        # --- D. Draw Upper Body & Head ---
        p.save()
        # Pivot at neck/chest (512, 560)
        p.translate(512 + head_x, 560 + head_y)
        p.rotate(head_rot)
        p.translate(-512, -560)
        p.drawImage(0, 0, upper_img)
        p.restore()

        p.end()

        # Save frame
        rgba = out.convertToFormat(QImage.Format.Format_RGBA8888)
        pil_img = Image.frombytes("RGBA", (W, H), bytes(rgba.constBits()))
        pil_img.save(FRAMES_DIR / f"frame_{frame:03d}.png")

    print(f"Rendered {CYCLE_FRAMES} frames successfully to {FRAMES_DIR}")

if __name__ == "__main__":
    main()
