"""Studio local editing helpers; run with the existing Studio Python."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from studio import editing_tools as tools


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest='command', required=True)
    subs.add_parser('doctor')
    subs.add_parser('start-vision')
    glax = subs.add_parser('glaxnimate')
    glax.add_argument('file', nargs='?')
    review = subs.add_parser('review-frame')
    review.add_argument('--image', required=True)
    review.add_argument('--narration', required=True)
    review.add_argument('--expected', required=True)
    review.add_argument('--output', required=True)
    align = subs.add_parser('align')
    align.add_argument('--audio', required=True)
    align.add_argument('--srt', required=True)
    align.add_argument('--output', required=True)
    args = parser.parse_args()
    if args.command == 'doctor':
        result = tools.doctor()
    elif args.command == 'start-vision':
        result = tools.ensure_vision_server()
    elif args.command == 'glaxnimate':
        tools.open_vector_editor(args.file)
        return 0
    elif args.command == 'align':
        return subprocess.run(tools.align_command(args.audio, args.srt, args.output),
                              env=tools.environment(), creationflags=tools.NO_WINDOW).returncode
    else:
        result = tools.review_frame(args.image, args.narration, args.expected)
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
