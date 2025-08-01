#!/usr/bin/env python3
"""
Build script for creating a standalone executable using PyInstaller.
"""

import subprocess
import sys
from pathlib import Path
import shutil
import os

def create_spec_file():
    """Create a PyInstaller spec file with proper configuration."""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['app/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('content', 'content'),
        ('static', 'static'),
        ('app', 'app'),
    ],
    hiddenimports=[
        'pygments.lexers',
        'pygments.formatters',
        'pygments.styles',
        'markdown.extensions',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
        'markdown.extensions.tables',
        'markdown.extensions.fenced_code',
        'pymdownx.superfences',
        'pymdownx.betterem',
        'pymdownx.tasklist',
        'pymdownx.tilde',
        'pymdownx.magiclink',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='nicegui-blog',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
'''
    
    with open('nicegui-blog.spec', 'w') as f:
        f.write(spec_content)
    print("Created PyInstaller spec file: nicegui-blog.spec")

def build_executable():
    """Build the standalone executable using PyInstaller."""
    print("Building standalone executable...")
    
    # Ensure spec file exists
    if not Path('nicegui-blog.spec').exists():
        create_spec_file()
    
    # Run PyInstaller
    cmd = [sys.executable, '-m', 'pyinstaller', '--clean', 'nicegui-blog.spec']
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Build successful!")
        print(result.stdout)
        
        # Check if executable was created
        exe_path = Path('dist') / 'nicegui-blog'
        if sys.platform == 'win32':
            exe_path = exe_path.with_suffix('.exe')
            
        if exe_path.exists():
            print(f"✅ Executable created: {exe_path}")
            print(f"📁 File size: {exe_path.stat().st_size / 1024 / 1024:.1f} MB")
        else:
            print("❌ Executable not found in expected location")
            
    except subprocess.CalledProcessError as e:
        print("❌ Build failed!")
        print(f"Error: {e.stderr}")
        return False
    
    return True

def clean_build():
    """Clean build artifacts."""
    print("Cleaning build artifacts...")
    
    dirs_to_clean = ['build', 'dist', '__pycache__']
    files_to_clean = ['nicegui-blog.spec']
    
    for dir_name in dirs_to_clean:
        if Path(dir_name).exists():
            shutil.rmtree(dir_name)
            print(f"🗑️  Removed: {dir_name}")
    
    for file_name in files_to_clean:
        if Path(file_name).exists():
            Path(file_name).unlink()
            print(f"🗑️  Removed: {file_name}")

def main():
    """Main build function."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Build NiceGUI blog executable')
    parser.add_argument('--clean', action='store_true', help='Clean build artifacts')
    parser.add_argument('--spec-only', action='store_true', help='Only create spec file')
    
    args = parser.parse_args()
    
    if args.clean:
        clean_build()
        return
    
    if args.spec_only:
        create_spec_file()
        return
    
    # Default: create spec and build
    print("🚀 Building NiceGUI Blog standalone executable...")
    
    if build_executable():
        print("\n🎉 Build completed successfully!")
        print("📁 You can find the executable in the 'dist' directory")
        
        # Show usage instructions
        exe_name = 'nicegui-blog.exe' if sys.platform == 'win32' else 'nicegui-blog'
        print(f"\n📖 To run the application:")
        print(f"   cd dist")
        print(f"   ./{exe_name}")
    else:
        print("\n❌ Build failed!")
        sys.exit(1)

if __name__ == '__main__':
    main()