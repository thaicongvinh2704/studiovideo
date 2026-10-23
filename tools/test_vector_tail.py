"""Render an authentic silky-smooth vector tail with exact Siamese dark brown and glossy highlight."""
from pathlib import Path
from PIL import Image
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter, QPainterPath, QColor, QPen, QImage, QLinearGradient

WORKDIR = Path("projects/mo_den_motion_demo/back_wiggle")

INK = QColor("#080807")
BROWN = QColor("#3e271d")
BROWN_LIGHT = QColor("#543628")
HIGHLIGHT = QColor(255, 255, 255, 180)

def main():
    W, H = 300, 450
    qimg = QImage(W, H, QImage.Format.Format_ARGB32_Premultiplied)
    qimg.fill(Qt.GlobalColor.transparent)

    p = QPainter(qimg)
    p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    p.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)

    # Tail centerline path from root to tip
    path = QPainterPath()
    # Root at bottom left (45, 425)
    path.moveTo(45, 425)
    # Gentle S-curve up
    path.cubicTo(100, 360, 115, 260, 95, 170)
    path.cubicTo(85, 110, 130, 55, 195, 50)
    path.cubicTo(250, 45, 265, 80, 260, 125)

    # 1. Dark outline (outer stroke)
    pen_outline = QPen(INK, 68.0, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
    p.setPen(pen_outline)
    p.drawPath(path)

    # 2. Main brown fill (inner stroke)
    pen_fill = QPen(BROWN, 54.0, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
    p.setPen(pen_fill)
    p.drawPath(path)

    # 3. Soft internal gradient / highlight stroke along outer crest
    # Outer crest from y=170 up around the curve to the tip
    hl_path = QPainterPath()
    hl_path.moveTo(85, 170)
    hl_path.cubicTo(77, 115, 125, 42, 195, 38)
    hl_path.cubicTo(240, 35, 258, 65, 255, 100)

    hl_pen = QPen(HIGHLIGHT, 5.0, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
    p.setPen(hl_pen)
    p.drawPath(hl_path)

    p.end()

    # Save to PIL
    raw = qimg.convertToFormat(QImage.Format.Format_RGBA8888).constBits()
    pil_img = Image.frombytes("RGBA", (W, H), bytes(raw))
    pil_img.save(WORKDIR / "layer_tail_vector.png")
    print("Saved layer_tail_vector.png")

if __name__ == "__main__":
    main()
