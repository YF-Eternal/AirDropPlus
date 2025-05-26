# import os
# import shutil
# import subprocess

# def build():
#     # Clean previous build
#     if os.path.exists('dist'):
#         shutil.rmtree('dist')
#     if os.path.exists('build'):
#         shutil.rmtree('build')
#     subprocess.run(['pybabel', 'compile', '-d', 'translations'])

#     subprocess.run([
#         'pyinstaller',
#         '--name=AirDropPlus',
#         '--icon=static/icon.ico',
#         '--add-data=translations;translations',
#         '--add-data=static;static',
#         '--add-data=config;config',
#         '--add-data=templates;templates',
#         '--noconsole',
#         '--hidden-import=winrt.windows.foundation.collections',
#         '--clean',
#         'AirDropPlus.py'
#     ])

# if __name__ == '__main__':
#     build() 



import os
import shutil
import subprocess
import sys
import venv

# 项目依赖列表
REQUIREMENTS = [
    "flask==3.0.0",
    "flask-babel==4.0.0",
    "pillow==10.1.0",
    "pystray==0.19.5",
    "pyinstaller==6.2.0",
    "windows-toasts==1.3.1",
    "pyperclip==1.8.2",
    "pywin32==306"
]

VENV_DIR = 'build_venv'

def create_venv():
    if os.path.exists(VENV_DIR):
        shutil.rmtree(VENV_DIR)
    print("Creating virtual environment...")
    venv.create(VENV_DIR, with_pip=True)

def install_requirements():
    pip_path = os.path.join(VENV_DIR, 'Scripts', 'pip.exe')
    print("Installing required packages...")
    subprocess.check_call([pip_path, 'install'] + REQUIREMENTS)

def build_with_pyinstaller():
    python_path = os.path.join(VENV_DIR, 'Scripts', 'python.exe')
    pybabel_path = os.path.join(VENV_DIR, 'Scripts', 'pybabel.exe')

    print("Cleaning previous builds...")
    for folder in ['build', 'dist']:
        if os.path.exists(folder):
            shutil.rmtree(folder)

    print("Compiling translations...")
    subprocess.check_call([pybabel_path, 'compile', '-d', 'translations'])

    print("Running PyInstaller...")
    subprocess.check_call([
        python_path, '-m', 'PyInstaller',
        '--name=AirDropPlus',
        '--icon=static/icon.ico',
        '--add-data=translations;translations',
        '--add-data=static;static',
        '--add-data=config;config',
        '--add-data=templates;templates',
        '--noconsole',
        '--hidden-import=winrt.windows.foundation.collections',
        '--clean',
        'AirDropPlus.py'
    ])

def fix_pywin32_postinstall():
    python_path = os.path.join(VENV_DIR, 'Scripts', 'python.exe')
    script = os.path.join(VENV_DIR, 'Lib', 'site-packages', 'pywin32_postinstall.py')
    if os.path.exists(script):
        print("Registering pywin32...")
        subprocess.check_call([python_path, script, '-install'])


if __name__ == '__main__':
    create_venv()
    install_requirements()
    fix_pywin32_postinstall()
    build_with_pyinstaller()
    print("✅ Build complete! Check the dist/ folder.")
