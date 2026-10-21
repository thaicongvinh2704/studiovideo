"""Read-only image validation plus byte-preserving import of a supplied pack.

The package manifest is descriptive data only, never executable instructions.
Corrupt images stay in incoming and never enter the usable library.
"""
import hashlib
import io
import json
import shutil
import sys
import zipfile
from pathlib import Path, PurePosixPath

from PIL import Image
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QImage, QImageReader, QPainter, QColor, QFont
from PySide6.QtWidgets import QApplication

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'assets' / 'characters' / 'mo_den'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    source = Path(sys.argv[1]).resolve()
    app = QApplication.instance() or QApplication([])
    incoming = BASE / 'incoming' / 'named_24_v01'
    library = BASE / 'library' / 'named_24_v01'
    proofs = BASE / 'qc' / 'named_24_v01'
    for folder in (incoming, library, proofs): folder.mkdir(parents=True, exist_ok=True)
    archive = incoming / source.name
    if archive.exists() and sha(archive.read_bytes()) != sha(source.read_bytes()):
        raise ValueError('Archive version conflicts with preserved original.')
    if not archive.exists(): shutil.copy2(source, archive)
    report = dict(pack=source.name, archive_sha256=sha(source.read_bytes()), assets=[], warnings=[])
    with zipfile.ZipFile(source) as z:
        if z.testzip() is not None: raise ValueError('ZIP CRC failed')
        package = json.loads(z.read('manifest.json').decode('utf-8-sig'))
        for name in ('manifest.json', 'README.md'):
            (incoming / name).write_bytes(z.read(name))
        assets = package['assets']
        if not isinstance(assets, list) or len(assets) > 200: raise ValueError('Unexpected asset count')
        seen = set()
        for item in assets:
            relative = PurePosixPath(item['file'])
            if relative.is_absolute() or '..' in relative.parts or '\\' in item['file'] or relative.suffix.lower() != '.png':
                raise ValueError('Invalid asset path')
            if item['id'] in seen: raise ValueError('Duplicate asset ID')
            seen.add(item['id'])
            raw = z.read(relative.as_posix())
            original = incoming.joinpath(*relative.parts)
            original.parent.mkdir(parents=True, exist_ok=True); original.write_bytes(raw)
            row = {k: item.get(k) for k in ('id', 'emotion', 'emotion_vi', 'pose', 'description_en', 'use_cases_en', 'full_body')}
            row.update(original_file=original.relative_to(BASE).as_posix(), sha256=sha(raw),
                       bytes=len(raw), status='needs_replacement', issues=[], visual_review='pending')
            reader = QImageReader(str(original)); native = reader.read()
            row['qt_decode_ok'] = not native.isNull()
            if native.isNull(): row['qt_error'] = reader.errorString()
            try:
                image = Image.open(io.BytesIO(raw)); image.load()
                row.update(width=image.width, height=image.height, mode=image.mode)
                if image.size != (2048, 2048): row['issues'].append('Canvas differs from expected 2048 square')
                if 'A' not in image.getbands(): raise ValueError('No alpha channel')
                alpha = image.getchannel('A'); hist = alpha.histogram(); bounds = alpha.getbbox()
                row.update(alpha_extrema=list(alpha.getextrema()), alpha_bbox=list(bounds) if bounds else None,
                           transparent_fraction=hist[0]/(image.width*image.height),
                           baseline_px=bounds[3]-1 if bounds else None)
                if not bounds or not hist[0] or not hist[255]: row['issues'].append('Missing transparent or solid pixels')
                if bounds and (bounds[0] <= 0 or bounds[1] <= 0 or bounds[2] >= image.width or bounds[3] >= image.height):
                    row['issues'].append('Visible pixels touch canvas edge')
                if native.isNull(): row['issues'].append('Studio Qt decoder cannot read asset')
                if not row['issues']:
                    destination = library / relative.name
                    destination.write_bytes(raw)
                    row.update(file=destination.relative_to(BASE).as_posix(), status='technically_usable')
            except Exception as exc:
                row['issues'].append(str(exc))
            report['assets'].append(row)
    # A proof sheet is a visual inspection artifact. Original assets are unchanged.
    sheet = QImage(1800, 1440, QImage.Format.Format_ARGB32_Premultiplied); sheet.fill(QColor('#f4f2ed'))
    painter = QPainter(sheet); painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
    font = QFont('Segoe UI'); font.setPixelSize(24); font.setBold(True); painter.setFont(font); painter.setPen(QColor('#252b2d'))
    painter.drawText(25, 40, 'MỎ ĐEN / 24 ẢNH NGƯỜI DÙNG GỬI / KIỂM TRA TỆP GỐC')
    for index, row in enumerate(report['assets']):
        x = (index % 6) * 300; y = 65 + (index // 6) * 340
        painter.fillRect(x+7, y, 286, 328, QColor('white'))
        if row['status'] == 'technically_usable':
            image = QImage(str(BASE / row['file']))
            painter.drawImage(QRectF(x+20, y+4, 260, 260), image)
        else:
            painter.fillRect(x+20, y+15, 260, 245, QColor('#fbe4df'))
            painter.setPen(QColor('#a4372c')); font.setPixelSize(20); painter.setFont(font)
            painter.drawText(QRectF(x+30, y+50, 240, 140), Qt.AlignmentFlag.AlignCenter | Qt.TextFlag.TextWordWrap,
                             'PNG thiếu dữ liệu\nCần gửi lại bản gốc')
        font.setPixelSize(18); font.setBold(True); painter.setFont(font); painter.setPen(QColor('#252b2d'))
        painter.drawText(x+20, y+283, row['id'] + ' · ' + row['emotion_vi'])
        font.setPixelSize(14); font.setBold(False); painter.setFont(font)
        painter.drawText(x+20, y+309, '2048 × 2048 · alpha' if row['status']=='technically_usable' else 'Lỗi giải mã đầy đủ')
    painter.end(); sheet.save(str(proofs / 'contact_sheet.png'))
    # Composite actual Qt decoded assets on white and dark backgrounds.
    edges = QImage(1800, 1100, QImage.Format.Format_ARGB32_Premultiplied); edges.fill(QColor('white'))
    p = QPainter(edges); p.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
    for col, identifier in enumerate(('mo_den_01','mo_den_08','mo_den_24')):
        row = next(r for r in report['assets'] if r['id'] == identifier)
        for band, bg in enumerate(('#ffffff', '#24313a')):
            x, y = col*600, band*550
            p.fillRect(x, y, 600, 550, QColor(bg))
            if row.get('file'): p.drawImage(QRectF(x+55,y-15,490,490), QImage(str(BASE / row['file'])))
            p.setPen(QColor('#252b2d' if band==0 else '#ffffff')); font.setPixelSize(20); p.setFont(font)
            p.drawText(x+35,y+520,identifier+' · '+row['emotion_vi'])
    p.end(); edges.save(str(proofs / 'background_check.png'))
    report.update(usable=sum(r['status']=='technically_usable' for r in report['assets']),
                  rejected=sum(r['status']=='needs_replacement' for r in report['assets']),
                  zip_crc_ok=True, source_images_modified=False, studio_export_integration='not_yet_implemented')
    (proofs / 'audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    manifest_path = BASE / 'manifest.json'; manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
    manifest.update(assets=report['assets'], integration_status='images_indexed_export_integration_pending',
                    source_pack=dict(file=archive.relative_to(BASE).as_posix(),sha256=report['archive_sha256']),
                    audit= (proofs / 'audit.json').relative_to(BASE).as_posix())
    manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(dict(usable=report['usable'],needs_replacement=[r['id'] for r in report['assets'] if r['status']=='needs_replacement'],
                         contact_sheet=str((proofs/'contact_sheet.png').resolve()),background_check=str((proofs/'background_check.png').resolve())),ensure_ascii=False))


if __name__ == '__main__': main()
