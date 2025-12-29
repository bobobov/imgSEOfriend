# -*- mode: python ; coding: utf-8 -*-

"""
PyInstaller 简化配置文件 - Image SEO Optimizer
用于快速打包测试
"""

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('dark_theme.qss', '.'),  # 包含样式文件
        ('assets/app_icon.ico', 'assets'),  # 包含图标文件
    ],
    hiddenimports=[
        'PySide6.QtCore',
        'PySide6.QtGui', 
        'PySide6.QtWidgets',
        'PIL',
        'requests',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ImageSEOFriend',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/app_icon.ico',  # 应用程序图标
)