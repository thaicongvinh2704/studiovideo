"""Compare bundled imports with exported procedures, without inspecting user apps."""
from pathlib import Path
import pefile

root=Path(__file__).resolve().parents[1]/'dist'/'StickmanAnimationStudio'/'_internal'
files={p.name.lower():p for p in root.rglob('*.dll')}
files.update({p.name.lower():p for p in root.glob('*.dll')})
cache={}
names=[root/'PySide6'/'QtCore.pyd',root/'PySide6'/'Qt6Core.dll',root/'PySide6'/'pyside6.abi3.dll',root/'shiboken6'/'shiboken6.abi3.dll']
for p in names:
    pe=pefile.PE(str(p))
    print(p.name,'imports:',[i.dll.decode() for i in pe.DIRECTORY_ENTRY_IMPORT],flush=True)
    for imp in pe.DIRECTORY_ENTRY_IMPORT:
        dll=imp.dll.decode().lower()
        if dll not in files:continue
        if dll not in cache:
            dependency=pefile.PE(str(files[dll]))
            cache[dll]={e.name for e in getattr(dependency,'DIRECTORY_ENTRY_EXPORT').symbols}
        for function in imp.imports:
            if function.name and function.name not in cache[dll]:
                print('MISSING EXPORT:',p.name,dll,function.name.decode(),flush=True)
