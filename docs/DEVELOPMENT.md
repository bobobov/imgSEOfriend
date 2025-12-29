# 开发指南

## 项目结构

```
imgSEOfriend/
├── src/
│   └── imgseofriend/          # 主要源码包
│       ├── __init__.py
│       ├── app.py             # 应用入口
│       ├── main_window.py     # 主窗口
│       ├── settings_dialog.py # 设置对话框
│       ├── worker.py          # 图片处理工作线程
│       ├── config_manager.py  # 配置管理
│       ├── ai_service.py      # AI服务
│       └── before_after_widget.py # 对比组件
├── tests/                     # 测试文件
├── docs/                      # 文档
├── scripts/                   # 构建脚本
├── assets/                    # 资源文件
├── screenshots/               # 截图
├── pyproject.toml            # 项目配置
├── requirements.txt          # 依赖列表
├── main.py                   # 主启动文件
└── README.md                # 项目说明
```

## 开发环境设置

### 1. 克隆项目
```bash
git clone <repository-url>
cd imgSEOfriend
```

### 2. 创建虚拟环境
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate     # Windows
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
# 开发环境额外依赖
pip install -e .[dev]
```

## 运行应用

### 开发模式
```bash
python main.py
```

### 安装后运行
```bash
pip install -e .
imgseofriend
```

## 测试

```bash
# 运行所有测试
python -m pytest tests/

# 运行特定测试
python -m pytest tests/test_basic.py

# 代码覆盖率
python -m pytest --cov=src tests/
```

## 代码规范

```bash
# 代码格式化
black src/ tests/

# 代码检查
flake8 src/ tests/

# 类型检查
mypy src/
```

## 构建

```bash
# 清理
python scripts/clean.py

# 构建可执行文件
python scripts/build.py

# 多平台构建
python scripts/build_multi.py
```

## 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启 Pull Request