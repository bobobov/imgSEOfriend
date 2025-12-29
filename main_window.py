#!/usr/bin/env python3
"""
Image SEO Optimizer - Main Window
主界面窗口实现
"""

import os
from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit,
    QRadioButton, QButtonGroup, QFrame, QSizePolicy,
    QMessageBox, QFileDialog, QProgressBar, QApplication
)
from PySide6.QtCore import Qt, QMimeData, QUrl, Signal, QTimer
from PySide6.QtGui import QPixmap, QDragEnterEvent, QDropEvent, QFont, QFocusEvent

from config_manager import ConfigManager


class CustomWidthLineEdit(QLineEdit):
    """自定义宽度输入框，点击时自动选中Custom选项"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = None
    
    def set_parent_window(self, parent_window):
        """设置父窗口引用"""
        self.parent_window = parent_window
    
    def mousePressEvent(self, event):
        """处理鼠标点击事件"""
        if self.parent_window and not self.parent_window.width_custom.isChecked():
            self.parent_window.width_custom.setChecked(True)
            self.parent_window.custom_width_input.setEnabled(True)
        super().mousePressEvent(event)
from settings_dialog import SettingsDialog
from worker import ImageWorker, ImageResult
from before_after_widget import BeforeAfterWidget


class ImageDropLabel(QLabel):
    """支持拖拽的图片显示标签"""
    
    image_loaded = Signal(str)  # 定义信号，传递图片路径
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setMinimumSize(400, 300)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("""
            QLabel {
                border: 3px dashed #4a4a4a;
                border-radius: 12px;
                background-color: #1e1e1e;
                color: #888888;
                font-size: 16px;
                font-weight: 500;
            }
            QLabel:hover {
                border: 3px dashed #6200ee;
                background-color: #252525;
                color: #7d1fe8;
            }
        """)
        self.setText("Drag Image Here")
        self.current_image_path = None
        
    def dragEnterEvent(self, event: QDragEnterEvent):
        """拖拽进入事件"""
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls:
                file_path = urls[0].toLocalFile()
                if file_path and self._is_image_file(file_path):
                    event.acceptProposedAction()
                    self.setStyleSheet("""
                        QLabel {
                            border: 3px dashed #6200ee;
                            border-radius: 12px;
                            background-color: #252525;
                            color: #7d1fe8;
                            font-size: 16px;
                            font-weight: 500;
                        }
                    """)
                else:
                    event.ignore()
        else:
            event.ignore()
    
    def dragLeaveEvent(self, event):
        """拖拽离开事件"""
        self.setStyleSheet("""
            QLabel {
                border: 3px dashed #4a4a4a;
                border-radius: 12px;
                background-color: #1e1e1e;
                color: #888888;
                font-size: 16px;
                font-weight: 500;
            }
            QLabel:hover {
                border: 3px dashed #6200ee;
                background-color: #252525;
                color: #7d1fe8;
            }
        """)
    
    def dropEvent(self, event: QDropEvent):
        """拖拽放下事件"""
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            if file_path and self._is_image_file(file_path):
                self.load_image(file_path)
                
        # 恢复默认样式
        self.setStyleSheet("""
            QLabel {
                border: 3px dashed #4a4a4a;
                border-radius: 12px;
                background-color: #1e1e1e;
                color: #888888;
                font-size: 16px;
                font-weight: 500;
            }
            QLabel:hover {
                border: 3px dashed #6200ee;
                background-color: #252525;
                color: #7d1fe8;
            }
        """)
    
    def _is_image_file(self, file_path: str) -> bool:
        """检查是否为图片文件"""
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.heic', '.heif'}
        return Path(file_path).suffix.lower() in image_extensions
    
    def load_image(self, image_path: str):
        """加载图片到 BeforeAfterWidget"""
        self.current_image_path = image_path
        
        # 首先设置 Before 图片（原图）
        success = self.image_display.set_before_image(image_path)
        
        if success:
            # 更新提示文本
            self.drop_hint.setText(f"Original Image Loaded: {Path(image_path).name}")
            self.drop_hint.setStyleSheet("""
                QLabel {
                    padding: 15px;
                    background-color: #e8f5e8;
                    border-radius: 8px;
                    font-size: 14px;
                    color: #2e7d32;
                    margin-bottom: 10px;
                }
            """)
            
            # 从文件名提取关键词作为默认值
            filename = Path(image_path).stem
            keyword = filename.replace('_', ' ').replace('-', ' ')
            self.keyword_input.reset()  # 重置输入框状态
            self.keyword_input.set_default_keyword(keyword)
            
            # 启用处理按钮
            self.process_image_only_button.setEnabled(True)
            # AI按钮需要用户输入关键词，通过on_keyword_changed方法控制
            self.process_with_ai_button.setEnabled(self.keyword_input.has_user_input())
        else:
            self.drop_hint.setText("Failed to load image")
            self.drop_hint.setStyleSheet("""
                QLabel {
                    padding: 15px;
                    background-color: #ffebee;
                    border-radius: 8px;
                    font-size: 14px;
                    color: #c62828;
                    margin-bottom: 10px;
                }
            """)
            QMessageBox.warning(self, "Warning", "Failed to load the image!")
    
    def reset(self):
        """重置标签"""
        self.current_image_path = None
        self.clear()
        self.setText("Drag Image Here")
        self.setStyleSheet("""
            QLabel {
                border: 3px dashed #ccc;
                border-radius: 10px;
                background-color: #f9f9f9;
                color: #666;
                font-size: 18px;
            }
            QLabel:hover {
                border-color: #0078d4;
                background-color: #f0f8ff;
            }
        """)


class ClearOnFocusLineEdit(QLineEdit):
    """智能关键词输入框：用户输入优先，空值使用文件名"""
    
    # 定义信号：输入内容变化时发出
    text_changed = Signal(str)  # 传递当前文本内容
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._user_modified = False  # 标记用户是否修改过内容
        self._default_keyword = ""   # 默认关键词（文件名）
        
        # 连接文本变化信号
        self.textChanged.connect(self._on_text_changed)
        
    def focusInEvent(self, event: QFocusEvent):
        """获得焦点时选中全部内容，方便用户修改"""
        self.selectAll()
        super().focusInEvent(event)
        
    def set_default_keyword(self, keyword: str):
        """设置默认关键词（文件名）但不显示"""
        self._default_keyword = keyword
        # 不自动显示文件名，保持输入框显示提示文本
            
    def _on_text_changed(self, text: str):
        """文本变化时发出信号"""
        self.text_changed.emit(text)
        
    def get_keyword(self) -> str:
        """获取关键词：只返回用户输入的内容，不再使用默认关键词"""
        user_text = self.text().strip()
        return user_text  # 只返回用户输入的内容
        
    def has_user_input(self) -> bool:
        """检查用户是否输入了内容"""
        return bool(self.text().strip())
        
    def keyPressEvent(self, event):
        """键盘输入事件，标记用户已修改内容"""
        if not self._user_modified and event.text():
            self._user_modified = True
        super().keyPressEvent(event)
        
    def reset(self):
        """重置状态，用于新图片"""
        self._user_modified = False
        self._default_keyword = ""
        self.clear()


class ClickableLineEdit(QLineEdit):
    """可点击复制的文本框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.copied_label = None
        self.setStyleSheet("""
            QLineEdit {
                background-color: #2a2a2a;
                border: 2px solid #3a3a3a;
                border-radius: 8px;
                padding: 12px 16px;
                font-size: 14px;
                color: #ffffff;
                selection-background-color: #404040;
            }
            QLineEdit:hover {
                border: 2px solid #6200ee;
                background-color: #333333;
            }
        """)
        
    def mousePressEvent(self, event):
        """点击时复制内容到剪贴板"""
        if self.text():
            clipboard = QApplication.clipboard()
            clipboard.setText(self.text())
            # 显示复制成功的提示
            self.setStyleSheet("""
                QLineEdit {
                    background-color: #1e5a2e;
                    border: 2px solid #28a745;
                    border-radius: 8px;
                    padding: 12px 16px;
                    font-size: 14px;
                    color: #ffffff;
                    selection-background-color: #404040;
                }
            """)
            self.show_copied_notification()
            # 1.5秒后恢复原样式
            QTimer.singleShot(1500, self.restore_style)
        super().mousePressEvent(event)
    
    def show_copied_notification(self):
        """显示已复制提示"""
        if self.copied_label:
            self.copied_label.deleteLater()
        
        self.copied_label = QLabel("已复制", self)
        self.copied_label.setStyleSheet("""
            QLabel {
                background-color: #28a745;
                color: white;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 12px;
                font-weight: bold;
            }
        """)
        
        # 获取全局父窗口来显示提示
        parent = self.parent()
        while parent and parent.parent():
            parent = parent.parent()
        
        if parent:
            # 在主窗口中显示提示
            self.copied_label.setParent(parent)
            # 计算相对于主窗口的位置
            global_pos = self.mapTo(parent, QPoint(0, 0))
            label_width = self.copied_label.sizeHint().width()
            label_height = self.copied_label.sizeHint().height()
            x = global_pos.x() + (self.width() - label_width) // 2
            y = global_pos.y() - label_height - 5
            self.copied_label.move(x, y)
            self.copied_label.resize(label_width, label_height)
            self.copied_label.show()
        else:
            # 备用方案：在文本框上方显示
            self.copied_label.move(10, -25)
            self.copied_label.resize(60, 20)
            self.copied_label.show()
        
        # 1.5秒后隐藏提示
        QTimer.singleShot(1500, self.hide_copied_notification)
    
    def hide_copied_notification(self):
        """隐藏已复制提示"""
        if self.copied_label:
            self.copied_label.hide()
            self.copied_label.deleteLater()
            self.copied_label = None
    
    def show_copied_notification(self):
        """显示已复制提示"""
        if self.copied_label:
            self.copied_label.deleteLater()
        
        self.copied_label = QLabel("已复制", self)
        self.copied_label.setStyleSheet("""
            QLabel {
                background-color: #28a745;
                color: white;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 12px;
                font-weight: bold;
            }
        """)
        
        # 获取全局父窗口来显示提示
        parent = self.parent()
        while parent and parent.parent():
            parent = parent.parent()
        
        if parent:
            # 在主窗口中显示提示
            self.copied_label.setParent(parent)
            # 计算相对于主窗口的位置
            global_pos = self.mapTo(parent, QPoint(0, 0))
            label_width = self.copied_label.sizeHint().width()
            label_height = self.copied_label.sizeHint().height()
            x = global_pos.x() + (self.width() - label_width) // 2
            y = global_pos.y() - label_height - 5
            self.copied_label.move(x, y)
            self.copied_label.resize(label_width, label_height)
            self.copied_label.show()
        else:
            # 备用方案：在文本框上方显示
            self.copied_label.move(10, -25)
            self.copied_label.resize(60, 20)
            self.copied_label.show()
        
        # 1.5秒后隐藏提示
        QTimer.singleShot(1500, self.hide_copied_notification)
    
    def hide_copied_notification(self):
        """隐藏已复制提示"""
        if self.copied_label:
            self.copied_label.hide()
            self.copied_label.deleteLater()
            self.copied_label = None
    
    def restore_style(self):
        """恢复原始样式"""
        self.setStyleSheet("""
            QLineEdit {
                background-color: #2a2a2a;
                border: 2px solid #3a3a3a;
                border-radius: 8px;
                padding: 12px 16px;
                font-size: 14px;
                color: #ffffff;
                selection-background-color: #404040;
            }
            QLineEdit:hover {
                border: 2px solid #6200ee;
                background-color: #333333;
            }
        """)


