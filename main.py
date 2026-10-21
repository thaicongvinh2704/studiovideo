"""Bootstrap with a disk error log for windowed Windows builds."""
import sys
from pathlib import Path
import traceback

if __name__ == '__main__':
    try:
        from studio.app import main
        main()
    except Exception:
        root=Path(sys.executable).parent if getattr(sys,'frozen',False) else Path(__file__).resolve().parent
        log=root/'launch-error.log'
        log.write_text(traceback.format_exc(),encoding='utf-8')
        if sys.stderr is not None:traceback.print_exc()
        sys.exit(1)
