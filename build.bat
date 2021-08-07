@echo off
mkdir tmp
cd tmp
python -m PyInstaller -i ..\imgs\icon.ico --onefile ..\src\cppkernel.py
