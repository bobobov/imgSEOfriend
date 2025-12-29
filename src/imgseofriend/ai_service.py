import requests
import json
import time
from typing import Dict, Optional, Any
from .config_manager import ConfigManager


class AIService:
    """AI 服务类，负责调用 LLM API 生成 SEO 数据"""
    
    def __init__(self, config_manager: Optional[ConfigManager] = None):
        self.config_manager = config_manager or ConfigManager()
        self.timeout = 30  # 请求超时时间（秒）
        self.max_retries = 3  # 最大重试次数
    
    def _get_config(self) -> Dict[str, Any]:
        """获取 AI 配置"""
        return {
            "api_base_url": self.config_manager.get_api_base_url(),
            "api_key": self.config_manager.get_api_key(),
            "model_name": self.config_manager.get_model_name(),
            "system_prompt": self.config_manager.get_system_prompt()
        }
    
    def _build_payload(self, keyword: str, system_prompt: str, model_name: str) -> Dict[str, Any]:
        """构建 API 请求载荷"""
        user_prompt = f"Based on the keyword '{keyword}', generate a concise SEO Title and Alt Text. Output JSON only: {{\"title\": \"...\", \"alt_text\": \"...\"}}"
        
        return {
            "model": model_name,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user", 
                    "content": user_prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 200,
            "stream": False
        }
    
    def _parse_response_from_response_data(self, response_data: Dict[str, Any]) -> Dict[str, str]:
        """从 API 响应数据中提取 title 和 alt_text"""
        try:
            if "choices" in response_data and len(response_data["choices"]) > 0:
                content = response_data["choices"][0]["message"]["content"]
                
                # 清理内容：移除 markdown 代码块标记
                content = content.strip()
                
                # 移除 ```json 和 ``` 标记
                if content.startswith('```json'):
                    content = content[7:]  # 移除 ```json
                if content.startswith('```'):
                    content = content[3:]   # 移除 ```
                if content.endswith('```'):
                    content = content[:-3]  # 移除结尾的 ```
                
                content = content.strip()
                
                # 提取 JSON 部分
                if '{' in content and '}' in content:
                    start = content.find('{')
                    end = content.rfind('}') + 1
                    json_str = content[start:end]
                    return json.loads(json_str)
            
            # 如果都失败，返回默认值
            return {"title": "", "alt_text": ""}
            
        except (json.JSONDecodeError, KeyError, IndexError) as e:
            print(f"[AI_SERVICE] Error parsing response: {e}")
            return {"title": "", "alt_text": ""}

    def _parse_response(self, response_text: str) -> Dict[str, str]:
        """解析 API 响应，提取 title 和 alt_text"""
        try:
            # 尝试直接解析 JSON
            if response_text.strip().startswith('{'):
                return json.loads(response_text.strip())
            
            # 尝试从 OpenAI 格式响应中提取内容
            response_data = json.loads(response_text)
            return self._parse_response_from_response_data(response_data)
            
        except (json.JSONDecodeError, KeyError, IndexError) as e:
            print(f"[AI_SERVICE] Error parsing response: {e}")
            print(f"[AI_SERVICE] Response text: {response_text[:500]}...")
            return {"title": "", "alt_text": ""}
    
    def _make_request_with_retry(self, url: str, headers: Dict[str, str], 
                                payload: Dict[str, Any]) -> Optional[requests.Response]:
        """带重试机制的请求方法"""
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    url,
                    headers=headers,
                    json=payload,
                    timeout=self.timeout
                )
                
                if response.status_code == 200:
                    return response
                elif response.status_code == 401:
                    print(f"[AI_SERVICE] Authentication failed (attempt {attempt + 1}): Invalid API Key")
                    break  # 认证失败不重试
                elif response.status_code == 429:
                    wait_time = 2 ** attempt  # 指数退避
                    print(f"[AI_SERVICE] Rate limited (attempt {attempt + 1}), waiting {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    print(f"[AI_SERVICE] HTTP {response.status_code} (attempt {attempt + 1}): {response.text[:200]}")
                    if attempt < self.max_retries - 1:
                        time.sleep(1)
                        
            except requests.exceptions.Timeout:
                last_error = f"Request timeout (attempt {attempt + 1})"
                print(f"[AI_SERVICE] {last_error}")
                if attempt < self.max_retries - 1:
                    time.sleep(2)
            except requests.exceptions.ConnectionError:
                last_error = f"Connection error (attempt {attempt + 1})"
                print(f"[AI_SERVICE] {last_error}")
                if attempt < self.max_retries - 1:
                    time.sleep(2)
            except requests.exceptions.RequestException as e:
                last_error = f"Request exception (attempt {attempt + 1}): {e}"
                print(f"[AI_SERVICE] {last_error}")
                if attempt < self.max_retries - 1:
                    time.sleep(2)
        
        print(f"[AI_SERVICE] All attempts failed. Last error: {last_error}")
        return None
    
    def generate_seo_data(self, keyword: str, filename: str = "") -> Dict[str, str]:
        """
        生成 SEO 数据
        
        Args:
            keyword: 目标关键词
            filename: 文件名（可选，用于提供更多上下文）
            
        Returns:
            包含 title 和 alt_text 的字典，失败时返回空字符串
        """
        # 获取配置
        config = self._get_config()
        
        # 验证必要配置
        if not config["api_key"].strip():
            return {"title": "", "alt_text": ""}
        
        if not config["api_base_url"].strip():
            return {"title": "", "alt_text": ""}
        
        if not config["model_name"].strip():
            return {"title": "", "alt_text": ""}
        
        # 构建 API 请求
        url = f"{config['api_base_url'].rstrip('/')}/chat/completions"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config['api_key']}"
        }
        
        payload = self._build_payload(keyword, config["system_prompt"], config["model_name"])
        
        # 发送请求
        response = self._make_request_with_retry(url, headers, payload)
        
        if response is None:
            return {"title": "", "alt_text": ""}
        
        # 解析响应
        try:
            response_data = response.json()
            
            # 提取 SEO 数据
            seo_data = self._parse_response_from_response_data(response_data)
            
            # 验证返回数据
            if not isinstance(seo_data, dict) or "title" not in seo_data or "alt_text" not in seo_data:
                return {"title": "", "alt_text": ""}
            
            return seo_data
            
        except Exception:
            return {"title": "", "alt_text": ""}
    
    def test_connection(self) -> Dict[str, Any]:
        """
        测试 API 连接
        
        Returns:
            包含测试结果的字典
        """
        config = self._get_config()
        
        result = {
            "success": False,
            "message": "",
            "details": {}
        }
        
        # 验证配置
        if not config["api_key"].strip():
            result["message"] = "API Key is not configured"
            return result
        
        if not config["api_base_url"].strip():
            result["message"] = "API Base URL is not configured"
            return result
        
        if not config["model_name"].strip():
            result["message"] = "Model Name is not configured"
            return result
        
        result["details"] = {
            "api_base_url": config["api_base_url"],
            "model_name": config["model_name"],
            "api_key_provided": bool(config["api_key"].strip())
        }
        
        # 发送测试请求
        try:
            url = f"{config['api_base_url'].rstrip('/')}/chat/completions"
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {config['api_key']}"
            }
            
            test_payload = {
                "model": config["model_name"],
                "messages": [
                    {
                        "role": "user",
                        "content": "Hello, this is a connection test."
                    }
                ],
                "max_tokens": 10,
                "temperature": 0.1
            }
            
            response = requests.post(url, headers=headers, json=test_payload, timeout=10)
            
            if response.status_code == 200:
                result["success"] = True
                result["message"] = "Connection successful"
            else:
                result["message"] = f"HTTP {response.status_code}: {response.text[:100]}"
                
        except Exception as e:
            result["message"] = f"Connection failed: {str(e)}"
        
        return result