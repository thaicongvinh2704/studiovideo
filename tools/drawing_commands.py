"""Agent-facing JSON command API. No eval, no generated bitmaps.

Example: python tools/drawing_commands.py in.drawing.json --commands edits.json
         --output out.drawing.json --preview preview.png
The preview is a draft render; --svg additionally requires final QC.
"""
import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
from PySide6.QtWidgets import QApplication
from studio import drawing
from studio.drawing_edit import apply_command
from studio.character_qc import drawing_issues


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('--commands', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--preview', type=Path)
    parser.add_argument('--svg', type=Path)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    app = QApplication.instance() or QApplication([])
    try:
        doc = drawing.validate(json.loads(args.input.read_text(encoding='utf-8-sig')))
        commands = json.loads(args.commands.read_text(encoding='utf-8-sig'))
        if not isinstance(commands, list): raise ValueError('Tệp lệnh phải là danh sách JSON.')
        for command in commands: doc = apply_command(doc, command)
        if args.svg:
            problems = drawing_issues(doc, args.root)
            if problems: raise ValueError('Chưa được xuất thành phẩm: ' + '; '.join(problems))
        drawing.save_drawing(doc, args.output)
        if args.preview:
            args.preview.parent.mkdir(parents=True, exist_ok=True)
            if not drawing.render(doc).save(str(args.preview)): raise OSError('Không lưu được preview.')
        if args.svg:
            args.svg.parent.mkdir(parents=True, exist_ok=True)
            args.svg.write_text(drawing.svg(doc)[0], encoding='utf-8')
        print(json.dumps(dict(output=str(args.output.resolve()), commands=len(commands),
                              preview_is_draft=True, qc_issues=drawing_issues(doc, args.root)), ensure_ascii=False))
    except (ValueError, KeyError, IndexError, TypeError, OSError) as exc:
        print(str(exc), file=sys.stderr); return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
