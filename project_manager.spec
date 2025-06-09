# project_manager.spec

block_cipher = None

import os
from PyInstaller.utils.hooks import collect_data_files

project_root = os.path.abspath(".")

datas = collect_data_files('gui', subdir=None) + \
        collect_data_files('core', subdir=None) + \
        collect_data_files('data', subdir=None) + \
        collect_data_files('utils', subdir=None) + \
        [(os.path.join(project_root, "file_templates"), "file_templates")]

hiddenimports = [
    'PyQt5.sip',
    'PyQt5.QtWidgets',
    'PyQt5.QtGui',
    'PyQt5.QtCore',
]

a = Analysis(
    ['PMT.py'],  # <-- If it's PMT.py, change this to 'PMT.py'
    pathex=[project_root],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ProjectManager',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ProjectManager'
)