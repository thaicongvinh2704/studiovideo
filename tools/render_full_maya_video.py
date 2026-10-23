"""Render the complete Maya documentary video (full 13m51s or custom segment)."""
import argparse
import sys
import time
from pathlib import Path
from PySide6.QtGui import QGuiApplication

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from studio.project import load
from studio.exporter import export_video

def main():
    parser = argparse.ArgumentParser(description="Render Maya Documentary Video")
    parser.add_argument("--start", type=float, default=0.0, help="Start time in seconds")
    parser.add_argument("--length", type=float, default=None, help="Length in seconds (default: full video)")
    parser.add_argument("--fps", type=int, default=24, choices=[12, 24, 30], help="Frames per second")
    parser.add_argument("--out", type=str, default="outputs/Mo_Den_Maya_Dao_Dien_Final_1080p.mp4", help="Output path")
    parser.add_argument("--gpu", action="store_true", default=True, help="Use GPU hardware encoding (NVENC)")
    args = parser.parse_args()

    app = QGuiApplication(sys.argv)

    project_path = ROOT / "projects" / "mo_den_maya" / "project.json"
    root_dir = ROOT / "projects" / "mo_den_maya"
    out_path = Path(args.out)
    if not out_path.is_absolute():
        out_path = ROOT / out_path
    out_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Loading project from {project_path}...", flush=True)
    p = load(project_path)

    total_len = p['scenes'][-1]['start'] + p['scenes'][-1]['duration']
    render_len = args.length if args.length is not None else (total_len - args.start)

    print(f"Total video length: {total_len:.1f}s | Segment to render: {render_len:.1f}s (Start: {args.start:.1f}s)")
    print(f"Resolution: {p['width']}x{p['height']} @ {args.fps} FPS")
    print(f"GPU Hardware Encoding: {args.gpu} (NVIDIA NVENC h264_nvenc)")
    print(f"Output will be saved to: {out_path}")

    start_time = time.monotonic()

    def progress(curr, total):
        pct = (curr / total) * 100
        elapsed = time.monotonic() - start_time
        fps_speed = curr / max(0.1, elapsed)
        remaining = (total - curr) / max(0.1, fps_speed)
        if curr % (args.fps * 5) == 0 or curr == total:
            print(f"[{pct:5.1f}%] Frame {curr}/{total} | Speed: {fps_speed:.1f} fps | ETA: {remaining/60:.1f} min", flush=True)

    export_video(p, root_dir, out_path, start=args.start, length=render_len, width=p['width'], height=p['height'], fps=args.fps, progress=progress, gpu=args.gpu)

    elapsed_total = time.monotonic() - start_time
    print(f"Successfully finished export in {elapsed_total/60:.1f} minutes!")
    print(f"File created: {out_path} ({out_path.stat().st_size / 1024**2:.1f} MB)")

if __name__ == "__main__":
    main()
