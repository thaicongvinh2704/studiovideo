"""Preserve an existing app folder before PyInstaller creates a new build."""
from pathlib import Path
from datetime import datetime

root=Path(__file__).resolve().parents[1]
dist=(root/'dist').resolve();target=dist/'StickmanAnimationStudio'
if target.exists():
    if target.is_symlink() or not target.resolve().is_relative_to(dist):
        raise RuntimeError('Build target nằm ngoài thư mục dist; không di chuyển.')
    backup=dist/('StickmanAnimationStudio_backup_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
    if not backup.resolve().is_relative_to(dist):raise RuntimeError('Đường dẫn backup không hợp lệ.')
    target.rename(backup)
    print('Preserved existing app, editable demo and local projects:',backup)
