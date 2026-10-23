"""Test compositing the tail onto the symmetric body at several angles."""
import sys
from pathlib import Path
from PIL import Image
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter, QImage, QGuiApplication

WORKDIR = Path("projects/mo_den_motion_demo/back_wiggle")

def main():
    app = QGuiApplication.instance() or QGuiApplication(sys.argv)
    body_img = QImage(str(WORKDIR / "test_symmetric_body.png"))
    tail_img = QImage(str(WORKDIR / "layer_tail_vector.png"))

    W, H = body_img.width(), body_img.height()

    for angle in [-30, 0, 30]:
        out = QImage(W, H, QImage.Format.Format_ARGB32_Premultiplied)
        out.fill(Qt.GlobalColor.white)

        p = QPainter(out)
        p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        p.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)

        # 1. Draw Body
        p.drawImage(0, 0, body_img)

        # 2. Draw Tail
        # Root in tail image is at (45, 425)
        # Position on body: the cleft of the buttocks is around (512, 750)
        p.save()
        p.translate(512, 750)
        p.rotate(angle)
        # Translate so tail root (45, 425) aligns with (0, 0)
        p.translate(-45, -425)
        p.drawImage(0, 0, tail_img)
        p.restore()

        p.end()

        # Save safely
        rgba = out.convertToFormat(QImage.Format.Format_RGBA8888)
        pil_img = Image.frombytes("RGBA", (W, H), bytes(rgba.constBits()))
        pil_img.save(WORKDIR / f"test_composite_angle_{angle}.png")
        print(f"Saved test_composite_angle_{angle}.png")

if __name__ == "__main__":
    main()
