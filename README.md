# Telegram Password Generator 

<p align="center">
  <b>Простой Telegram-бот для мгновенной генерации <strong>14-значных паролей</strong></b><br>

</p>
<br>

## 📱 Команды
``` /start ```

``` /gen  ```

<br>

## 📋 Полная установка

### 1. установите репозиторий


### 2. Установите зависимости 
``` 
pip install aiogram
```
### 3. Запустите бота python main_bot.py
Генератор паролей запущен!
Все действия логируются в users_log.txt

<br>

## ⌨️ Команды бота

| Команда | Описание | Пример |
|---------|----------|---------|
| /start | Показать справку | 📋 Доступные команды: |
| /gen | 14-значный пароль | ✅ X7kP9mL2qW8rT4vN |

<br>


## 🛠️ Как работает генерация
``` 
def generate_password():
    letters_digits = string.ascii_letters + string.digits
    return ''.join(secrets.choice(letters_digits) for _ in range(14))
```


<br>

## 📊 Логирование

Все действия сохраняются в users_log.txt:
```
[2026-01-18 01:04:23] Матвей Скляров (@Motya_Sklyarov): команда_gen | X7kP9mL2qW8rT4vN
```
<br>

## 🛡️ Система мониторинга (опционально)

Автоматический контроль работы бота 24/7 — уведомления о сбоях + автоперезапуск.


<br>

## 💻 Системные требования

| Параметр | Требование |
|----------|------------|
| Python | 3.10+ |
| RAM | 128 МБ |
| Диск | 20 МБ |

macOS • Linux • Windows •

<br>

## 📄 Лицензия
MIT License © 2026 Матвей Скляров (@Motya_Sklyarov)

<br>

## ⭐ Поддержка

<p align="center">
  <a href="https://t.me/Pswd_Manager_bot">
    <img src="https://img.shields.io/badge/Telegram-@Pswd_Manager_bot-blue?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram Bot">
  </a>
  <a href="https://t.me/Motya_Sklyarov">
  <img src="https://img.shields.io/badge/Author-@Motya_Sklyarov-blue?style=for-the-badge&logo=telegram&logoColor=white" alt="Author">
  </a>
</p>

<div align="center">

Поставьте ⭐, если понравилось!