class ClickableTextEdit(QTextEdit):
    """可点击复制的多行文本框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setFixedHeight(80)  # 设置高度为约3行
        self.copied_label = None
        self.setStyleSheet("""
            QTextEdit {
                background-color: #2a2a2a;
                border: 2px solid #3a3a3a;
                border-radius: 8px;
                padding: 12px 16px;
                font-size: 14px;
                color: #ffffff;
                selection-background-color: #404040;
                line-height: 1.4;
            }
            QTextEdit:hover {
                border: 2px solid #6200ee;
                background-color: #333333;
            }
        """)
        
    def mousePressEvent(self, event):
        """点击时复制内容到剪贴板"""
        if self.toPlainText():
            clipboard = QApplication.clipboard()
            clipboard.setText(self.toPlainText())
            # 显示复制成功的提示
            self.setStyleSheet("""
                QTextEdit {
                    background-color: #1e5a2e;
                    border: 2px solid #28a745;
                    border-radius: 8px;
                    padding: 12px 16px;
                    font-size: 14px;
                    color: #ffffff;
                    selection-background-color: #404040;
                    line-height: 1.4;
                }
            """)
            self.show_copied_notification()
            # 1.5秒后恢复原样式
            QTimer.singleShot(1500, self.restore_style)
        super().mousePressEvent(event)
    
    def show_copied_notification(self):
        """显示已复制提示"""
        if self.copied_label:
            self.copied_label.deleteLater()
        
        self.copied_label = QLabel("已复制", self)
        self.copied_label.setStyleSheet("""
            QLabel {
                background-color: #28a745;
                color: white;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 12px;
                font-weight: bold;
            }
        """)
        
        # 计算位置（在文本框上方居中）
        label_rect = self.copied_label.geometry()
        label_rect.setWidth(self.copied_label.sizeHint().width())
        label_rect.setHeight(self.copied_label.sizeHint().height())
        x = (self.width() - label_rect.width()) // 2
        y = -label_rect.height() - 5
        self.copied_label.setGeometry(x, y, label_rect.width(), label_rect.height())
        self.copied_label.show()
        
        # 1秒后隐藏提示
        QTimer.singleShot(1000, self.hide_copied_notification)
    
    def hide_copied_notification(self):
        """隐藏已复制提示"""
        if self.copied_label:
            self.copied_label.hide()
            self.copied_label.deleteLater()
            self.copied_label = None
    
    def restore_style(self):
        """恢复原始样式"""
        self.setStyleSheet("""
            QTextEdit {
                background-color: #2a2a2a;
                border: 2px solid #3a3a3a;
                border-radius: 8px;
                padding: 12px 16px;
                font-size: 14px;
                color: #ffffff;
                selection-background-color: #404040;
                line-height: 1.4;
            }
            QTextEdit:hover {
                border: 2px solid #6200ee;
                background-color: #333333;
            }
        """)
    

class MainWindow(QMainWindow):
    """主窗口"""
    
    def __init__(self):
        super().__init__()
        self.config_manager = ConfigManager()
        self.current_worker = None
        self.current_image_result = None
        self.current_ai_result = None
        
        # 设置拖拽支持
        self.setAcceptDrops(True)
        
        self.init_ui()
        
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("Image SEO Optimizer")
        self.setMinimumSize(1000, 700)
        
        # 创建中央窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局：左右分栏
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # 左侧：预览区域
        self.preview_area = self.create_preview_area()
        main_layout.addWidget(self.preview_area, stretch=2)
        
        # 右侧：控制面板
        self.control_panel = self.create_control_panel()
        main_layout.addWidget(self.control_panel, stretch=1)
        
        # 添加分隔线
        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setStyleSheet("color: #ddd;")
        main_layout.insertWidget(1, separator)
        

        
    def create_preview_area(self) -> QWidget:
        """创建左侧预览区域"""
        preview_widget = QWidget()
        preview_widget.setObjectName("previewPanel")
        preview_layout = QVBoxLayout(preview_widget)
        preview_layout.setContentsMargins(0, 0, 0, 0)
        
        # 添加图片加载提示标签（优化高度，减少padding）
        self.drop_hint = QLabel("Drag Image Here to Start")
        self.drop_hint.setObjectName("hintLabel")
        self.drop_hint.setAlignment(Qt.AlignCenter)
        self.drop_hint.setStyleSheet("""
            QLabel {
                padding: 10px 16px;
                background-color: #f0f0f0;
                border-radius: 8px;
                font-size: 14px;
                color: #666;
                margin: 5px 0;
            }
        """)
        preview_layout.addWidget(self.drop_hint)
        
        # 创建 Before/After 对比组件
        self.image_display = BeforeAfterWidget()
        preview_layout.addWidget(self.image_display, stretch=1)
        
        # 进度条（初始隐藏）
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        preview_layout.addWidget(self.progress_bar)
        
        return preview_widget
    
    def create_control_panel(self) -> QWidget:
        """创建右侧控制面板"""
        control_widget = QWidget()
        control_widget.setObjectName("controlPanel")
        control_layout = QVBoxLayout(control_widget)
        control_layout.setContentsMargins(0, 0, 0, 0)
        
        # 顶部：设置按钮居右
        top_layout = QHBoxLayout()
        
        # 中间弹性空间
        top_layout.addStretch()
        
        # 设置按钮
        self.settings_button = QPushButton("Settings ⚙️")
        self.settings_button.setObjectName("settingsButton")
        self.settings_button.clicked.connect(self.open_settings)
        self.settings_button.setMaximumHeight(40)
        top_layout.addWidget(self.settings_button)
        
        control_layout.addLayout(top_layout)
        
        # 分隔线
        control_layout.addWidget(self.create_separator())
        
        # 表单区域
        form_layout = self.create_form_section()
        control_layout.addLayout(form_layout)
        
        # 分隔线
        control_layout.addWidget(self.create_separator())
        
        # 结果区域（初始隐藏）
        self.result_section = self.create_result_section()
        self.result_section.setVisible(False)
        control_layout.addWidget(self.result_section)
        
        # 底部：打开输出文件夹按钮
        control_layout.addStretch()
        self.open_output_folder_button = QPushButton("打开输出文件夹 📁")
        self.open_output_folder_button.setObjectName("openFolderButton")
        self.open_output_folder_button.clicked.connect(self.open_output_folder)
        control_layout.addWidget(self.open_output_folder_button)
        
        return control_widget
    
    def create_separator(self) -> QFrame:
        """创建分隔线"""
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("color: #ddd; margin: 10px 0;")
        return separator
    
    def create_form_section(self) -> QVBoxLayout:
        """创建表单区域"""
        form_layout = QVBoxLayout()
        
        # Keyword 输入框
        keyword_container = QHBoxLayout()
        keyword_container.setContentsMargins(0, 0, 0, 0)
        
        # Keyword 标签
        keyword_label = QLabel("Keyword:")
        keyword_label.setStyleSheet("font-size: 13px; color: #666; font-weight: 500;")
        keyword_label.setMinimumWidth(70)  # 固定宽度确保对齐
        keyword_container.addWidget(keyword_label)
        
        self.keyword_input = ClearOnFocusLineEdit()
        self.keyword_input.setPlaceholderText("请输入关键词描述")
        keyword_container.addWidget(self.keyword_input)
        
        form_layout.addLayout(keyword_container)
        
        # 连接关键词输入框信号
        self.keyword_input.text_changed.connect(self.on_keyword_changed)
        
        # Width 选择
        form_layout.addWidget(QLabel("Target Width:"))
        width_layout = QVBoxLayout()
        
        # 预设宽度选项行
        preset_width_layout = QHBoxLayout()
        
        self.width_button_group = QButtonGroup()
        
        self.width_500 = QRadioButton("500px")
        self.width_500.setChecked(True)
        self.width_button_group.addButton(self.width_500, 500)
        preset_width_layout.addWidget(self.width_500)
        
        self.width_750 = QRadioButton("750px")
        self.width_button_group.addButton(self.width_750, 750)
        preset_width_layout.addWidget(self.width_750)
        
        self.width_900 = QRadioButton("900px")
        self.width_button_group.addButton(self.width_900, 900)
        preset_width_layout.addWidget(self.width_900)
        
        self.width_1200 = QRadioButton("1200px")
        self.width_button_group.addButton(self.width_1200, 1200)
        preset_width_layout.addWidget(self.width_1200)
        
        width_layout.addLayout(preset_width_layout)
        
        # 自定义宽度行
        custom_width_layout = QHBoxLayout()
        self.width_custom = QRadioButton("Custom:")
        self.width_button_group.addButton(self.width_custom, -999)  # -999 表示自定义
        custom_width_layout.addWidget(self.width_custom)
        
        self.custom_width_input = CustomWidthLineEdit()
        self.custom_width_input.setPlaceholderText("Enter width")
        self.custom_width_input.setMaximumWidth(100)
        self.custom_width_input.setEnabled(False)  # 默认禁用
        self.custom_width_input.set_parent_window(self)  # 设置父窗口引用
        custom_width_layout.addWidget(self.custom_width_input)
        
        custom_width_layout.addWidget(QLabel("px"))
        custom_width_layout.addStretch()
        
        width_layout.addLayout(custom_width_layout)
        
        form_layout.addLayout(width_layout)
        
        # 连接信号
        self.width_custom.toggled.connect(self.on_custom_width_toggled)
        
        # Process 按钮
        button_layout = QHBoxLayout()
        
        self.process_image_only_button = QPushButton("Process Image Only")
        self.process_image_only_button.setObjectName("processImageButton")
        self.process_image_only_button.clicked.connect(self.process_image_only)
        self.process_image_only_button.setEnabled(False)
        button_layout.addWidget(self.process_image_only_button)
        
        self.process_with_ai_button = QPushButton("Process Image + Generate AI 🚀")
        self.process_with_ai_button.setObjectName("processAIButton")
        self.process_with_ai_button.clicked.connect(self.process_with_ai)
        self.process_with_ai_button.setEnabled(False)
        button_layout.addWidget(self.process_with_ai_button)
        
        form_layout.addLayout(button_layout)
        
        return form_layout
    
    def create_result_section(self) -> QWidget:
        """创建结果区域"""
        result_widget = QWidget()
        result_layout = QVBoxLayout(result_widget)
        
        # 标题
        result_layout.addWidget(QLabel("Generated SEO Data:"))
        
        # Title 输入框
        result_layout.addWidget(QLabel("Title (Click to copy):"))
        self.title_input = ClickableLineEdit()
        result_layout.addWidget(self.title_input)
        
        # Alt Text 输入框
        result_layout.addWidget(QLabel("Alt Text (Click to copy):"))
        self.alt_text_input = ClickableTextEdit()
        result_layout.addWidget(self.alt_text_input)
        
        # Regenerate AI 按钮
        self.regenerate_button = QPushButton("Regenerate AI 🔄")
        self.regenerate_button.setObjectName("regenerateButton")
        self.regenerate_button.clicked.connect(self.regenerate_ai)
        result_layout.addWidget(self.regenerate_button)
        
        return result_widget
    
    def open_settings(self):
        """打开设置对话框"""
        dialog = SettingsDialog(self)
        if dialog.exec() == SettingsDialog.Accepted:
            # 设置已保存，可以显示确认消息
            QMessageBox.information(self, "Settings", "Settings saved successfully!")
    
    def process_image_only(self):
        """仅处理图片，不生成 AI 内容"""
        if not self.image_display.current_image_path:
            QMessageBox.warning(self, "Warning", "Please drag and drop an image first!")
            return
        
        keyword = self.keyword_input.get_keyword()
        # 允许无关键词执行，如果无关键词则使用原文件名
        if not keyword:
            keyword = ""  # 使用空字符串表示使用原文件名
        
        # 获取选中的宽度
        target_width = self.get_target_width()
        if target_width is None:
            return  # 自定义宽度无效
        
        # 禁用控件，显示进度
        self.set_processing_state(True)
        
        # 创建工作线程
        self.current_worker = ImageWorker(
            image_path=self.image_display.current_image_path,
            keyword=keyword,
            target_width=target_width,
            process_mode="image_only"
        )
        
        # 连接信号
        self.current_worker.finished.connect(self.on_processing_finished)
        self.current_worker.error.connect(self.on_processing_error)
        self.current_worker.progress.connect(self.on_progress_updated)
        
        # 启动线程
        self.current_worker.start()
    
    def process_with_ai(self):
        """处理图片并生成 AI 内容"""
        if not self.image_display.current_image_path:
            QMessageBox.warning(self, "Warning", "Please drag and drop an image first!")
            return
        
        keyword = self.keyword_input.get_keyword()
        if not keyword:
            QMessageBox.warning(self, "Warning", "请输入关键词描述！AI处理需要关键词才能生成相关的SEO内容。")
            return
        
        # 获取选中的宽度
        target_width = self.get_target_width()
        if target_width is None:
            return  # 自定义宽度无效
        
        # 禁用控件，显示进度
        self.set_processing_state(True)
        
        # 创建工作线程
        self.current_worker = ImageWorker(
            image_path=self.image_display.current_image_path,
            keyword=keyword,
            target_width=target_width,
            process_mode="with_ai"
        )
        
        # 连接信号
        self.current_worker.finished.connect(self.on_processing_finished)
        self.current_worker.error.connect(self.on_processing_error)
        self.current_worker.progress.connect(self.on_progress_updated)
        
        # 启动线程
        self.current_worker.start()
    
    def process_image(self):
        """处理图片（保持向后兼容）"""
        self.process_with_ai()
    
    
    
    def on_progress_updated(self, message: str):
        """更新进度消息"""
        self.progress_bar.setFormat(message)
    
    def on_processing_finished(self, image_result: ImageResult, ai_result: dict):
        """处理完成"""
        self.current_image_result = image_result
        self.current_ai_result = ai_result
        
        # 设置 After 图片（处理后的图片）
        success = self.image_display.set_after_image(image_result.processed_path)
        
        if success:
            # 更新提示文本
            self.drop_hint.setText(f"Comparison Ready: {Path(self.current_image_path).name}")
            self.drop_hint.setStyleSheet("""
                QLabel {
                    padding: 15px;
                    background-color: #e3f2fd;
                    border-radius: 8px;
                    font-size: 14px;
                    color: #1565c0;
                    margin-bottom: 10px;
                }
            """)
        
        # 如果有 AI 结果，填入 AI 生成的数据
        if ai_result:
            self.title_input.setText(ai_result.get('title', ''))
            self.alt_text_input.setPlainText(ai_result.get('alt_text', ''))
        else:
            # 仅图片处理模式，清空或保留现有数据
            pass
        
        # 显示结果区域
        self.result_section.setVisible(True)
        
        # 恢复控件状态
        self.set_processing_state(False)
        
        self.show_success_notification("Image processed successfully!")
    
    def show_success_notification(self, message: str):
        """显示成功通知，1秒后自动消失"""
        # 创建通知标签
        notification = QLabel(message, self)
        notification.setStyleSheet("""
            QLabel {
                background-color: #28a745;
                color: white;
                padding: 12px 20px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
            }
        """)
        
        # 计算位置（在窗口中央上方）
        notification.adjustSize()
        x = (self.width() - notification.width()) // 2
        y = 100  # 距离窗口顶部100像素
        
        notification.move(x, y)
        notification.show()
        
        # 1秒后自动删除
        QTimer.singleShot(1000, lambda: notification.deleteLater())
    
    def on_processing_error(self, error_message: str):
        """处理错误"""
        QMessageBox.critical(self, "Error", f"Processing failed: {error_message}")
        self.set_processing_state(False)
    
    def set_processing_state(self, processing: bool):
        """设置处理状态"""
        self.process_image_only_button.setEnabled(not processing)
        self.process_with_ai_button.setEnabled(not processing)
        self.settings_button.setEnabled(not processing)
        self.keyword_input.setEnabled(not processing)
        
        # 处理宽度控件状态
        self.width_500.setEnabled(not processing)
        self.width_750.setEnabled(not processing)
        self.width_900.setEnabled(not processing)
        self.width_1200.setEnabled(not processing)
        self.width_custom.setEnabled(not processing)
        
        # 自定义输入框只有在非处理状态且选择了自定义时才启用
        if processing:
            self.custom_width_input.setEnabled(False)
        else:
            self.custom_width_input.setEnabled(self.width_custom.isChecked())
        
        self.progress_bar.setVisible(processing)
        
        if processing:
            self.progress_bar.setRange(0, 0)  # 无限进度条
        else:
            self.progress_bar.setRange(0, 100)  # 恢复正常范围
            self.progress_bar.setValue(0)
    
    def regenerate_ai(self):
        """重新生成AI数据"""
        if not self.current_image_result or not self.current_ai_result:
            return
        
        keyword = self.keyword_input.get_keyword()
        if not keyword:
            return
        
        # 获取原始图片路径和选中的宽度
        target_width = self.get_target_width()
        if target_width is None:
            return  # 自定义宽度无效
        
        # 禁用控件
        self.set_processing_state(True)
        
        # 创建工作线程（只重新生成AI数据）
        self.current_worker = ImageWorker(
            image_path=self.image_display.current_image_path,
            keyword=keyword,
            target_width=target_width,
            process_mode="with_ai"
        )
        
        # 连接信号
        self.current_worker.finished.connect(self.on_regenerate_finished)
        self.current_worker.error.connect(self.on_processing_error)
        self.current_worker.progress.connect(self.on_progress_updated)
        
        # 启动线程
        self.current_worker.start()
    
    def on_regenerate_finished(self, image_result: ImageResult, ai_result: dict):
        """重新生成完成"""
        self.current_ai_result = ai_result
        
        # 更新AI数据
        self.title_input.setText(ai_result.get('title', ''))
        self.alt_text_input.setPlainText(ai_result.get('alt_text', ''))
        
        # 恢复控件状态
        self.set_processing_state(False)
        
        QMessageBox.information(self, "Success", "SEO data regenerated successfully!")
    
    def on_keyword_changed(self, text: str):
        """关键词输入变化时的处理"""
        # 只有在有图片加载且有用户输入关键词时才启用AI按钮
        has_image = self.image_display.current_image_path is not None
        has_keyword = bool(text.strip())
        self.process_with_ai_button.setEnabled(has_image and has_keyword)
    
    def reset(self):
        """重置界面状态"""
        self.current_image_result = None
        self.current_ai_result = None
        self.image_display.clear_images()
        self.image_drop_label.reset()
        self.keyword_input.reset()
        self.title_input.clear()
        self.alt_text_input.clear()
        self.file_name_input.clear()
        self.process_image_only_button.setEnabled(False)
        self.process_with_ai_button.setEnabled(False)
    
    def open_output_folder(self):
        """打开输出文件夹"""
        if not self.current_image_path:
            QMessageBox.warning(self, "Warning", "No image loaded!")
            return
        
        # 创建输出文件夹路径
        from pathlib import Path
        input_path = Path(self.current_image_path)
        output_folder = input_path.parent / "image-optimized"
        
        # 如果文件夹不存在，提示用户
        if not output_folder.exists():
            QMessageBox.information(
                self, 
                "信息", 
                f"输出文件夹将在处理图片后自动创建：\n{output_folder}\n\n请先处理图片！"
            )
            return
        
        try:
            import subprocess
            import platform
            
            if platform.system() == "Darwin":  # macOS
                subprocess.run(["open", str(output_folder)])
            elif platform.system() == "Windows":
                subprocess.run(["explorer", str(output_folder)])
            else:  # Linux
                subprocess.run(["xdg-open", str(output_folder)])
                
        except Exception as e:
            QMessageBox.warning(self, "错误", f"无法打开文件夹：{e}")
    

    
    def on_custom_width_toggled(self, checked):
        """处理自定义宽度选项切换"""
        self.custom_width_input.setEnabled(checked)
        if checked:
            self.custom_width_input.setFocus()
    

    def get_target_width(self):
        """获取目标宽度"""
        target_width = self.width_button_group.checkedId()
        if target_width == -999:  # 自定义宽度
            try:
                custom_width_text = self.custom_width_input.text().strip()
                if not custom_width_text:
                    QMessageBox.warning(self, "Warning", "Please enter a value for custom width!")
                    return None
                custom_width = int(custom_width_text)
                if custom_width <= 0:
                    raise ValueError("Width must be positive")
                target_width = custom_width
            except (ValueError, TypeError):
                QMessageBox.warning(self, "Warning", "Please enter a valid positive number for custom width!")
                return None
        elif target_width == -1:  # 没有选中任何选项
            target_width = 800  # 默认值
        
        return target_width
    
    def closeEvent(self, event):
        """窗口关闭事件"""
        # 停止任何正在运行的工作线程
        if self.current_worker and self.current_worker.isRunning():
            self.current_worker.quit()
            self.current_worker.wait()
        
        event.accept()
    
    # 拖拽事件处理方法
    def dragEnterEvent(self, event: QDragEnterEvent):
        """拖拽进入事件"""
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls:
                file_path = urls[0].toLocalFile()
                if file_path and self._is_image_file(file_path):
                    event.acceptProposedAction()
                    self.setStyleSheet("""
                        QMainWindow {
                            border: 3px dashed #0078d4;
                        }
                    """)
                else:
                    event.ignore()
        else:
            event.ignore()
    
    def dragLeaveEvent(self, event):
        """拖拽离开事件"""
        self.setStyleSheet("")
    
    def dropEvent(self, event: QDropEvent):
        """拖拽放下事件"""
        self.setStyleSheet("")
        
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls:
                file_path = urls[0].toLocalFile()
                if file_path and self._is_image_file(file_path):
                    self.load_image(file_path)
                    event.acceptProposedAction()
                else:
                    QMessageBox.warning(self, "Warning", "Please drop a valid image file!")
    
    def _is_image_file(self, file_path: str) -> bool:
        """检查是否为支持的图片格式"""
        if not file_path:
            return False
        
        valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp', '.heif', '.heic'}
        return Path(file_path).suffix.lower() in valid_extensions
    
    def load_image(self, image_path: str):
        """加载图片到 BeforeAfterWidget"""
        self.current_image_path = image_path
        
        # 首先设置 Before 图片（原图）
        success = self.image_display.set_before_image(image_path)
        
        if success:
            # 更新提示文本
            self.drop_hint.setText(f"Original Image Loaded: {Path(image_path).name}")
            self.drop_hint.setStyleSheet("""
                QLabel {
                    padding: 15px;
                    background-color: #e8f5e8;
                    border-radius: 8px;
                    font-size: 14px;
                    color: #2e7d32;
                    margin-bottom: 10px;
                }
            """)
            
            # 从文件名提取关键词作为默认值
            file_name = Path(image_path).stem
            # 替换常见的分隔符为空格，并处理多个点号
            keyword = file_name.replace('_', ' ').replace('-', ' ').replace('.', ' ')
            # 去除多余空格
            keyword = ' '.join(keyword.split())
            self.keyword_input.reset()  # 重置输入框状态
            self.keyword_input.set_default_keyword(keyword)
            
            # 清除之前的结果
            self.alt_text_input.clear()
            self.title_input.clear()
            self.current_image_result = None
            self.current_ai_result = None
            
            # 启用处理按钮
            self.process_image_only_button.setEnabled(True)
            self.process_with_ai_button.setEnabled(True)
        else:
            QMessageBox.warning(self, "Error", f"Failed to load image: {image_path}")