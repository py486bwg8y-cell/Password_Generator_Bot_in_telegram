import time
import psutil
import subprocess
from datetime import datetime
import asyncio
from aiogram import Bot
from pathlib import Path

BOT_TOKEN = "" #токен второго телеграм бота
ADMIN_ID = 1234567890 #User_id telegram 

BASE_DIR = Path(__file__).resolve().parent

LOG_FILE = BASE_DIR / "watchdog.log"

TARGET_PID_FILE = BASE_DIR / "Watchdog.pid"

MAIN_BOT_PATH = BASE_DIR.parent / "main" / "main_bot.py"

bot = Bot(token=BOT_TOKEN)


def log_entry(message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {message}"
    print(entry)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry + "\n")


async def send_notification(message: str):
    timestamp = datetime.now().strftime("%H:%M:%S")
    formatted_msg = f"[{timestamp}] {message}"
    try:
        await bot.send_message(ADMIN_ID, formatted_msg)
        log_entry("Уведомление отправлено")
    except Exception as e:
        log_entry(f"Ошибка уведомления: {e}")


def process_alive():
    if not TARGET_PID_FILE.exists():
        log_entry(f"Файл PID цели не найден: {TARGET_PID_FILE}")
        return False
    
    try:
        with open(TARGET_PID_FILE, "r", encoding="utf-8") as f:
            pid = int(f.read().strip())
        
        proc = psutil.Process(pid)
        status = proc.status()
        log_entry(f"Процесс цели PID={pid} статус={status}")
        return status in [psutil.STATUS_RUNNING, psutil.STATUS_SLEEPING]
    except psutil.NoSuchProcess:
        log_entry("Процесс цели не запущен")
        return False
    except Exception as e:
        log_entry(f"Ошибка проверки процесса: {e}")
        return False


def restart_target():
    try:
        proc = subprocess.Popen(["python3", str(MAIN_BOT_PATH)])
        log_entry(f"Цель перезапущена: PID={proc.pid}")
        asyncio.create_task(send_notification("Процесс цели перезапущен"))
    except Exception as e:
        log_entry(f"Ошибка перезапуска: {e}")
        asyncio.create_task(send_notification(f"Ошибка перезапуска: {e}"))


async def monitoring_loop():
    log_entry("Мониторинг процессов запущен")
    await send_notification("Мониторинг процессов инициализирован")
    
    if process_alive():
        await send_notification("Процесс цели: активен")
    else:
        log_entry("Процесс цели не активен при старте")
        await send_notification("Процесс цели: неактивен, запуск")
        restart_target()
    
    failure_count = 0
    cycle_count = 0
    
    while True:
        await asyncio.sleep(30)
        cycle_count += 1
        
        if not process_alive():
            failure_count += 1
            log_entry(f"Сбой процесса: {failure_count}/3 (цикл {cycle_count})")
            
            if failure_count >= 3:
                log_entry("Достигнут порог критических сбоев, перезапуск")
                await send_notification("Порог сбоев: инициирован перезапуск")
                restart_target()
                failure_count = 0
        else:
            if failure_count > 0:
                await send_notification("Процесс цели: восстановлен")
            failure_count = 0
        
        log_entry(f"Цикл мониторинга: {cycle_count}")


if __name__ == "__main__":
    asyncio.run(monitoring_loop())
