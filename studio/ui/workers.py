import threading
from PySide6.QtCore import QThread, Signal

class Worker(QThread):
    done=Signal(object)
    failed=Signal(str)
    progress=Signal(int,int)
    def __init__(self,function,parent=None):
        super().__init__(parent)
        self.function=function
        self.cancel=threading.Event()
    def run(self):
        try: self.done.emit(self.function(self))
        except Exception as exc:
            import traceback
            import sys
            if sys.stderr is not None:traceback.print_exc()
            self.failed.emit(str(exc))
