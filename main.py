import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PySide6.QtCore import Qt
from settings_dialog import SettingsDialog
from config_manager import ConfigManager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image SEO Optimizer - Test")
        self.setGeometry(100, 100, 400, 200)
        
        # 配置管理器
        self.config_manager = ConfigManager()
        
        # 中央窗口
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 布局
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # 标题
        title_label = QLabel("Image SEO Optimizer - Settings Test")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 20px;")
        layout.addWidget(title_label)
        
        # 当前配置信息
        self.config_info = QLabel()
        self.config_info.setAlignment(Qt.AlignLeft)
        self.config_info.setStyleSheet("margin: 10px; padding: 10px; background-color: #f0f0f0; border-radius: 5px;")
        layout.addWidget(self.config_info)
        
        # 打开设置按钮
        settings_button = QPushButton("Open Settings")
        settings_button.clicked.connect(self.open_settings)
        settings_button.setStyleSheet("margin: 10px; padding: 10px;")
        layout.addWidget(settings_button)
        
        # 刷新配置信息按钮
        refresh_button = QPushButton("Refresh Config Info")
        refresh_button.clicked.connect(self.refresh_config_info)
        refresh_button.setStyleSheet("margin: 10px; padding: 10px;")
        layout.addWidget(refresh_button)
        
        # 初始化显示配置信息
        self.refresh_config_info()
    
    def open_settings(self):
        """打开设置对话框"""
        dialog = SettingsDialog(self)
        dialog.settings_changed.connect(self.on_settings_changed)
        dialog.exec()
    
    def on_settings_changed(self):
        """设置变更时刷新显示"""
        self.refresh_config_info()

    
    def refresh_config_info(self):
        """刷新配置信息显示"""
        config = self.config_manager.get_all_config()
        
        info_text = "<b>Current Configuration:</b><br><br>"
        info_text += f"API Base URL: {config['api_base_url']}<br>"
        info_text += f"API Key: {'*' * len(config['api_key']) if config['api_key'] else 'Not set'}<br>"
        info_text += f"Model: {config['model_name']}<br>"
        info_text += f"System Prompt: {config['system_prompt']}<br>"
        info_text += f"Output Width: {config['output_width']}px<br>"
        info_text += f"Output Quality: {config['output_quality']}%<br>"
        info_text += f"Output Directory: {config['output_directory'] or 'Default'}"
        
        self.config_info.setText(info_text)


def main():
    app = QApplication(sys.argv)
    
    # 设置应用程序信息
    app.setApplicationName("Image SEO Optimizer")
    app.setOrganizationName("ImageSEO")
    
    # 创建主窗口
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()