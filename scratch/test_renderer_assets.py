from pathlib import Path
import sys
sys.path.insert(0, str(Path('.').resolve()))

from PySide6.QtGui import QGuiApplication
app = QGuiApplication(sys.argv)
from studio.renderer import Renderer
from studio.project import resolve

root = Path('projects/mo_den_phong_than').resolve()
r = Renderer()

test_files = [
    'assets/Mo_Den_Phong_Than_V2/images/K01.png',
    'assets/Mo_Den_Phong_Than_V2/images/Y01.png',
    'assets/Mo_Den_Phong_Than_V2/images/Y08.png',
    'assets/Mo_Den_Phong_Than_V2/images/Y09.png',
    'assets/Mo_Den_Phong_Than_V2/images/B14.png',
    'assets/Mo_Den_Phong_Than_V2/images/K15.png',
    'assets/Mo_Den_Phong_Than_V2/diagrams/D01_Hai_Menh_Lenh.png',
    'assets/Mo_Den_Phong_Than_V2/sequences/E01_A.png',
    '../../assets/characters/mo_den/library/named_24_v01/mo_den_01_neutral_seated_paws_resting.png'
]

for tf in test_files:
    resolved = resolve(root, tf)
    im = r.image(root, tf)
    print(f"OK: {tf} -> {resolved.name} ({im.width()}x{im.height()})")

print("ALL TEST FILES LOADED SUCCESSFULLY BY RENDERER!")
