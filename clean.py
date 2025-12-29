#!/usr/bin/env python3
"""
清理脚本 - Image SEO Optimizer
用于清理临时文件、构建产物和缓存
"""

import os
import shutil
import glob
from pathlib import Path


def clean_build_artifacts():
    """清理构建产物"""
    print("🧹 清理构建产物...")
    
    artifacts = [
        'build',
        'dist', 
        '__pycache__',
        '*.pyc',
        '*.pyo',
        '*.pyd',
        '.pytest_cache',
        '*.egg-info',
        '.coverage',
        'htmlcov',
        '.mypy_cache',
        '.tox'
    ]
    
    removed_count = 0
    
    for item in artifacts:
        if item.startswith('*.'):
            # 处理通配符
            files = glob.glob(item, recursive=True)
            for file_path in files:
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        removed_count += 1
                        print(f"   🗑️  删除文件: {file_path}")
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                        removed_count += 1
                        print(f"   🗑️  删除目录: {file_path}")
                except Exception as e:
                    print(f"   ❌ 无法删除 {file_path}: {e}")
        else:
            # 处理具体目录
            if os.path.exists(item):
                try:
                    if os.path.isdir(item):
                        shutil.rmtree(item)
                        print(f"   🗑️  删除目录: {item}")
                    else:
                        os.remove(item)
                        print(f"   🗑️  删除文件: {item}")
                    removed_count += 1
                except Exception as e:
                    print(f"   ❌ 无法删除 {item}: {e}")
    
    print(f"✅ 清理完成，删除了 {removed_count} 个项目")


def clean_python_cache():
    """清理 Python 缓存"""
    print("\n🧹 清理 Python 缓存...")
    
    # 递归查找所有 __pycache__ 目录
    for root, dirs, files in os.walk('.'):
        if '__pycache__' in dirs:
            pycache_path = os.path.join(root, '__pycache__')
            try:
                shutil.rmtree(pycache_path)
                print(f"   🗑️  删除: {pycache_path}")
            except Exception as e:
                print(f"   ❌ 无法删除 {pycache_path}: {e}")


def clean_temp_files():
    """清理临时文件"""
    print("\n🧹 清理临时文件...")
    
    temp_patterns = [
        '*.tmp',
        '*.temp',
        '*.log',
        '*.bak',
        '*.swp',
        '*.swo',
        '.DS_Store',
        'Thumbs.db',
        'desktop.ini'
    ]
    
    removed_count = 0
    
    for pattern in temp_patterns:
        files = glob.glob(pattern, recursive=True)
        for file_path in files:
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    removed_count += 1
                    print(f"   🗑️  删除临时文件: {file_path}")
            except Exception as e:
                print(f"   ❌ 无法删除 {file_path}: {e}")
    
    print(f"✅ 临时文件清理完成，删除了 {removed_count} 个文件")


def clean_ide_files():
    """清理 IDE 文件"""
    print("\n🧹 清理 IDE 文件...")
    
    ide_patterns = [
        '.vscode',
        '.idea',
        '*.sublime-*',
        '.atom',
        '*.code-workspace'
    ]
    
    removed_count = 0
    
    for pattern in ide_patterns:
        if pattern.startswith('*.'):
            files = glob.glob(pattern, recursive=True)
            for file_path in files:
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        removed_count += 1
                        print(f"   🗑️  删除 IDE 文件: {file_path}")
                except Exception as e:
                    print(f"   ❌ 无法删除 {file_path}: {e}")
        else:
            # 处理目录
            if os.path.exists(pattern):
                try:
                    shutil.rmtree(pattern)
                    removed_count += 1
                    print(f"   🗑️  删除 IDE 目录: {pattern}")
                except Exception as e:
                    print(f"   ❌ 无法删除 {pattern}: {e}")
    
    print(f"✅ IDE 文件清理完成，删除了 {removed_count} 个项目")


def show_clean_summary():
    """显示清理摘要"""
    print("\n" + "="*50)
    print("🧹 Image SEO Optimizer - 清理摘要")
    print("="*50)
    print("✅ 构建产物已清理")
    print("✅ Python 缓存已清理")
    print("✅ 临时文件已清理")
    print("✅ IDE 文件已清理")
    print("\n💡 提示:")
    print("   - 构建产物已删除，下次构建时将重新生成")
    print("   - Python 缓存已清理，将重新加载模块")
    print("   - 项目现在更加整洁，适合提交到版本控制")
    print("="*50)


def main():
    """主函数"""
    print("Image SEO Optimizer 清理工具")
    print("="*40)
    
    # 检查当前目录
    if not os.path.exists('app.py'):
        print("❌ 错误: 请在项目根目录中运行此脚本")
        return
    
    try:
        clean_build_artifacts()
        clean_python_cache()
        clean_temp_files()
        clean_ide_files()
        show_clean_summary()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  清理被用户中断")
    except Exception as e:
        print(f"\n❌ 清理过程中出现错误: {e}")


if __name__ == '__main__':
    main()