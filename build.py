#!/usr/bin/env python3
"""
构建脚本 - Image SEO Optimizer
用于打包应用程序
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


def build_app(mode='simple', platform='auto'):
    """构建应用程序"""
    print(f"开始构建 Image SEO Optimizer (模式: {mode}, 平台: {platform})")
    
    # 清理之前的构建
    clean_build_dirs()
    
    # 选择配置文件
    if mode == 'full':
        if platform == 'windows':
            spec_file = 'imgSEOfriend_windows.spec'
        else:
            spec_file = 'imgSEOfriend.spec'
    else:
        spec_file = 'build_simple.spec'
    
    if not os.path.exists(spec_file):
        print(f"错误: 找不到配置文件 {spec_file}")
        return False
    
    # 构建命令
    cmd = f'python3 -m PyInstaller {spec_file}'
    
    if run_command(cmd):
        print(f"\n✅ 构建成功！")
        print(f"📦 输出目录: dist/")
        
        # 检查输出文件
        dist_dir = Path('dist')
        if dist_dir.exists():
            print("\n📁 生成的文件:")
            for file in dist_dir.rglob('*'):
                if file.is_file():
                    size = file.stat().st_size / (1024 * 1024)  # MB
                    print(f"   {file.name} ({size:.1f} MB)")
        
        return True
    else:
        print("❌ 构建失败")
        return False


def main():
    """主函数"""
    print("Image SEO Optimizer 构建工具")
    print("=" * 40)
    print("🎨 使用图标: assets/app_icon.ico")
    print("=" * 40)
    
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        if mode not in ['simple', 'full']:
            print("使用方法: python3 build.py [simple|full]")
            return
    else:
        print("选择构建模式:")
        print("1. simple - 简单构建（推荐用于测试）")
        print("2. full - 完整构建（包含所有资源和元数据）")
        
        choice = input("请选择 (1/2): ").strip()
        mode = 'simple' if choice == '1' else 'full'
    
    success = build_app(mode)
    
    if success:
        print("\n🎉 构建完成！")
        print("💡 提示: 可执行文件位于 dist/ 目录中")
        print("🧪 建议先测试应用程序功能是否正常")
    else:
        print("\n💥 构建失败，请检查错误信息")


if __name__ == '__main__':
    main()