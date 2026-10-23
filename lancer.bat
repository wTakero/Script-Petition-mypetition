@echo off
chcp 65001 > nul
echo Lancement du script d'automatisation Brave...
python "%~dp0automation_brave.py"
pause
