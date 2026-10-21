"""Prepare a QC packet, or record a separately written review after visual inspection.

There is intentionally no --auto-pass option. New drawings stay drafts until reviewed.
"""
import argparse
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from PySide6.QtWidgets import QApplication
from studio.drawing import validate, save_drawing
from studio.character_qc import is_character, prepare_packet, record_review, geometry_issues, review_issues


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('drawing'); parser.add_argument('--root', default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument('--review', help='JSON with reviewer and individually documented checks; inspect current images first')
    parser.add_argument('--output', help='Save updated drawing, default overwrites the supplied drawing')
    args = parser.parse_args()
    app = QApplication.instance() or QApplication([])
    doc = validate(json.loads(Path(args.drawing).read_text(encoding='utf-8-sig')))
    entries = [e for e in doc['layers'] if is_character(e)]
    if len(entries) != 1: parser.error('QC một nhân vật mỗi lần; bản vẽ cần đúng một lớp nhân vật.')
    entry = entries[0]
    if args.review:
        notes = json.loads(Path(args.review).read_text(encoding='utf-8-sig'))
        record_review(entry, args.root, notes['checks'], notes['reviewer'])
        print('Recorded internal QC for the current revision; not user approval.')
    else:
        packet = prepare_packet(entry, args.root)
        print(json.dumps(dict(geometry_issues=geometry_issues(entry), evidence=packet['evidence'], status='pending_visual_review'), ensure_ascii=False, indent=2))
    save_drawing(doc, args.output or args.drawing)


if __name__ == '__main__': main()
