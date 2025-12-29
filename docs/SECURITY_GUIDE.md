# 🔐 API Key 安全指南

## 当前存储位置

### macOS
- **QSettings 位置**: `~/Library/Preferences/com.ImageSEO.Optimizer.plist`
- **加密配置位置**: `~/.imgfriend/config.enc`
- **加密密钥位置**: `~/.imgfriend/key`

### Windows
- **QSettings 位置**: 注册表 `HKEY_CURRENT_USER\Software\ImageSEO\Optimizer`
- **加密配置位置**: `%USERPROFILE%\.imgfriend\config.enc`
- **加密密钥位置**: `%USERPROFILE%\.imgfriend\key`

## 安全措施

### 1. 文件权限
- 配置文件设置为 `0o600`（仅用户可读写）
- 防止其他用户访问敏感信息

### 2. 加密存储
- 使用 Fernet 对称加密（AES 128 + HMAC）
- PBKDF2 密钥派生增强安全性
- 配置文件完全加密存储

### 3. 版本控制保护
- `.gitignore` 排除所有配置文件
- 防止意外提交敏感信息

## 安装加密依赖

```bash
pip3 install cryptography
```

## 使用建议

### ✅ 安全实践
1. **定期更换 API Key**
2. **使用最小权限原则**
3. **定期检查配置文件权限**
4. **备份加密密钥**

### ❌ 禁止行为
1. **不要将 API Key 硬编码在代码中**
2. **不要上传配置文件到公共仓库**
3. **不要在共享计算机上保存 API Key**
4. **不要将密钥文件发送给他人**

## 打包发布配置

### PyInstaller 配置
在 `.spec` 文件中添加：
```python
a = Analysis(
    # ... 其他配置
    excludes=['config_manager.py'],  # 如果不需要配置功能
    datas=[],
    # ...
)
```

### 排除文件
确保以下文件不被包含在发布包中：
- `~/.imgfriend/`
- `*.plist`
- `*.conf`

## 故障恢复

### 忘记 API Key
1. 删除配置目录：`rm -rf ~/.imgfriend`
2. 重新启动应用，重新配置 API Key

### 迁移到新设备
1. 复制 `~/.imgfriend/` 目录到新设备
2. 确保文件权限正确（`chmod 600 ~/.imgfriend/*`）

## 审计日志

应用会记录配置文件的访问情况，可在日志中查看：
- 配置读取时间
- 配置修改时间
- 加密失败警告

## 🧪 测试安全功能

运行测试脚本验证安全性：

```bash
python3 test_security.py
```

测试内容：
- ✅ API Key 加密保存
- ✅ 配置文件权限验证
- ✅ 加密读取功能
- ✅ Fernet 加密验证
- ✅ 旧配置自动迁移