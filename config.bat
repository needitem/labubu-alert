@echo off
chcp 65001 > nul
echo Telegram Bot Token and Chat ID Setup
echo.
echo 1. Create bot and get token: https://t.me/BotFather
echo 2. Get Chat ID: https://t.me/userinfobot
echo.

set /p BOT_TOKEN="Bot Token: "
set /p CHAT_ID="Chat ID: "

echo TELEGRAM_BOT_TOKEN=%BOT_TOKEN%> .env
echo TELEGRAM_CHAT_ID=%CHAT_ID%>> .env

echo.
echo Setup complete. .env file created.
pause