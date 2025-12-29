#!/usr/bin/env python3
"""
Image SEO Optimizer - Main Application
主应用程序入口
"""

import sys
from PySide6.QtWidgets import QApplication
from main_window import MainWindow


def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 加载暗色主题样式
    try:
        with open("dark_theme.qss", "r", encoding="utf-8") as style_file:
            app.setStyleSheet(style_file.read())
    except FileNotFoundError:
        pass  # 样式文件缺失，使用默认样式
    except Exception:
        pass  # 样式加载失败，使用默认样式
    
    # 设置应用程序信息
    app.setApplicationName("Image SEO Optimizer")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("ImageSEO")
    app.setOrganizationDomain("imageseo.local")
    
    # 创建并显示主窗口
    window = MainWindow()
    window.show()
    
    # 运行应用程序
    sys.exit(app.exec())


if __name__ == "__main__":
    main()