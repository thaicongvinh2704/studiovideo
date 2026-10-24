from PIL import Image
from pathlib import Path

img_dir = Path('projects/mo_den_phong_than/assets/Mo_Den_Phong_Than_V2/images')
files = ['Y02.png', 'Y02_B.png', 'B16.png', 'A01.png', 'A04.png', 'A05.png', 'C_JZ.png', 'C_WZ.png', 'O01.png', 'O05.png']

for f in files:
    p = img_dir / f
    if p.exists():
        im = Image.open(p)
        alpha_info = im.getchannel('A').getextrema() if im.mode == 'RGBA' else 'No Alpha (RGB)'
        print(f"{f:10s} | {im.size} | {im.mode} | alpha: {alpha_info}")
    else:
        print(f"{f:10s} | MISSING")
