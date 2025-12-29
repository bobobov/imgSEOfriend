#!/usr/bin/env python3
"""
多平台构建脚本 - Image SEO Optimizer
支持 macOS 和 Windows 平台构建
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def run_command(cmd):
    """运行命令并显示输出"""
    print(f"执行命令: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(f"错误: {result.stderr}")
    
    return result.returncode == 0


def clean_build_dirs():
    """清理构建目录"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"清理目录: {dir_name}")
            shutil.rmtree(dir_name)


def build_platform(platform, mode='full'):
    """构建指定平台"""
    print(f"\n🔨 构建 {platform.upper()} 版本 (模式: {mode})")
    
    # 清理之前的构建
    clean_build_dirs()
    
    # 选择配置文件
    if platform == 'windows':
        spec_file = 'imgSEOfriend_windows.spec'
    elif platform == 'macos':
        spec_file = 'imgSEOfriend.spec'
    else:
        print(f"❌ 不支持的平台: {platform}")
        return False
    
    if not os.path.exists(spec_file):
        print(f"❌ 找不到配置文件: {spec_file}")
        return False
    
    # 构建命令
    cmd = f'python3 -m PyInstaller {spec_file}'
    
    if run_command(cmd):
        print(f"✅ {platform.upper()} 构建成功！")
        
        # 重命名输出文件以包含平台标识
        dist_dir = Path('dist')
        if dist_dir.exists():
            if platform == 'macos' and (dist_dir / 'ImageSEOFriend.app').exists():
                # macOS .app 包
                app_path = dist_dir / 'ImageSEOFriend.app'
                renamed_path = dist_dir / 'ImageSEOFriend-macOS.app'
                if renamed_path.exists():
                    shutil.rmtree(renamed_path)
                shutil.move(str(app_path), str(renamed_path))
                print(f"📦 重命名: ImageSEOFriend.app -> ImageSEOFriend-macOS.app")
                
            elif platform == 'windows' and (dist_dir / 'ImageSEOFriend.exe').exists():
                # Windows .exe
                exe_path = dist_dir / 'ImageSEOFriend.exe'
                renamed_path = dist_dir / 'ImageSEOFriend-Windows.exe'
                if renamed_path.exists():
                    renamed_path.unlink()
                exe_path.rename(renamed_path)
                print(f"📦 重命名: ImageSEOFriend.exe -> ImageSEOFriend-Windows.exe")
        
        return True
    else:
        print(f"❌ {platform.upper()} 构建失败")
        return False


def main():
    """主函数"""
    print("Image SEO Optimizer 多平台构建工具")
    print("=" * 50)
    print("🎨 使用图标: assets/app_icon.ico")
    print("=" * 50)
    
    # 检测当前平台
    current_platform = sys.platform.lower()
    if current_platform == 'darwin':
        current_platform = 'macos'
    elif current_platform in ['win32', 'windows']:
        current_platform = 'windows'
    
    print(f"🖥️  当前平台: {current_platform}")
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'all':
            # 构建所有平台（仅在当前支持的平台上）
            print("\n🌍 构建所有支持的平台...")
            
            if current_platform == 'macos':
                # 在 macOS 上只能构建 macOS 版本
                success = build_platform('macos')
            elif current_platform == 'windows':
                # 在 Windows 上只能构建 Windows 版本
                success = build_platform('windows')
            else:
                print(f"❌ 当前平台 {current_platform} 不支持跨平台构建")
                return
                
        elif command in ['macos', 'windows']:
            # 构建指定平台
            success = build_platform(command)
        else:
            print("使用方法:")
            print("  python3 build_multi.py all     # 构建所有支持的平台")
            print("  python3 build_multi.py macos   # 构建 macOS 版本")
            print("  python3 build_multi.py windows # 构建 Windows 版本")
            return
    else:
        # 默认构建当前平台
        print(f"\n🏠 构建当前平台版本: {current_platform}")
        success = build_platform(current_platform)
    
    if success:
        print("\n🎉 构建完成！")
        print("📦 输出目录: dist/")
        
        # 显示最终文件
        dist_dir = Path('dist')
        if dist_dir.exists():
            print("\n📁 生成的文件:")
            for item in dist_dir.iterdir():
                if item.is_file():
                    size = item.stat().st_size / (1024 * 1024)  # MB
                    print(f"   📄 {item.name} ({size:.1f} MB)")
                elif item.is_dir():
                    # 计算目录大小
                    total_size = 0
                    for file in item.rglob('*'):
                        if file.is_file():
                            total_size += file.stat().st_size
                    size = total_size / (1024 * 1024)  # MB
                    print(f"   📁 {item.name}/ ({size:.1f} MB)")
        
        print("\n💡 提示:")
        print("   - macOS: 双击 .app 文件或使用 open ImageSEOFriend-macOS.app")
        print("   - Windows: 双击 .exe 文件运行")
        print("   - 建议在目标平台上测试应用程序功能")
    else:
        print("\n💥 构建失败，请检查错误信息")


if __name__ == '__main__':
    main()