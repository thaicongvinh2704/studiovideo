"""Test unified body pivot at neck/chest to verify seamless intact body."""
import math
from pathlib import Path
from PIL import Image
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QImage

WORKDIR = Path("projects/mo_den_motion_demo/back_wiggle")
TEST_DIR = WORKDIR / "test_frames_unified"
TEST_DIR.mkdir(exist_ok=True)

FPS = 30
CYCLE_FRAMES = 36

def main():
    body_img = QImage(str(WORKDIR / "test_symmetric_body.png"))
    tail_img = QImage(str(WORKDIR / "layer_tail_vector.png"))

    W, H = 1024, 1024

    for frame in range(CYCLE_FRAMES):
        phase = 2.0 * math.pi * (frame / CYCLE_FRAMES)

        # Body sway: pivoted at neck (512, 380)
        # Angle: +/- 5.5 degrees
        body_angle = 5.5 * math.sin(phase)
        
        # Bouncy vertical bounce: 10px drop on wide swings
        bounce_y = -10.0 * (1.0 - math.cos(2.0 * phase)) / 2.0
        
        # Hip horizontal sway offset
        hip_drift_x = 18.0 * math.sin(phase)

        # Tail angle: counter-phase whip + 2nd harmonic
        tail_angle = -35.0 * math.sin(phase - 0.4) + 10.0 * math.sin(2.0 * phase)

        out = QImage(W, H, QImage.Format.Format_ARGB32_Premultiplied)
        out.fill(Qt.GlobalColor.white)

        p = QPainter(out)
        p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        p.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)

        # Draw Body pivoted at (512, 380)
        p.save()
        p.translate(512 + hip_drift_x, 380 + bounce_y)
        p.rotate(body_angle)
        p.translate(-512, -380)
        p.drawImage(0, 0, body_img)

        # Draw Tail attached to rump cleft (512, 750)
        p.translate(512, 750)
        p.rotate(tail_angle)
        p.translate(-45, -425)
        p.drawImage(0, 0, tail_img)
        p.restore()

        p.end()

        rgba = out.convertToFormat(QImage.Format.Format_RGBA8888)
        pil_img = Image.frombytes("RGBA", (W, H), bytes(rgba.constBits()))
        pil_img.save(TEST_DIR / f"frame_{frame:03d}.png")

    print(f"Rendered unified test frames to {TEST_DIR}")

if __name__ == "__main__":
    main()
