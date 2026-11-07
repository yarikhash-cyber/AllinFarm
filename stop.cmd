@echo off
chcp 65001 >nul
title AllinFarm
cd /d "%~dp0"
echo Зупиняю AllinFarm. Дані в базі зберігаються до наступного запуску.
docker compose stop
timeout /t 5 >nul
