@echo off
chcp 65001 >nul
title AllinFarm
cd /d "%~dp0"

docker info >nul 2>&1
if errorlevel 1 (
  echo.
  echo Docker Desktop не запущений.
  echo Відкрийте Docker Desktop з меню Пуск, зачекайте, поки внизу зліва з'явиться "Engine running", і запустіть start.cmd ще раз.
  echo.
  pause
  exit /b 1
)

echo.
echo Запускаю AllinFarm. Перший раз це триває кілька хвилин: Docker завантажує і збирає все потрібне.
echo.
docker compose up --build --detach --wait
if errorlevel 1 (
  echo.
  echo Щось пішло не так. Скопіюйте текст вище і надішліть Claude.
  echo.
  pause
  exit /b 1
)

echo.
echo AllinFarm працює: http://localhost:8080
echo Пошта для розробки: http://localhost:8025
echo Щоб зупинити, двічі клацніть stop.cmd
echo.
start "" http://localhost:8080
timeout /t 10 >nul
