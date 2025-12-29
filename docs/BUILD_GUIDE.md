# 构建说明文档

## 📋 构建脚本使用指南

本项目提供了多个构建脚本来满足不同的构建需求。

---

## 🔧 构建脚本列表

### 1. `build.py` - 基础构建脚本
**用途：** 简单的 macOS 构建，支持简单和完整两种模式

**使用方法：**
```bash
# 简单构建（推荐用于测试）
python3 build.py simple

# 完整构建（包含所有资源和元数据）
python3 build.py full

# 交互式选择
python3 build.py
```

---

### 2. `build_multi.py` - 多平台构建脚本
**用途：** 支持 macOS 和 Windows 平台的构建，自动重命名输出文件

**使用方法：**
```bash
# 构建当前平台版本（自动检测）
python3 build_multi.py

# 构建 macOS 版本
python3 build_multi.py macos

# 构建 Windows 版本（需要在 Windows 环境中运行）
python3 build_multi.py windows

# 构建所有支持的平台（在当前平台上）
python3 build_multi.py all
```

**输出文件：**
- macOS: `ImageSEOFriend-macOS.app`
- Windows: `ImageSEOFriend-Windows.exe`

---

## 📁 配置文件说明

### 1. `build_simple.spec` - 简单构建配置
- **用途：** 快速测试构建
- **特点：** 最小依赖，构建速度快
- **输出：** 单个可执行文件

### 2. `imgSEOfriend.spec` - macOS 完整构建配置
- **用途：** macOS 完整版发布
- **特点：** 包含 .app 包、完整元数据、代码签名
- **输出：** macOS .app 应用程序包

### 3. `imgSEOfriend_windows.spec` - Windows 完整构建配置
- **用途：** Windows 完整版发布
- **特点：** 包含版本信息、Windows 特定配置
- **输出：** Windows .exe 可执行文件

### 4. `version_info.txt` - Windows 版本信息
- **用途：** Windows 可执行文件的版本信息
- **包含：** 产品名称、版本号、版权信息等

---

## 🎯 构建流程

### macOS 构建流程
```bash
# 1. 环境检查
python3 --version  # 确认 Python 3.9+
pip3 list | grep PyInstaller  # 确认 PyInstaller 已安装

# 2. 构建应用
python3 build_multi.py macos

# 3. 验证构建
ls -la dist/ImageSEOFriend-macOS.app

# 4. 测试运行
open dist/ImageSEOFriend-macOS.app
```

### Windows 构建流程（在 Windows 环境中）
```bash
# 1. 环境检查
python --version
pip list | findstr PyInstaller

# 2. 构建应用
python build_multi.py windows

# 3. 验证构建
dir dist\ImageSEOFriend-Windows.exe

# 4. 测试运行
dist\ImageSEOFriend-Windows.exe
```

---

## 📦 构建输出

### 文件结构
```
dist/
├── ImageSEOFriend-macOS.app/          # macOS 应用程序包
│   └── Contents/
│       ├── MacOS/
│       │   └── ImageSEOFriend         # 主可执行文件
│       ├── Resources/
│       │   └── *.icns               # 应用图标
│       └── _CodeSignature/           # 代码签名
├── ImageSEOFriend-Windows.exe         # Windows 可执行文件
└── 其他临时文件...
```

### 文件大小参考
- **macOS .app 包：** ~58-60 MB
- **Windows .exe：** ~60-70 MB
- **简单构建：** ~52-55 MB

---

## 🛠️ 自定义构建

### 添加新的数据文件
编辑 `.spec` 文件中的 `datas` 部分：
```python
datas=[
    ('dark_theme.qss', '.'),
    ('assets/app_icon.ico', 'assets'),
    # 添加新的数据文件
    ('path/to/your/file', 'destination/folder'),
],
```

### 添加新的隐藏导入
编辑 `.spec` 文件中的 `hiddenimports` 部分：
```python
hiddenimports=[
    'PySide6.QtCore',
    # 添加新的隐藏导入
    'your_custom_module',
],
```

### 排除不需要的模块
编辑 `.spec` 文件中的 `excludes` 部分：
```python
excludes=[
    'tkinter',
    # 添加要排除的模块
    'matplotlib',
    'numpy',
],
```

---

## 🐛 常见问题

### 构建失败
1. **依赖问题：** 确认所有依赖都已正确安装
2. **权限问题：** 确认有写入构建目录的权限
3. **路径问题：** 确认在项目根目录执行构建脚本

### 运行时错误
1. **模块缺失：** 检查 `hiddenimports` 配置
2. **文件路径问题：** 检查 `datas` 配置
3. **平台兼容性：** 确认在目标平台上构建

### 性能优化
1. **减小文件大小：** 使用 `excludes` 排除不需要的模块
2. **启动速度：** 考虑使用 `onedir` 模式替代 `onefile`
3. **内存使用：** 优化应用程序的内存管理

---

## 📚 相关文档

- [PyInstaller 官方文档](https://pyinstaller.readthedocs.io/)
- [PySide6 部署指南](https://doc.qt.io/qtforpython-6/deployment.html)
- [macOS 应用程序打包](https://developer.apple.com/documentation/bundleresources)
- [Windows 应用程序部署](https://docs.microsoft.com/en-us/windows/uwp/packaging/)

---

**最后更新：** 2025-12-29  
**维护者：** Image SEO Optimizer 开发团队