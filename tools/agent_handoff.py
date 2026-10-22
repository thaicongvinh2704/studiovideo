"""Local cooperative ownership/checkpoints. Never invokes an AI or reads credentials."""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
OWNERS = ("codex", "antigravity")
REQUIRED = (
    "AGENTS.md", "GEMINI.md", "AGENT_HANDOFF.md",
    "coordination/ANTIGRAVITY_START.md", "coordination/tasks.json",
    "projects/mo_den_maya/HANDOFF.md",
    "assets/characters/mo_den/manifest.json",
    "projects/mo_den_maya/voice_direction/selected_voice_H.json",
)
MEDIA = (
    "projects/mo_den_maya/assets/audio/narration.wav",
    "outputs/Mo_Den_Maya_Dao_Dien_Final_1080p.mp4",
    "projects/mo_den_maya/director_v2/Mo_Den_Maya_Dao_Dien_V2_1080p.mp4",
)


def now():
    return datetime.now(timezone.utc).isoformat()


def read_state(root):
    state = json.loads((root / "coordination/state.json").read_text(encoding="utf-8-sig"))
    if (state.get("version") != 1 or "active_writer" not in state
            or state["active_writer"] not in (None, *OWNERS)):
        raise ValueError("Invalid shared state; inspect it before changing ownership.")
    return state


def atomic_json(path, data):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


@contextmanager
def state_lock(root):
    lock = root / "coordination/.state.lock"
    try:
        handle = lock.open("x", encoding="utf-8")
    except FileExistsError as exc:
        raise RuntimeError("State lock exists; inspect the writer before retrying.") from exc
    try:
        with handle:
            handle.write(str(os.getpid()))
        yield
    finally:
        lock.unlink()


def change_owner(root, owner, *, release=False, takeover=False):
    with state_lock(root):
        state = read_state(root)
        previous = state["active_writer"]
        if release:
            if previous != owner:
                raise RuntimeError("Only the current writer may release ownership.")
            state["active_writer"] = None
        else:
            if previous not in (None, owner) and not takeover:
                raise RuntimeError("Another agent owns edits. Human transfer is required for --takeover.")
            state["active_writer"] = owner
        state["last_transition_utc"] = now()
        atomic_json(root / "coordination/state.json", state)
    return state


def command(root, args):
    try:
        result = subprocess.run(args, cwd=root, capture_output=True, text=True,
                                encoding="utf-8", errors="replace", timeout=30)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"ok": False, "error": str(exc)}
    if result.returncode:
        return {"ok": False, "exit_code": result.returncode,
                "error": result.stderr.strip()[-1500:]}
    return {"ok": True, "output": result.stdout.rstrip("\r\n")}


def media_status(path):
    if not path.is_file():
        return {"exists": False}
    with path.open("rb") as stream:
        is_pointer = stream.read(128).startswith(b"version https://git-lfs.github.com/spec/v1")
    return {"exists": True, "bytes": path.stat().st_size, "lfs_pointer": is_pointer}


def snapshot(root):
    git = shutil.which("git")
    git_state = {"available": bool(git)}
    if git:
        # Keep normal LFS semantics. On sandbox failure, record UNKNOWN/error,
        # never an empty clean tree or a false modified hydrated media file.
        for name, args in (
            ("head", ["rev-parse", "HEAD"]),
            ("origin_main", ["rev-parse", "origin/main"]),
            ("working_tree", ["status", "--porcelain=v1", "--untracked-files=all"]),
        ):
            git_state[name] = command(root, [git, "--no-optional-locks", *args])
    modules = {name: importlib.util.find_spec(name) is not None
               for name in ("PySide6", "PIL", "piper")}
    return {
        "version": 1, "created_utc": now(), "repo_root": str(root),
        "state": read_state(root), "git": git_state,
        "runtime": {"python": sys.executable, "python_version": sys.version.split()[0],
                    "modules": modules,
                    "ffmpeg": shutil.which("ffmpeg"), "ffprobe": shutil.which("ffprobe")},
        "required_files": {p: (root / p).is_file() for p in REQUIRED},
        "media": {p: media_status(root / p) for p in MEDIA},
        "not_verified_by_this_tool": ["agent_model_response", "Antigravity abilities",
                                     "new_voice_synthesis", "visual_quality", "listening_qc"],
    }


def checkpoint(root, owner, summary, next_action):
    with state_lock(root):
        state = read_state(root)
        if state["active_writer"] not in (None, owner):
            raise RuntimeError("Another writer owns this repository checkpoint.")
        data = snapshot(root)
        data.update(author=owner, summary=summary, next_action=next_action)
        atomic_json(root / "coordination/checkpoint.json", data)
    return data


def main():
    # Windows launchers may inherit a legacy code page even with Vietnamese state.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="operation", required=True)
    subs.add_parser("status", help="Read current environment and Git state; no model call")
    claim = subs.add_parser("claim", help="Acquire cooperative writer ownership")
    claim.add_argument("--owner", choices=OWNERS, required=True)
    claim.add_argument("--takeover", action="store_true", help="Only after a human transfers work")
    release = subs.add_parser("release")
    release.add_argument("--owner", choices=OWNERS, required=True)
    save = subs.add_parser("checkpoint")
    save.add_argument("--owner", choices=OWNERS, required=True)
    save.add_argument("--summary", required=True)
    save.add_argument("--next", required=True, dest="next_action")
    args = parser.parse_args()
    try:
        if args.operation == "status":
            data = snapshot(ROOT)
        elif args.operation == "checkpoint":
            data = checkpoint(ROOT, args.owner, args.summary, args.next_action)
        else:
            data = change_owner(ROOT, args.owner, release=args.operation == "release",
                                takeover=getattr(args, "takeover", False))
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, RuntimeError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
