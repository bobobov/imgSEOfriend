# -*- mode: python ; coding: utf-8 -*-

"""
PyInstaller 配置文件 - Image SEO Optimizer
用于将应用程序打包为独立的可执行文件
"""

import os
import sys
from pathlib import Path

# 获取项目根目录
ROOT_DIR = Path.cwd()

# 分析主程序
a = Analysis(
    ['app.py'],  # 主入口文件
    pathex=[str(ROOT_DIR)],  # 项目路径
    binaries=[],
    datas=[
        # 包含样式文件
        ('dark_theme.qss', '.'),
        # 包含图标文件
        ('assets/app_icon.ico', 'assets'),
        # 包含文档文件（可选）
        ('README.md', '.'),
        ('md/PROJECT_SUMMARY.md', 'md'),
        ('md/SECURITY_GUIDE.md', 'md'),
        ('md/HEIC_HEIF_SUPPORT.md', 'md'),
        # 如果有其他资源文件，可以在这里添加
        # ('assets/*', 'assets'),
        # ('icons/*', 'icons'),
    ],
    hiddenimports=[
        # PySide6 相关模块
        'PySide6.QtCore',
        'PySide6.QtGui', 
        'PySide6.QtWidgets',
        'PySide6.QtMultimedia',
        'PySide6.QtMultimediaWidgets',
        # 图像处理库
        'PIL',
        'PIL.Image',
        'PIL.ImageQt',
        'PIL.ImageFilter',
        'PIL.ImageEnhance',
        # 其他可能需要的隐藏导入
        'requests',
        'json',
        'threading',
        'queue',
        'asyncio',
        'pathlib',
        'configparser',
        'logging',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # 排除不需要的模块以减小包大小
        'tkinter',
        'matplotlib',
        'numpy',
        'scipy',
        'pandas',
        'jupyter',
        'notebook',
        'IPython',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

# PYZ 文件
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# 可执行文件配置
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ImageSEOFriend',  # 可执行文件名
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # 使用 UPX 压缩（如果可用）
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 不显示控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # macOS 特定选项
    icon='assets/app_icon.ico',  # 应用程序图标
    bundle_identifier='com.imageseo.friend',
    info_plist={
        'CFBundleName': 'Image SEO Friend',
        'CFBundleDisplayName': 'Image SEO Optimizer',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleExecutable': 'ImageSEOFriend',
        'CFBundleIdentifier': 'com.imageseo.friend',
        'NSHighResolutionCapable': True,
        'LSApplicationCategoryType': 'public.app-category.graphics-design',
        'CFBundleDocumentTypes': [
            {
                'CFBundleTypeName': 'Image',
                'CFBundleTypeExtensions': ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp', 'heic', 'heif'],
                'CFBundleTypeRole': 'Editor',
            }
        ],
    },
)

# macOS 特定：创建 .app 包
app = BUNDLE(
    exe,
    name='ImageSEOFriend.app',
    icon='assets/app_icon.ico',  # 应用程序图标
    bundle_identifier='com.imageseo.friend',
    info_plist={
        'CFBundleName': 'Image SEO Friend',
        'CFBundleDisplayName': 'Image SEO Optimizer',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleExecutable': 'ImageSEOFriend',
        'CFBundleIdentifier': 'com.imageseo.friend',
        'NSHighResolutionCapable': True,
        'LSApplicationCategoryType': 'public.app-category.graphics-design',
        'CFBundleDocumentTypes': [
            {
                'CFBundleTypeName': 'Image',
                'CFBundleTypeExtensions': ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp', 'heic', 'heif'],
                'CFBundleTypeRole': 'Editor',
            }
        ],
    },
)