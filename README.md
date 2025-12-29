# Image SEO Optimizer - AI驱动的图片SEO优化工具

<div align="center">

![Image SEO Optimizer](https://img.shields.io/badge/Image%20SEO%20Optimizer-AI%20Powered-blue?style=for-the-badge)

[![Python](https://img.shields.io/badge/Python-3.9%2B-green?style=flat-square)](https://www.python.org/)
[![PySide6](https://img.shields.io/badge/PySide6-Desktop%20GUI-blue?style=flat-square)](https://doc.qt.io/qtforpython/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Windows-lightgrey?style=flat-square)](#-构建与部署)

🚀 **版本 1.0.0** | 📦 [下载发布版本](https://github.com/bobobov/imgSEOfriend/releases) | 🐛 [报告问题](https://github.com/bobobov/imgSEOfriend/issues)

一个基于AI的专业图片SEO优化工具，支持批量处理、格式转换、自动生成SEO元数据。支持多平台部署，提供独立可执行文件。

[功能特性](#-功能特性) • [快速开始](#-快速开始) • [构建与部署](#-构建与部署) • [使用指南](#-使用指南)

</div>

## 🚀 功能特性

### 🖼️ 智能图片处理
- **格式转换**: 自动转换为WebP格式，大幅减小文件体积
- **尺寸优化**: 智能调整图片尺寸，保持最佳质量与大小平衡
- **HEIC/HEIF支持**: 完整支持苹果设备的HEIC格式图片
- **方向修复**: 自动识别并修复手机拍摄的旋转问题

### 🤖 AI智能优化
- **SEO元数据生成**: 基于关键词自动生成优化的Title和Alt Text
- **多模型支持**: 兼容OpenAI、DeepSeek、Gemini等主流AI服务
- **自定义Prompt**: 支持自定义AI生成模板，满足不同需求

### 🎨 专业界面
- **Before/After对比**: 直观的拖拽对比组件，实时查看优化效果
- **文件信息显示**: 详细的文件大小、尺寸信息展示
- **深色主题**: 现代化的深色界面，保护眼睛

### ⚡ 性能优化
- **异步处理**: 非阻塞的图片加载和处理，流畅的用户体验
- **内存优化**: 高效的图片处理算法，支持大文件处理
- **快速响应**: 优化的拖拽体验，即时反馈

## 📸 界面预览

<div align="center">

![Image SEO Optimizer 界面](screenshots/SCR-20251229-jozl.png)

**主界面** - 简洁直观的操作体验

</div>

## 📦 系统要求

### 开发环境
- **操作系统**: macOS 10.15+, Windows 10+, Linux (Ubuntu 20.04+)
- **Python版本**: 3.9+ 或更高版本
- **内存**: 建议 4GB+ RAM
- **存储**: 至少 100MB 可用空间

### 发布版本
- **macOS**: macOS 10.15+ (Catalina) - Intel 架构
- **Windows**: Windows 10+ (x64)
- **内存**: 4GB+ RAM
- **存储**: 200MB+ 可用空间
- **网络**: 互联网连接（AI服务需要）

## 🛠️ 安装指南

### 🎯 方法一：下载发布版本（推荐）

**macOS:**
1. 下载 `ImageSEOFriend-macOS.app`
2. 双击运行（可能需要在系统偏好设置中允许运行）

**Windows:**
1. 下载 `ImageSEOFriend-Windows.exe`
2. 双击运行

### 🔧 方法二：从源码运行

```bash
# 克隆项目
git clone https://github.com/bobobov/imgSEOfriend.git
cd imgSEOfriend

# 安装依赖
pip3 install PySide6 Pillow requests cryptography

# 启动应用
python3 app.py
```

### 🛠️ 方法三：开发环境设置

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip3 install -r requirements.txt

# 运行应用
python3 app.py
```

## 📋 依赖包

主要依赖包（requirements.txt）：

```
PySide6>=6.5.0
Pillow>=9.0.0
pillow-heif>=0.12.0
requests>=2.28.0
```

开发依赖（requirements-dev.txt）：

```
pytest>=7.0.0
black>=22.0.0
flake8>=5.0.0
mypy>=1.0.0
```

## 🎯 使用指南

### 基本使用流程

1. **启动应用**: 双击运行或命令行启动 `python app.py`
2. **拖入图片**: 将图片文件拖拽到应用窗口的预览区域
3. **设置参数**:
   - 输入目标关键词
   - 选择输出宽度（1200px/800px/600px/原始尺寸）
4. **AI设置**: 配置AI服务提供商和API密钥
5. **开始处理**: 点击"开始处理"按钮
6. **查看结果**: 在Before/After对比界面查看优化效果
7. **编辑元数据**: 调整AI生成的SEO信息
8. **保存文件**: 保存优化后的图片

### AI配置设置

点击右上角的"AI设置"按钮，配置以下信息：

- **API Provider**: 选择AI服务提供商
- **Base URL**: 设置API接口地址
- **API Key**: 输入你的API密钥
- **Model Name**: 指定使用的模型名称
- **Prompt Template**: 自定义生成模板

### 支持的图片格式

**输入格式**:
- JPEG (.jpg, .jpeg)
- PNG (.png)
- HEIC (.heic) - 苹果设备格式
- HEIF (.heif) - 高效图像格式
- WebP (.webp)
- BMP (.bmp)
- TIFF (.tiff, .tif)

**输出格式**:
- WebP (推荐，最优压缩)
- 可扩展支持其他格式

## 🔧 高级配置

### 环境变量配置

```bash
# AI服务配置
export OPENAI_API_KEY="your-openai-key"
export DEEPSEEK_API_KEY="your-deepseek-key"
export AI_BASE_URL="https://api.deepseek.com/v1"

# 输出配置
export OUTPUT_DIR="/path/to/output"
export DEFAULT_QUALITY="80"
export DEFAULT_WIDTH="1200"
```

### 配置文件位置

- **macOS**: `~/Library/Preferences/ImageFriend/`
- **Windows**: `%APPDATA%/ImageFriend/`
- **Linux**: `~/.config/ImageFriend/`

## 🏗️ 构建与部署

### 🚀 快速构建

**macOS 构建：**
```bash
# 构建 macOS 版本
python3 build_multi.py macos

# 输出：dist/ImageSEOFriend-macOS.app
```

**Windows 构建（在 Windows 环境）：**
```bash
# 构建 Windows 版本
python build_multi.py windows

# 输出：dist/ImageSEOFriend-Windows.exe
```

### 📋 构建脚本说明

| 脚本文件 | 用途 | 平台 |
|---------|------|------|
| `build_multi.py` | 多平台构建 | macOS/Windows |
| `build.py` | 基础构建 | macOS |
| `clean.py` | 清理临时文件 | 跨平台 |

### 📦 构建配置

| 配置文件 | 用途 | 特点 |
|---------|------|------|
| `imgSEOfriend.spec` | macOS 完整版 | .app 包，代码签名 |
| `imgSEOfriend_windows.spec` | Windows 完整版 | 版本信息，图标 |
| `build_simple.spec` | 简单版 | 最小依赖，快速构建 |

详细构建说明请参考：[BUILD_GUIDE.md](BUILD_GUIDE.md)

## 🏗️ 项目结构

```
imgSEOfriend/
├── 📱 应用程序
│   ├── app.py                     # 应用程序入口点
│   ├── main_window.py             # 主窗口
│   ├── before_after_widget.py      # 可拖拽对比的图片组件 ⭐
│   ├── config_manager.py          # 配置管理
│   ├── settings_dialog.py         # AI设置对话框
│   ├── worker.py                  # 图片处理工作线程
│   └── ai_service.py              # AI服务集成
├── 🎨 界面与资源
│   ├── dark_theme.qss             # 深色主题样式
│   └── assets/
│       └── app_icon.ico           # 应用程序图标
├── 🔧 构建与部署
│   ├── build.py                   # 基础构建脚本
│   ├── build_multi.py             # 多平台构建脚本
│   ├── clean.py                   # 清理脚本
│   ├── imgSEOfriend.spec          # macOS 构建配置
│   ├── imgSEOfriend_windows.spec  # Windows 构建配置
│   ├── build_simple.spec          # 简单构建配置
│   └── version_info.txt           # Windows 版本信息
├── 📚 文档
│   ├── README.md                  # 项目文档
│   ├── BUILD_GUIDE.md             # 构建指南
│   ├── RELEASE_NOTES.md           # 发布说明
│   └── md/                        # 文档目录
│       ├── PROJECT_SUMMARY.md     # 项目总结
│       ├── SECURITY_GUIDE.md      # 安全指南
│       ├── HEIC_HEIF_SUPPORT.md   # HEIC 格式支持
│       └── 需求.md                # 需求文档
└── ⚙️ 配置文件
    └── .gitignore                 # Git 忽略文件
```

## 🧪 测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_image_processing.py

# 生成覆盖率报告
pytest --cov=src tests/
```

## 🐛 故障排除

### 常见问题

**Q: HEIC图片无法打开？**
A: 确保已安装 `pillow-heif` 包：`pip install pillow-heif`

**Q: AI生成失败？**
A: 检查API密钥和网络连接，确认服务商配置正确

**Q: 图片处理很慢？**
A: 大文件处理需要时间，建议先调整尺寸再处理

**Q: 应用启动失败？**
A: 检查Python版本（需要3.8+）和依赖包安装

### 日志调试

启用详细日志：

```bash
export DEBUG=1
python app.py
```

## 🤝 贡献指南

我们欢迎所有形式的贡献！

### 贡献流程

1. **Fork** 项目
2. **创建** 功能分支 (`git checkout -b feature/amazing-feature`)
3. **提交** 更改 (`git commit -m 'Add amazing feature'`)
4. **推送** 到分支 (`git push origin feature/amazing-feature`)
5. **创建** Pull Request

### 代码规范

- 使用 `black` 进行代码格式化
- 遵循 PEP 8 编码规范
- 添加适当的类型提示
- 编写单元测试

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🧹 维护与清理

### 清理项目
```bash
# 清理构建产物和临时文件
python3 clean.py

# 手动清理
rm -rf build/ dist/ __pycache__/
find . -name "*.pyc" -delete
```

### 项目维护
- 定期运行 `clean.py` 清理临时文件
- 更新依赖包版本
- 检查AI服务API兼容性

## 🙏 致谢

- [PySide6](https://doc.qt.io/qtforpython/) - 强大的Python GUI框架
- [Pillow](https://pillow.readthedocs.io/) - 优秀的Python图像处理库
- [pillow-heif](https://pypi.org/project/pillow-heif/) - HEIC格式支持
- [PyInstaller](https://pyinstaller.org/) - Python应用打包工具

## 📞 联系我们

- **项目主页**: https://github.com/bobobov/imgSEOfriend
- **问题反馈**: https://github.com/bobobov/imgSEOfriend/issues
- **发布下载**: https://github.com/bobobov/imgSEOfriend/releases

---

<div align="center">

**[⬆ 回到顶部](#image-seo-optimizer---ai驱动的图片seo优化工具)**

如果这个项目对你有帮助，请考虑给我们一个 ⭐️

Made with ❤️ by [Image SEO Optimizer Team](https://github.com/bobobov/imgSEOfriend)

</div>