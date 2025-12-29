"""
Tests for Image SEO Optimizer
"""

import unittest
import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from imgseofriend.config_manager import ConfigManager
from imgseofriend.ai_service import AIService


class TestConfigManager(unittest.TestCase):
    """测试配置管理器"""
    
    def setUp(self):
        self.config = ConfigManager()
    
    def test_default_config(self):
        """测试默认配置"""
        self.assertIsNotNone(self.config.get_api_base_url())
        self.assertIsNotNone(self.config.get_model_name())


class TestAIService(unittest.TestCase):
    """测试AI服务"""
    
    def setUp(self):
        self.config = ConfigManager()
        self.ai_service = AIService(self.config)
    
    def test_service_initialization(self):
        """测试服务初始化"""
        self.assertIsNotNone(self.ai_service)
        self.assertIsNotNone(self.ai_service.config_manager)


if __name__ == '__main__':
    unittest.main()