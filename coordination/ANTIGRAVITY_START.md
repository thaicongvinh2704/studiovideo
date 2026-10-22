# Initial assignment in the official Antigravity client

The human user asked you to support this Studio and take over authorized work
if Codex becomes unavailable. This file is a task the user sends directly to you,
not an automated call from Codex. Report in Vietnamese.

Do AG-001 first; do not start a full video or regenerate narration. Read
`AGENTS.md`, `GEMINI.md`, `AGENT_HANDOFF.md`, `projects/mo_den_maya/HANDOFF.md`,
`coordination/state.json`, `coordination/tasks.json` and the latest checkpoint.
Verify live files instead of trusting old factual status. User instructions win.

## Produce your own evidence

1. Explain the current mascot and rejected designs, Maya voice H, Northern
   Vietnamese, speed applied once, and technical versus visual/listening QC.
   Point to actual source files. Identify the pending task.
2. Check current Git status/diff and running jobs. Preserve existing changes.
   Claim ownership with `python tools/agent_handoff.py claim --owner antigravity`
   before writing. If another writer is active, stop edits and tell the user;
   use `--takeover` only when they directly transfer work.
3. Probe Python/tools with `tools/agent_handoff.py status`. Default Python might
   lack PySide6; an existing Qt environment is documented in the handoff. Report
   actual dependencies instead of assuming source-machine paths work.
4. With a working Qt interpreter and `QT_QPA_PLATFORM=offscreen`, run:

   ```powershell
   python -X utf8 -m unittest discover -s tests -p 'test_agent_handoff.py' -v
   python -X utf8 -m unittest discover -s tests -p 'test_supplied_character.py' -v
   python -X utf8 -m unittest discover -s tests -p 'test_media_delivery.py' -v
   python -X utf8 -m unittest discover -s tests -p 'test_vietnamese_narration.py' -v
   ```

   Replace `python` with a verified interpreter if needed. Tests create temporary
   files. If still in Plan mode, explain which steps need an execution-enabled
   mode in the official client; do not claim execution. Record exact commands,
   exit codes, counts and skips/errors. Failures are findings, not permission to
   edit source during AG-001.
5. Use ffprobe on `projects/mo_den_maya/assets/audio/narration.wav` and
   `outputs/Mo_Den_Maya_Dao_Dien_Final_1080p.mp4`. Report actual codec/duration/
   frame size. This is technical evidence, not approval of the film or voice.
6. Read `assets/characters/mo_den/README.md` and `manifest.json`; open one indexed
   PNG with a real image-viewing tool, describe observations and its exact path.
   If no image tool is available, mark visual inspection NOT_EVALUATED. Do not
   invent observation from a filename or manifest. Do not generate art.
7. Write `coordination/reports/antigravity_acceptance.md` with a capability table:
   repo understanding, shell/test, media probing, image viewing, runtime for NEW
   voice synthesis, and actual audio listening. Use VERIFIED / FAILED /
   NOT_EVALUATED with evidence. New synthesis and listening are NOT_EVALUATED
   unless actually authorized/performed; metadata is not listening.
8. Update AG-001 and `state.json`'s capability status honestly. Partial success
   permits the corresponding technical work, not every production role. Release
   ownership and save a checkpoint with the next concrete step.

## Full takeover later

When the human asks you to continue Codex's unfinished work, read current state
and diff again, claim ownership and continue the last authorized objective.
You can act as technical lead; do not stay a reviewer just because Codex held
that role before. Do not wait for Codex's quota to reset. Preserve production
requirements and record progress after each milestone. If no production task is
currently authorized, report readiness and limitations; do not invent an episode
or redo accepted narration.
