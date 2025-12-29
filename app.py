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