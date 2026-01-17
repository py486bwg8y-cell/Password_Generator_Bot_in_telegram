import os
import logging
from pathlib import Path
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from datetime import datetime
import asyncio
import string
import secrets
import sys


BASE_DIR = Path(__file__).resolve().parent


USER_LOG_FILE = BASE_DIR / "users_log.txt"


PID_FILE = BASE_DIR.parent / "monitor" / "Watchdog.pid"


PID_FILE.parent.mkdir(parents=True, exist_ok=True)


with open(PID_FILE, "w", encoding="utf-8") as f:
    f.write(str(os.getpid()))



bot_token = "" #токен канала
bot = Bot(token=bot_token)
dp = Dispatcher()

MONITOR_USER_ID = None

def generate_password():
    letters_digits = string.ascii_letters + string.digits
    special_chars = '?!'
    
    key_chars = [secrets.choice(letters_digits) for _ in range(14)]
    replace_pos = secrets.choice(range(14))
    key_chars[replace_pos] = secrets.choice(special_chars)
    
    return ''.join(key_chars)

def log_user_activity(name, username, action, message_text=""):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    
    if len(message_text) > 200:
        message_text = message_text[:200] + "..."
    
    log_entry = (
        f"{timestamp} | Имя: {name} | Username: @{username} | "
        f"Действие: {action} | Сообщение: {message_text}\n"
    )
    
    
    with open(USER_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)
    
    print(f"[{timestamp}] {name} (@{username}): {action} | {message_text}")

def log_monitor_activity(action, message_text=""):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = (
        f"{timestamp} | MONITOR | Действие: {action} | Сообщение: {message_text}\n"
    )
    
    
    monitor_log_file = BASE_DIR / "monitor_log.txt"
    with open(monitor_log_file, "a", encoding="utf-8") as f:
        f.write(log_entry)
    
    print(f"[{timestamp}] MONITOR: {action} | {message_text}")

logging.basicConfig(level=logging.INFO)

@dp.message(Command("start")) 
async def start_handler(message: Message):
    name = message.from_user.first_name or "Без имени"
    username = message.from_user.username or "Без username"
    
    log_user_activity(name, username, "команда_start", "/start")
    
    await message.answer(
        f"Привет, {name}! Я генерирую 14-значные пароли:\n\n"
        "Используй /gen для генерации!"
    )

@dp.message(Command("gen"))  
async def gen_handler(message: Message):
    name = message.from_user.first_name or "Без имени"
    username = message.from_user.username or "Без username"
    
    log_user_activity(name, username, "генерация_пароля", message.text)
    
    password = generate_password()
    
    await message.answer(
        f"Ваш пароль:\n`{password}`"
    )

@dp.message(F.text == "#ping")
async def handle_ping(message: Message):
    global MONITOR_USER_ID
    
    MONITOR_USER_ID = message.from_user.id
    log_monitor_activity("PING_ПОЛУЧЕН", "#ping")
    await message.answer("PONG")

@dp.message(F.text == "ERR_RESTART")
async def handle_restart(message: Message):
    log_monitor_activity("RESTART_СИГНАЛ", "ERR_RESTART")
    await message.answer("RESTARTING...")
    await asyncio.sleep(2)
    os.execv(sys.executable, [sys.executable] + sys.argv)

@dp.message()
async def all_other_messages(message: Message):
    global MONITOR_USER_ID
    
    name = message.from_user.first_name or "Без имени"
    username = message.from_user.username or "Без username"
    
    
    if MONITOR_USER_ID and message.from_user.id == MONITOR_USER_ID:
        return  
    
    if message.text:
        action = "текст"
    elif message.photo:
        action = "фото"
    elif message.voice:
        action = "голосовое"
    elif message.sticker:
        action = "стикер"
    elif message.video:
        action = "видео"
    else:
        action = "другое"
    
    log_user_activity(name, username, action, message.text or "без текста")
    
    if message.text and not message.text.startswith('/'):
        await message.answer(
            "Доступные команды:\n"
            "/start - приветствие\n"
            "/gen - сгенерировать 14-значный пароль"
        )

async def main():
    print("Генератор паролей запущен!")
    print(f"Лог пользователей → {USER_LOG_FILE}")
    print(f"PID для watchdog → {PID_FILE}")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
