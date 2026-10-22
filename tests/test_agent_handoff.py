"""Ownership contention and checkpoint honesty, independent of AI providers."""
import json
import io
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from tools.agent_handoff import change_owner, checkpoint, command, main, media_status, read_state, state_lock


class AgentHandoffTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1] / "outputs")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / "coordination").mkdir()
        (self.root / "coordination/state.json").write_text(
            json.dumps({"version": 1, "active_writer": "codex"}), encoding="utf-8")

    def test_other_agent_cannot_claim_or_release_active_writer(self):
        before = (self.root / "coordination/state.json").read_bytes()
        for kwargs in ({}, {"release": True}):
            with self.assertRaises(RuntimeError):
                change_owner(self.root, "antigravity", **kwargs)
        self.assertEqual(before, (self.root / "coordination/state.json").read_bytes())
        self.assertFalse((self.root / "coordination/.state.lock").exists())

    def test_release_then_claim_and_explicit_takeover(self):
        change_owner(self.root, "codex", release=True)
        change_owner(self.root, "antigravity")
        self.assertEqual(read_state(self.root)["active_writer"], "antigravity")
        change_owner(self.root, "codex", takeover=True)
        self.assertEqual(read_state(self.root)["active_writer"], "codex")

    def test_state_mutex_is_not_bypassed_or_removed(self):
        with state_lock(self.root):
            with self.assertRaises(RuntimeError):
                change_owner(self.root, "codex")
            self.assertTrue((self.root / "coordination/.state.lock").exists())
        self.assertFalse((self.root / "coordination/.state.lock").exists())

    def test_checkpoint_preserves_git_failure_as_unknown_not_clean(self):
        failure = {"ok": False, "error": "LFS access denied"}
        with patch("tools.agent_handoff.shutil.which", return_value="git"), \
             patch("tools.agent_handoff.command", return_value=failure):
            data = checkpoint(self.root, "codex", "Incomplete environment", "Fix access")
        self.assertFalse(data["git"]["working_tree"]["ok"])
        self.assertNotIn("output", data["git"]["working_tree"])
        saved = json.loads((self.root / "coordination/checkpoint.json").read_text(encoding="utf-8"))
        self.assertEqual(saved["next_action"], "Fix access")

    def test_lfs_pointer_is_not_reported_as_real_media(self):
        path = self.root / "audio.wav"
        path.write_bytes(b"version https://git-lfs.github.com/spec/v1\noid sha256:abc\nsize 5\n")
        self.assertTrue(media_status(path)["lfs_pointer"])
        path.write_bytes(b"RIFFactual audio header")
        self.assertFalse(media_status(path)["lfs_pointer"])
        self.assertFalse(media_status(self.root / "missing.wav")["exists"])

    def test_porcelain_staged_vs_unstaged_spacing_is_preserved(self):
        result = command(self.root, [sys.executable, "-c", "print(' M source.py')"])
        self.assertTrue(result["ok"])
        self.assertEqual(result["output"], " M source.py")

    def test_windows_legacy_console_can_print_vietnamese_state(self):
        path = self.root / "coordination/state.json"
        state = json.loads(path.read_text(encoding="utf-8"))
        state["objective"] = "Tiếp quản Mỏ Đen"
        path.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
        buffer = io.BytesIO()
        console = io.TextIOWrapper(buffer, encoding="ascii")
        with patch("tools.agent_handoff.ROOT", self.root), \
             patch("sys.stdout", console), \
             patch("sys.argv", ["agent_handoff.py", "claim", "--owner", "codex"]):
            self.assertEqual(main(), 0)
            console.flush()
            self.assertEqual(json.loads(buffer.getvalue().decode("utf-8"))["objective"], state["objective"])


if __name__ == "__main__":
    unittest.main()
