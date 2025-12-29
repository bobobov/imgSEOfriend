#!/usr/bin/env python3
"""
Before/After 图片对比组件
支持拖动分割线查看图片对比效果
"""

import os
from pathlib import Path

from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt, QRect, QSize, Signal
from PySide6.QtGui import QPixmap, QPainter, QPen, QCursor, QResizeEvent, QColor, QImage
from PIL import Image
from pillow_heif import register_heif_opener

# 注册 HEIF 图片格式支持
register_heif_opener()


class BeforeAfterWidget(QWidget):
    """
    Before/After 图片对比组件
    支持拖动分割线查看对比效果
    """
    
    # 信号
    divider_moved = Signal(int)  # 分割线位置改变信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.before_pixmap = None
        self.after_pixmap = None
        self.before_path = None  # Before 图片路径
        self.after_path = None    # After 图片路径
        self.before_size = None   # Before 图片文件大小
        self.after_size = None     # After 图片文件大小
        self.before_dimensions = None   # Before 图片尺寸 (width, height)
        self.after_dimensions = None     # After 图片尺寸 (width, height)
        self.divider_position = 0.5  # 分割线位置 (0.0 - 1.0)
        self.dragging = False
        self.show_before = True  # 控制显示哪张图片
        self.current_image_path = None  # 当前加载的图片路径
        
        self.setMinimumSize(400, 300)
        self.setCursor(Qt.SplitHCursor)
        self.setMouseTracking(True)
        
        # 样式设置 - 匹配暗色主题
        self.setStyleSheet("""
            BeforeAfterWidget {
                border: 2px solid #3a3a3a;
                border-radius: 12px;
                background-color: #1e1e1e;
            }
        """)
    
    def format_file_size(self, size_bytes: int) -> str:
        """格式化文件大小为人类可读格式"""
        if size_bytes is None or size_bytes == 0:
            return "Unknown"
        
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                if size_bytes < 1.0:
                    return f"{size_bytes:.2f} {unit}"
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"
    
    def get_file_size(self, file_path: str) -> int:
        """获取文件大小（字节）"""
        try:
            if file_path and os.path.exists(file_path):
                return os.path.getsize(file_path)
        except Exception:
            pass
        return 0
    
    def get_image_dimensions(self, file_path: str) -> tuple:
        """获取图片尺寸 (width, height) - 使用 PIL 高效获取"""
        try:
            if file_path and os.path.exists(file_path):
                # 使用 PIL 只读取图片头部信息获取尺寸，不加载整个图片
                with Image.open(file_path) as img:
                    return (img.width, img.height)
        except Exception:
            pass
        return None
    
    def _load_file_info_async(self, image_type: str, file_path: str):
        """异步获取图片文件信息（大小和尺寸）"""
        try:
            # 获取文件大小
            file_size = self.get_file_size(file_path)
            
            # 获取图片尺寸
            dimensions = self.get_image_dimensions(file_path)
            
            if image_type == 'before':
                self.before_size = file_size
                self.before_dimensions = dimensions
            elif image_type == 'after':
                self.after_size = file_size
                self.after_dimensions = dimensions
            
            # 更新显示
            self.update()
        except Exception:
            pass
    
    def load_image_with_orientation(self, image_path: str) -> QPixmap:
        """加载图片并正确处理EXIF方向信息 - 优化版本"""
        try:
            # 对于HEIC文件，需要处理EXIF方向
            if image_path.lower().endswith(('.heic', '.heif')):
                return self._load_heic_with_orientation(image_path)
            
            # 对于其他格式，直接用QPixmap快速加载
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                return pixmap
            
            # 如果QPixmap加载失败，回退到原始方法
            return QPixmap(image_path)
                
        except Exception:
            # 如果出错，回退到原始方法
            return QPixmap(image_path)
    
    def _load_heic_with_orientation(self, image_path: str) -> QPixmap:
        """专门处理HEIC文件的EXIF方向"""
        try:
            # 使用PIL打开HEIC文件以获取正确的方向
            with Image.open(image_path) as img:
                # 获取EXIF方向信息
                orientation = None
                if hasattr(img, '_getexif') and img._getexif() is not None:
                    exif = img._getexif()
                    if exif:
                        from PIL.ExifTags import TAGS
                        for tag_id, value in exif.items():
                            tag = TAGS.get(tag_id, tag_id)
                            if tag == 'Orientation':
                                orientation = value
                                break
                
                # 根据方向旋转图片
                if orientation:
                    if orientation == 3:
                        img = img.rotate(180, expand=True)
                    elif orientation == 6:
                        img = img.rotate(270, expand=True)
                    elif orientation == 8:
                        img = img.rotate(90, expand=True)
                    elif orientation == 2:
                        img = img.transpose(Image.FLIP_LEFT_RIGHT)
                    elif orientation == 4:
                        img = img.rotate(180, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
                    elif orientation == 5:
                        img = img.rotate(270, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
                    elif orientation == 7:
                        img = img.rotate(90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
                
                # 转换为QPixmap
                import io
                buffer = io.BytesIO()
                
                # 如果是RGBA模式，转换为RGB
                if img.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                    img = background
                
                img.save(buffer, format='PNG')
                qimage = QImage()
                qimage.loadFromData(buffer.getvalue())
                
                return QPixmap.fromImage(qimage)
                
        except Exception:
            # 如果出错，回退到原始方法
            return QPixmap(image_path)
    
    def set_images(self, before_path: str, after_path: str):
        """设置前后图片"""
        try:
            self.before_pixmap = self.load_image_with_orientation(before_path)
            self.after_pixmap = self.load_image_with_orientation(after_path)
            
            if not self.before_pixmap.isNull() and not self.after_pixmap.isNull():
                self.before_path = before_path
                self.after_path = after_path
                # 异步获取文件大小和尺寸信息，避免阻塞主线程
                self.before_size = None
                self.after_size = None
                self.before_dimensions = None
                self.after_dimensions = None
                self.current_image_path = before_path
                self.update()
                
                # 在后台获取文件信息
                from PySide6.QtCore import QTimer
                QTimer.singleShot(10, lambda: self._load_file_info_async('before', before_path))
                QTimer.singleShot(10, lambda: self._load_file_info_async('after', after_path))
                return True
            else:
                print("Warning: Failed to load images")
                return False
        except Exception:
            pass
            return False
    
    def set_before_image(self, path: str):
        """设置 Before 图片"""
        try:
            self.before_pixmap = self.load_image_with_orientation(path)
            if not self.before_pixmap.isNull():
                self.before_path = path
                # 异步获取文件大小和尺寸信息，避免阻塞主线程
                self.before_size = None  # 先设为 None
                self.before_dimensions = None  # 先设为 None
                self.current_image_path = path
                self.update()
                
                # 在后台获取文件信息
                from PySide6.QtCore import QTimer
                QTimer.singleShot(10, lambda: self._load_file_info_async('before', path))
                return True
        except Exception:
            pass
        return False
    
    def set_after_image(self, path: str):
        """设置 After 图片"""
        try:
            self.after_pixmap = self.load_image_with_orientation(path)
            if not self.after_pixmap.isNull():
                self.after_path = path
                # 异步获取文件大小和尺寸信息，避免阻塞主线程
                self.after_size = None  # 先设为 None
                self.after_dimensions = None  # 先设为 None
                self.update()
                
                # 在后台获取文件信息
                from PySide6.QtCore import QTimer
                QTimer.singleShot(10, lambda: self._load_file_info_async('after', path))
                return True
        except Exception:
            pass
        return False
    
    def set_divider_position(self, position: float):
        """设置分割线位置 (0.0 - 1.0)"""
        self.divider_position = max(0.0, min(1.0, position))
        self.update()
        self.divider_moved.emit(int(self.divider_position * self.width()))
    
    def paintEvent(self, event):
        """绘制事件"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        rect = self.rect()
        
        # 预留顶部和底部的标签空间
        label_height = 35
        image_rect = QRect(0, label_height, rect.width(), rect.height() - 2 * label_height)
        
        if self.before_pixmap:
            # 绘制背景
            painter.fillRect(rect, QColor(30, 30, 30))  # 暗色背景
            
            # 缩放图片以适应图片区域，保持宽高比
            scaled_before = self.before_pixmap.scaled(
                image_rect.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            
            # 计算图片在图片区域内的居中位置
            x_offset = (image_rect.width() - scaled_before.width()) // 2
            y_offset = (image_rect.height() - scaled_before.height()) // 2
            
            # 创建实际的图片显示区域
            actual_image_rect = QRect(
                image_rect.left() + x_offset, 
                image_rect.top() + y_offset,
                scaled_before.width(), 
                scaled_before.height()
            )
            
            if self.after_pixmap:
                # 两张图片都存在时，显示对比效果
                scaled_after = self.after_pixmap.scaled(
                    image_rect.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
                
                # 计算分割线位置（相对于实际图片区域）
                divider_x = actual_image_rect.left() + int(actual_image_rect.width() * self.divider_position)
                
                # 绘制 Before 图片（左侧）- 使用裁剪区域
                painter.setClipRect(actual_image_rect.left(), actual_image_rect.top(), 
                                   divider_x - actual_image_rect.left(), actual_image_rect.height())
                painter.drawPixmap(actual_image_rect, scaled_before)
                
                # 绘制 After 图片（右侧）- 使用裁剪区域
                painter.setClipRect(divider_x, actual_image_rect.top(), 
                                   actual_image_rect.right() - divider_x, actual_image_rect.height())
                painter.drawPixmap(actual_image_rect, scaled_after)
                
                # 清除裁剪区域
                painter.setClipping(False)
                
                # 绘制分割线（只在图片区域内）
                painter.setPen(QPen(QColor(255, 255, 255, 200), 2))
                painter.drawLine(divider_x, actual_image_rect.top(), divider_x, actual_image_rect.bottom())
                
                # 绘制分割线手柄
                handle_width = 40
                handle_height = 60
                handle_x = divider_x - handle_width // 2
                handle_y = (rect.height() - handle_height) // 2
                
                # 手柄背景 - 使用主题色
                painter.fillRect(handle_x, handle_y, handle_width, handle_height, 
                               QColor(98, 0, 238, 220))  # 主题紫色
                
                # 手柄边框
                painter.setPen(QPen(Qt.white, 2))
                painter.drawRect(handle_x, handle_y, handle_width, handle_height)
                
                # 手柄箭头
                painter.setPen(QPen(Qt.white, 3))
                arrow_y = handle_y + handle_height // 2
                
                # 左箭头
                painter.drawLine(handle_x + 10, arrow_y, handle_x + 16, arrow_y)
                painter.drawLine(handle_x + 10, arrow_y - 3, handle_x + 10, arrow_y + 3)
                
                # 右箭头
                painter.drawLine(handle_x + handle_width - 16, arrow_y, 
                                handle_x + handle_width - 10, arrow_y)
                painter.drawLine(handle_x + handle_width - 10, arrow_y - 3, 
                                handle_x + handle_width - 10, arrow_y + 3)
            else:
                # 只有 Before 图片时，显示整张图片
                painter.drawPixmap(actual_image_rect, scaled_before)
            
            # 绘制外部标签
            font = painter.font()
            font.setBold(True)
            font.setPointSize(12)
            painter.setFont(font)
            
            # Before 标签 - 左上角（图片外面）
            painter.setPen(QPen(QColor(255, 255, 255, 180), 1))
            before_rect = painter.boundingRect(QRect(10, 10, 100, 30), 
                                              Qt.AlignLeft | Qt.AlignVCenter, "BEFORE")
            painter.fillRect(before_rect.adjusted(-5, -2, 5, 2), 
                           QColor(0, 0, 0, 120))  # 半透明背景
            painter.setPen(Qt.white)
            painter.drawText(10, 30, "BEFORE")
            
            # After 标签 - 右上角（图片外面，只有在有After图片时才显示）
            if self.after_pixmap:
                after_text = "AFTER"
                after_text_width = painter.fontMetrics().horizontalAdvance(after_text)
                painter.fillRect(rect.width() - after_text_width - 15, 10, 
                               after_text_width + 10, 30, QColor(0, 0, 0, 120))
                painter.drawText(rect.width() - after_text_width - 10, 30, "AFTER")
            
            # 绘制文件大小信息（底部，图片外面）
            if self.before_pixmap is not None or self.after_pixmap is not None:
                font.setPointSize(13)  # 增大2个字号
                font.setBold(False)
                painter.setFont(font)
                bottom_y = rect.height() - 30  # 调整位置为上方，为尺寸信息留空间
                
                # Before 文件大小（左侧）
                if self.before_pixmap is not None:
                    before_size_text = f"Before: {self.format_file_size(self.before_size)}"
                    painter.setPen(QPen(QColor(255, 255, 255, 160), 1))
                    painter.drawText(15, bottom_y, before_size_text)
                    
                    # Before 图片尺寸（左侧，文件大小下方）
                    if self.before_dimensions:
                        width, height = self.before_dimensions
                        before_dim_text = f"{width}*{height}px"
                        painter.setPen(QPen(QColor(255, 255, 255, 120), 1))  # 更透明的颜色
                        painter.drawText(15, bottom_y + 15, before_dim_text)
                
                # After 文件大小（右侧）
                if self.after_pixmap is not None:
                    after_size_text = f"After: {self.format_file_size(self.after_size)}"
                    after_size_width = painter.fontMetrics().horizontalAdvance(after_size_text)
                    painter.setPen(QPen(QColor(255, 255, 255, 160), 1))
                    painter.drawText(rect.width() - after_size_width - 15, bottom_y, after_size_text)
                    
                    # After 图片尺寸（右侧，文件大小下方）
                    if self.after_dimensions:
                        width, height = self.after_dimensions
                        after_dim_text = f"{width}*{height}px"
                        after_dim_width = painter.fontMetrics().horizontalAdvance(after_dim_text)
                        painter.setPen(QPen(QColor(255, 255, 255, 120), 1))  # 更透明的颜色
                        painter.drawText(rect.width() - after_dim_width - 15, bottom_y + 15, after_dim_text)
                    
                    # 计算并显示压缩比例（只在两张图片都存在且有有效大小时）
                    if self.before_size and self.before_size > 0 and self.after_size and self.after_size > 0:
                        compression_ratio = ((self.before_size - self.after_size) / self.before_size) * 100
                        if compression_ratio > 0:
                            compression_text = f"📉 {compression_ratio:.1f}% smaller"
                            compression_width = painter.fontMetrics().horizontalAdvance(compression_text)
                            painter.setPen(QPen(QColor(76, 175, 80, 200), 1))  # 绿色
                            painter.drawText((rect.width() - compression_width) // 2, bottom_y, compression_text)
            
        else:
            # 没有图片时显示提示 - 暗色主题
            painter.fillRect(rect, QColor(30, 30, 30))
            painter.setPen(QPen(QColor(136, 136, 136), 1))
            font = painter.font()
            font.setPointSize(16)
            font.setBold(True)
            painter.setFont(font)
            painter.drawText(rect, Qt.AlignCenter, "No Images Loaded\n\nDrag and drop an image to begin")
    
    def mousePressEvent(self, event):
        """鼠标按下事件"""
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.setCursor(Qt.ClosedHandCursor)
    
    def mouseReleaseEvent(self, event):
        """鼠标释放事件"""
        if event.button() == Qt.LeftButton:
            self.dragging = False
            self.setCursor(Qt.SplitHCursor)
    
    def mouseMoveEvent(self, event):
        """鼠标移动事件"""
        if self.dragging:
            # 更新分割线位置
            new_position = event.x() / self.width()
            self.set_divider_position(new_position)
        else:
            # 检查鼠标是否在分割线附近
            divider_x = int(self.width() * self.divider_position)
            if abs(event.x() - divider_x) < 20:
                self.setCursor(Qt.SplitHCursor)
            else:
                self.setCursor(Qt.ArrowCursor)
    
    def resizeEvent(self, event: QResizeEvent):
        """窗口大小改变事件"""
        super().resizeEvent(event)
        self.update()
    
    def get_divider_position(self) -> float:
        """获取当前分割线位置"""
        return self.divider_position
    
    def reset_position(self):
        """重置分割线到中间位置"""
        self.set_divider_position(0.5)


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # 创建测试窗口
    widget = BeforeAfterWidget()
    widget.setWindowTitle("Before/After Widget Test")
    
    # 设置测试图片（如果有）
    # widget.set_images("before.jpg", "after.jpg")
    
    widget.show()
    sys.exit(app.exec())