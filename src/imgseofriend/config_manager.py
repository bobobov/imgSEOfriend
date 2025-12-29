from PySide6.QtCore import QSettings
from typing import Optional
import os
from pathlib import Path
import json
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class ConfigManager:
    """配置管理器，负责安全保存和读取应用程序设置"""
    
    def __init__(self, organization_name="ImageSEO", application_name="Optimizer"):
        # 优先使用加密配置，回退到 QSettings
        self.config_dir = Path.home() / ".imgfriend"
        self.config_file = self.config_dir / "config.enc"
        self.settings = QSettings(organization_name, application_name)
        
        # 确保配置目录存在
        self.config_dir.mkdir(exist_ok=True)
        
        # 初始化加密
        self._init_encryption()
    
    def _init_encryption(self):
        """初始化加密功能"""
        try:
            key_file = self.config_dir / "key"
            
            if key_file.exists():
                # 读取现有密钥
                with open(key_file, 'rb') as f:
                    key = f.read()
            else:
                # 生成新密钥
                key = Fernet.generate_key()
                with open(key_file, 'wb') as f:
                    f.write(key)
                
                # 设置文件权限（仅用户可读写）
                os.chmod(key_file, 0o600)
            
            self.cipher = Fernet(key)
        except ImportError:
              self.cipher = None
    
    def _load_encrypted_config(self) -> dict:
        """加载加密配置"""
        if not self.cipher or not self.config_file.exists():
            return {}
        
        try:
            with open(self.config_file, 'rb') as f:
                encrypted_data = f.read()
            
            decrypted_data = self.cipher.decrypt(encrypted_data)
            return json.loads(decrypted_data.decode())
        except Exception:
            pass
            return {}
    
    def _save_encrypted_config(self, config: dict):
        """保存加密配置"""
        if not self.cipher:
            return False
        
        try:
            config_json = json.dumps(config, indent=2)
            encrypted_data = self.cipher.encrypt(config_json.encode())
            
            with open(self.config_file, 'wb') as f:
                f.write(encrypted_data)
            
            # 设置文件权限（仅用户可读写）
            os.chmod(self.config_file, 0o600)
            return True
        except Exception:
            pass
            return False
    
    def save_api_base_url(self, url: str):
        """保存 API Base URL"""
        self.settings.setValue("api/api_base_url", url)
    
    def get_api_base_url(self) -> str:
        """获取 API Base URL"""
        return self.settings.value("api/api_base_url", "https://api.deepseek.com")
    
    def save_api_key(self, key: str):
        """安全保存 API Key"""
        config = self._load_encrypted_config()
        config["api_key"] = key
        
        if self._save_encrypted_config(config):
            # 加密保存成功，从 QSettings 中删除
            self.settings.remove("api/api_key")
        else:
            # 回退到 QSettings
            self.settings.setValue("api/api_key", key)
    
    def get_api_key(self) -> str:
        """安全获取 API Key"""
        # 优先从加密配置读取
        config = self._load_encrypted_config()
        if "api_key" in config:
            return config["api_key"]
        
        # 回退到 QSettings（兼容旧版本）
        return self.settings.value("api/api_key", "")
    
    def save_model_name(self, model: str):
        """保存模型名称"""
        self.settings.setValue("api/model_name", model)
    
    def get_model_name(self) -> str:
        """获取模型名称"""
        return self.settings.value("api/model_name", "deepseek-chat")
    
    def save_system_prompt(self, prompt: str):
        """保存系统提示词"""
        self.settings.setValue("api/system_prompt", prompt)
    
    def get_system_prompt(self) -> str:
        """获取 System Prompt"""
        default_prompt = """Role: You are a Professional Image SEO Specialist and Accessibility Expert.

Task: Generate SEO-optimized Title and Alternative Text (Alt Text) for processed images in English language.

Input: {keyword}

Guiding Principles:

Contextual Analysis:
- Analyze the keyword to understand the subject matter (product, scene, object, etc.)
- Consider the image context based on the keyword pattern

SEO Title Strategy:
- Create a descriptive, searchable title (5-12 words)
- Structure: [Subject] + [Key Attribute/Feature] + [Context/Purpose]
- Use Title Case for better readability
- Include relevant descriptive terms that users might search for

Alt Text Strategy:
- Write comprehensive description for accessibility and SEO
- Focus on visual elements: color, composition, style, context
- Incorporate the keyword naturally
- Maximum 150 characters for optimal compatibility
- Avoid redundant phrases like "image of" or "picture of"

Special Considerations:
- For product keywords: focus on features, usage, and appearance
- For scene keywords: describe the visual composition and atmosphere  
- For abstract keywords: interpret the visual representation creatively
- Maintain professional tone while being descriptive

Output Requirement:
You must respond ONLY with a valid JSON object.
Output Format: 
{
  "title": "Descriptive title in Title Case",
  "alt_text": "Detailed description for accessibility and SEO"
}"""
        return self.settings.value("api/system_prompt", default_prompt)
    
    def save_output_width(self, width: int):
        """保存输出宽度"""
        self.settings.setValue("output/width", width)
    
    def get_output_width(self) -> int:
        """获取输出宽度"""
        return int(self.settings.value("output/width", 1200))
    
    def save_output_quality(self, quality: int):
        """保存输出质量"""
        self.settings.setValue("output/quality", quality)
    
    def get_output_quality(self) -> int:
        """获取输出质量"""
        return int(self.settings.value("output/quality", 80))
    
    def save_output_directory(self, path: str):
        """保存输出目录"""
        self.settings.setValue("output/directory", path)
    
    def get_output_directory(self) -> str:
        """获取输出目录"""
        return self.settings.value("output/directory", "")
    
    def get_all_config(self) -> dict:
        """获取所有配置"""
        return {
            "api_base_url": self.get_api_base_url(),
            "api_key": self.get_api_key(),
            "model_name": self.get_model_name(),
            "system_prompt": self.get_system_prompt(),
            "output_width": self.get_output_width(),
            "output_quality": self.get_output_quality(),
            "output_directory": self.get_output_directory()
        }
    
    def save_all_config(self, config: dict):
        """保存所有配置"""
        if "api_base_url" in config:
            self.save_api_base_url(config["api_base_url"])
        if "api_key" in config:
            self.save_api_key(config["api_key"])
        if "model_name" in config:
            self.save_model_name(config["model_name"])
        if "system_prompt" in config:
            self.save_system_prompt(config["system_prompt"])
        if "output_width" in config:
            self.save_output_width(config["output_width"])
        if "output_quality" in config:
            self.save_output_quality(config["output_quality"])
        if "output_directory" in config:
            self.save_output_directory(config["output_directory"])