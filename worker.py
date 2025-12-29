import os
import time
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
from PySide6.QtCore import QThread, Signal
from PIL import Image
from pillow_heif import register_heif_opener
from ai_service import AIService
from config_manager import ConfigManager

# 注册 HEIF 图片格式支持
register_heif_opener()


class ImageResult:
    """图片处理结果类"""
    
    def __init__(self, original_path: str, processed_path: str, 
                 original_size: Tuple[int, int], processed_size: Tuple[int, int],
                 original_filesize: int, processed_filesize: int):
        self.original_path = original_path
        self.processed_path = processed_path
        self.original_size = original_size  # (width, height)
        self.processed_size = processed_size  # (width, height)
        self.original_filesize = original_filesize  # bytes
        self.processed_filesize = processed_filesize  # bytes
    
    def get_compression_ratio(self) -> float:
        """获取压缩比例"""
        if self.original_filesize == 0:
            return 0
        return (1 - self.processed_filesize / self.original_filesize) * 100
    
    def get_size_info(self) -> str:
        """获取尺寸信息字符串"""
        return (f"Original: {self.original_size[0]}x{self.original_size[1]}, "
                f"{self._format_filesize(self.original_filesize)}")


class ImageWorker(QThread):
    """
    图片处理工作线程
    负责图片 resize、WebP 转换和 AI SEO 数据生成
    """
    
    # 信号定义
    finished = Signal(object, dict)  # image_result, ai_result
    error = Signal(str)  # error_message
    progress = Signal(str)  # progress_message
    
    def __init__(self, image_path: str, keyword: str, target_width: int,
                 config_manager: Optional[ConfigManager] = None, 
                 output_directory: Optional[str] = None,
                 process_mode: str = "image_only"):  # "image_only" or "with_ai"
        super().__init__()
        
        # 输入参数
        self.image_path = image_path
        self.keyword = keyword
        self.target_width = target_width
        self.output_directory = output_directory
        self.process_mode = process_mode
        
        # 服务对象
        self.config_manager = config_manager or ConfigManager()
        self.ai_service = AIService(self.config_manager)
        
        # 处理参数
        self.output_quality = self.config_manager.get_output_quality()
    
    def _ensure_output_directory(self) -> str:
        """确保输出目录存在"""
        if self.output_directory:
            output_dir = Path(self.output_directory)
        else:
            # 在原图片路径下创建 image-optimized 文件夹
            input_path = Path(self.image_path)
            output_dir = input_path.parent / "image-optimized"
        
        output_dir.mkdir(exist_ok=True)
        return str(output_dir)
    
    def _get_output_filename(self, keyword: str) -> str:
        """生成输出文件名，处理重名冲突"""
        output_dir = self._ensure_output_directory()
        
        # 如果没有关键词，使用原文件名
        if not keyword or keyword.strip() == "":
            input_path = Path(self.image_path)
            base_name = input_path.stem + ".webp"
        else:
            # 清理关键词作为文件名
            clean_keyword = "".join(c for c in keyword if c.isalnum() or c in (' ', '-', '_')).strip()
            clean_keyword = clean_keyword.replace(' ', '-').lower()
            
            if not clean_keyword:
                clean_keyword = "optimized"
            
            base_name = f"{clean_keyword}.webp"
        
        output_path = Path(output_dir) / base_name
        
        # 检查文件是否存在，如果存在则添加序号
        counter = 1
        while output_path.exists():
            if not keyword or keyword.strip() == "":
                input_path = Path(self.image_path)
                base_name = f"{input_path.stem}-{counter}.webp"
            else:
                clean_keyword = "".join(c for c in keyword if c.isalnum() or c in (' ', '-', '_')).strip()
                clean_keyword = clean_keyword.replace(' ', '-').lower()
                if not clean_keyword:
                    clean_keyword = "optimized"
                base_name = f"{clean_keyword}-{counter}.webp"
            output_path = Path(output_dir) / base_name
            counter += 1
        
        return str(output_path)
    
    def _process_image(self) -> Optional[ImageResult]:
        """处理图片：resize 和 WebP 转换"""
        img = None
        try:
            self.progress.emit("Loading image...")
            
            # 打开原始图片
            img = Image.open(self.image_path)
            
            # 获取原始信息
            original_size = img.size
            original_filesize = os.path.getsize(self.image_path)
            
            self.progress.emit("Processing image...")
            
            # 计算新尺寸（保持宽高比）
            if img.width > self.target_width:
                ratio = self.target_width / img.width
                new_height = int(img.height * ratio)
                new_size = (self.target_width, new_height)
            else:
                new_size = img.size
            
            # 处理图片模式（转换为 RGB）
            if img.mode in ('RGBA', 'LA', 'P'):
                # 创建白色背景
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                img.close()
                img = background
            
            # Resize 图片
            if new_size != img.size:
                img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            # 生成输出文件名
            output_path = self._get_output_filename(self.keyword)
            
            self.progress.emit("Saving as WebP...")
            
            # 保存为 WebP（移除元数据以减小文件大小）
            img.save(output_path, 'WebP', quality=self.output_quality, method=6)
            
            # 获取处理后文件信息
            processed_filesize = os.path.getsize(output_path)
            processed_size = new_size
            
            # 关闭图片
            img.close()
            img = None
            
            self.progress.emit("Image processing completed!")
            
            result = ImageResult(
                original_path=self.image_path,
                processed_path=output_path,
                original_size=original_size,
                processed_size=processed_size,
                original_filesize=original_filesize,
                processed_filesize=processed_filesize
            )
            return result
                
        except Exception:
            pass
            import traceback
            traceback.print_exc()
            
            if img:
                img.close()
                
            error_msg = f"Image processing failed: {str(e)}"
            self.progress.emit(error_msg)
            self.error.emit(error_msg)
            return None
    
    def _generate_ai_data(self) -> Dict[str, str]:
        """生成 AI SEO 数据"""
        try:
            self.progress.emit("Generating SEO data...")
            
            # 获取文件名用于提供上下文
            filename = Path(self.image_path).stem
            
            # 调用 AI 服务
            ai_result = self.ai_service.generate_seo_data(self.keyword, filename)
            
            if ai_result and ai_result.get("title") and ai_result.get("alt_text"):
                self.progress.emit("SEO data generated!")
                return ai_result
            else:
                # 如果 AI 生成失败，返回默认数据
                default_result = {
                    "title": f"{self.keyword.title()} | Optimized Image",
                    "alt_text": f"Optimized image of {self.keyword}"
                }
                self.progress.emit("Using default SEO data...")
                return default_result
                
        except Exception as e:
            error_msg = f"AI data generation failed: {str(e)}"
            self.progress.emit(error_msg)
            self.error.emit(error_msg)
            # 返回默认数据
            return {
                "title": f"{self.keyword.title()} | Optimized Image",
                "alt_text": f"Optimized image of {self.keyword}"
            }
    
    def run(self):
        """线程主方法"""
        try:
            # 验证输入参数
            if not os.path.exists(self.image_path):
                self.error.emit(f"Image file not found: {self.image_path}")
                return
            
            # 只有在 AI 模式下才需要关键词
            if self.process_mode == "with_ai" and not self.keyword.strip():
                self.error.emit("Keyword is required for AI processing")
                return
            
            if self.target_width <= 0:
                self.error.emit("Target width must be greater than 0")
                return
            
            # 处理图片
            image_result = self._process_image()
            if image_result is None:
                return  # 错误已通过 error 信号发出
            
            # 根据处理模式决定是否生成 AI 数据
            ai_result = None
            if self.process_mode == "with_ai":
                ai_result = self._generate_ai_data()
                
                # 如果AI生成成功，根据Title重命名文件
                if ai_result and ai_result.get("title"):
                    self.progress.emit("Renaming file based on AI title...")
                    new_filename = self._normalize_filename(ai_result["title"])
                    new_path = Path(image_result.processed_path).parent / f"{new_filename}.webp"
                    
                    # 重命名文件
                    try:
                        import shutil
                        shutil.move(image_result.processed_path, str(new_path))
                        # 更新结果中的路径
                        image_result.processed_path = str(new_path)
                        self.progress.emit(f"File renamed to: {new_filename}.webp")
                    except Exception as rename_error:
                        self.progress.emit(f"Warning: Failed to rename file: {rename_error}")
            
            # 发出完成信号
            self.finished.emit(image_result, ai_result)
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            error_msg = f"Worker thread error: {str(e)}"
            self.error.emit(error_msg)
    
    @staticmethod
    def _normalize_filename(title: str) -> str:
        """标准化文件名"""
        import re
        
        # 强制转换为小写
        normalized = title.lower()
        
        # 空格和特殊字符替换为短横线
        # 只保留字母、数字和短横线
        normalized = re.sub(r'[^a-z0-9\s-]', '-', normalized)
        
        # 空格替换为短横线
        normalized = normalized.replace(' ', '-')
        
        # 保持连续的短横线为单个
        normalized = re.sub(r'-+', '-', normalized)
        
        # 移除首尾的短横线
        normalized = normalized.strip('-')
        
        # 如果结果为空，使用默认名称
        if not normalized:
            normalized = "optimized-image"
        
        return normalized
    
    @staticmethod
    def _format_filesize(size_bytes: int) -> str:
        """格式化文件大小"""
        if size_bytes < 1024:
            return f"{size_bytes}B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f}KB"
        else:
            return f"{size_bytes / (1024 * 1024):.1f}MB"