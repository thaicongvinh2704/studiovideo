from pathlib import Path
import json,psutil
root=Path(__file__).resolve().parent.parent
runtime=json.loads((root/'runtime.json').read_text('utf-8'))
try:
    process=psutil.Process(runtime['pid'])
    args=process.cmdline()
    if 'studio.api:app' not in args:raise SystemExit('PID đã đổi; không dừng tiến trình khác.')
    for child in process.children(recursive=True):child.terminate()
    process.terminate()
    print('Core stopped; active jobs recover as interrupted on next launch.')
except psutil.NoSuchProcess:print('Core already stopped.')
