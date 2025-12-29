from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
                               QLineEdit, QPushButton, QTextEdit, QMessageBox,
                               QGroupBox, QLabel, QSpinBox, QSlider)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from config_manager import ConfigManager
from ai_service import AIService


class SettingsDialog(QDialog):
    """设置对话框"""
    
    settings_changed = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config_manager = ConfigManager()
        self.init_ui()
        self.load_settings()
    
    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle("AI Settings")
        self.setModal(True)
        self.resize(700, 600)  # 增加宽度以适应更宽的输入框
        
        # 主布局
        layout = QVBoxLayout()
        
        # API 设置组
        api_group = QGroupBox("API Configuration")
        api_layout = QFormLayout()
        
        # API Base URL
        self.api_base_url_input = QLineEdit()
        self.api_base_url_input.setPlaceholderText("https://api.deepseek.com")
        self.api_base_url_input.setMinimumWidth(400)  # 加倍宽度
        api_layout.addRow("API Base URL:", self.api_base_url_input)
        
        # API Key
        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.Password)
        self.api_key_input.setPlaceholderText("Enter your API key")
        self.api_key_input.setMinimumWidth(400)  # 加倍宽度
        api_layout.addRow("API Key:", self.api_key_input)
        
        # Model Name
        self.model_name_input = QLineEdit()
        self.model_name_input.setPlaceholderText("deepseek-chat")
        self.model_name_input.setMinimumWidth(400)  # 加倍宽度
        api_layout.addRow("Model Name:", self.model_name_input)
        
        api_group.setLayout(api_layout)
        layout.addWidget(api_group)
        
        # Prompt 设置组
        prompt_group = QGroupBox("Prompt Configuration")
        prompt_layout = QFormLayout()
        
        # System Prompt
        self.system_prompt_input = QTextEdit()
        self.system_prompt_input.setMaximumHeight(300)  # 增加约10行高度 (100 + 200)
        self.system_prompt_input.setMinimumWidth(400)  # 加倍宽度
        self.system_prompt_input.setPlaceholderText("You are an SEO assistant.")
        prompt_layout.addRow("System Prompt:", self.system_prompt_input)
        
        prompt_group.setLayout(prompt_layout)
        layout.addWidget(prompt_group)
        
        # Output 设置组
        output_group = QGroupBox("Output Configuration")
        output_layout = QFormLayout()
        
        
        
        # Output Quality
        quality_layout = QHBoxLayout()
        
        self.output_quality_slider = QSlider(Qt.Horizontal)
        self.output_quality_slider.setMinimum(10)
        self.output_quality_slider.setMaximum(100)
        self.output_quality_slider.setMinimumWidth(300)  # 滑块宽度
        self.output_quality_slider.setValue(80)  # 默认值
        
        self.output_quality_label = QLabel("80 %")
        self.output_quality_label.setMinimumWidth(50)  # 标签宽度
        self.output_quality_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        # 连接滑块值变化信号
        self.output_quality_slider.valueChanged.connect(
            lambda value: self.output_quality_label.setText(f"{value} %")
        )
        
        quality_layout.addWidget(self.output_quality_slider)
        quality_layout.addWidget(self.output_quality_label)
        
        output_layout.addRow("WebP Quality:", quality_layout)
        
        output_group.setLayout(output_layout)
        layout.addWidget(output_group)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        
        # Test Connection 按钮
        self.test_button = QPushButton("Test Connection")
        self.test_button.clicked.connect(self.test_connection)
        button_layout.addWidget(self.test_button)
        
        button_layout.addStretch()
        
        # OK 和 Cancel 按钮
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept_settings)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def load_settings(self):
        """加载设置到界面"""
        self.api_base_url_input.setText(self.config_manager.get_api_base_url())
        self.api_key_input.setText(self.config_manager.get_api_key())
        self.model_name_input.setText(self.config_manager.get_model_name())
        self.system_prompt_input.setPlainText(self.config_manager.get_system_prompt())
        
        # 加载WebP Quality设置
        quality_value = self.config_manager.get_output_quality()
        self.output_quality_slider.setValue(quality_value)
        self.output_quality_label.setText(f"{quality_value} %")
    
    def save_settings(self):
        """保存界面设置"""
        self.config_manager.save_api_base_url(self.api_base_url_input.text().strip())
        self.config_manager.save_api_key(self.api_key_input.text().strip())
        self.config_manager.save_model_name(self.model_name_input.text().strip())
        self.config_manager.save_system_prompt(self.system_prompt_input.toPlainText().strip())
        self.config_manager.save_output_quality(self.output_quality_slider.value())
    
    def test_connection(self):
        """测试连接"""
        api_base_url = self.api_base_url_input.text().strip()
        api_key = self.api_key_input.text().strip()
        model_name = self.model_name_input.text().strip()
        
        if not api_base_url:
            QMessageBox.warning(self, "Warning", "API Base URL is required for testing!")
            return
        
        if not api_key:
            QMessageBox.warning(self, "Warning", "API Key is required for testing!")
            return
        
        if not model_name:
            QMessageBox.warning(self, "Warning", "Model Name is required for testing!")
            return
        
        # 保存当前配置到临时变量
        temp_config = ConfigManager()
        temp_config.save_api_base_url(api_base_url)
        temp_config.save_api_key(api_key)
        temp_config.save_model_name(model_name)
        temp_config.save_system_prompt(self.system_prompt_input.toPlainText().strip())
        
        # 测试连接
        ai_service = AIService(temp_config)
        result = ai_service.test_connection()
        
        # 显示测试结果
        msg = QMessageBox(self)
        msg.setWindowTitle("Connection Test")
        
        if result["success"]:
            msg.setText("Connection successful!\n\n"
                       f"URL: {api_base_url}\n"
                       f"Model: {model_name}\n"
                       f"API Key: {'Provided' if api_key else 'Not provided'}")
            msg.setIcon(QMessageBox.Information)
        else:
            msg.setText(f"Connection failed!\n\n"
                       f"Error: {result['message']}\n\n"
                       f"URL: {api_base_url}\n"
                       f"Model: {model_name}\n"
                       f"API Key: {'Provided' if api_key else 'Not provided'}")
            msg.setIcon(QMessageBox.Critical)
        
        msg.exec()
    
    def accept_settings(self):
        """接受设置并保存"""
        if not self.api_base_url_input.text().strip():
            QMessageBox.warning(self, "Warning", "API Base URL is required!")
            return
        
        if not self.api_key_input.text().strip():
            QMessageBox.warning(self, "Warning", "API Key is required!")
            return
        
        if not self.model_name_input.text().strip():
            QMessageBox.warning(self, "Warning", "Model Name is required!")
            return
        
        self.save_settings()
        self.settings_changed.emit()
        self.accept()
    
    def get_current_config(self):
        """获取当前配置"""
        return {
            "api_base_url": self.api_base_url_input.text().strip(),
            "api_key": self.api_key_input.text().strip(),
            "model_name": self.model_name_input.text().strip(),
            "system_prompt": self.system_prompt_input.toPlainText().strip(),
            "output_quality": self.output_quality_slider.value()
        }