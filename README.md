# Chat Application

Этот проект предоставляет простой REST API мессенджер, включая авторизацию, регистрацию, создание и просмотр чатов, а также отправку сообщений. Веб-приложение работает на Python и библиотеками Flask.

## Установка и запуск

### Требования
1. Python 3.10 или выше
2. Установленные зависимости из `requirements.txt`

### Установка
1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/DxrkFuture/flask-messager-rest-api.git
    cd flask-messager-rest-api
    ```
2. Установите виртуальное окружение:
    ```
    python -m venv venv
    source venv/bin/activate   # Для Linux/MacOS
    venv\Scripts\activate      # Для Windows
    ```
3. Установите зависимости:
    ```
    pip install -r requirements.txt
    ```

### Запуск API
1. Инициализируйте базу данных postgres добавив/изменив строчки в файле .env:
    ```
    SECRET_KEY=your-secret-key
    DATABASE_URL=postgresql://username@adress/database
    MAIL_SERVER=smtp.googlemail.com # к примеру от google
    MAIL_PORT=587
    MAIL_USE_TLS=1
    MAIL_USERNAME=your-email@gmail.com
    MAIL_PASSWORD=your-email-password
    AWS_ACCESS_KEY_ID=your-aws-access-key
    AWS_SECRET_ACCESS_KEY=your-aws-secret-key
    S3_BUCKET=your-s3-bucket-name
    ```
    **Обязательно для безопасности поменяйте** `SECRET_KEY` **и** `DATABASE_URL`

2. Запустить инициализацию базы данных upgrade.tables.py
    ```
    python upgrade_tables.py
    ```
3. Запустить REST API:
    ```
    python run.py
    ```

## Описание API
### Роуты авторизации и регистрации
- POST /register

    **Регистрация нового пользователя.**

    Параметры (JSON):
    ```json
    {
        "username": "имя_пользователя",
        "email": "email_пользователя",
        "password": "пароль"
    }
    ```
    Ответ:
    ```json
    {
        "message": "Пользователь успешно зарегистрирован"
    }
    ```
- POST /login

    **Авторизация пользователя.**

    Параметры (JSON):
    ```json
    {
        "username": "имя_пользователя",
        "password": "пароль"
    }
    ```
    Ответ:
    ```json
    {
        "access_token": "токен"
    }
    ```

    **Далее все операции будут выполнятся с этим токеном**

### Роуты для управления пользователем
- GET /profile/search/ + username пользователя

    **Поиск пользователей по никнейму и получение user_id для создания чатов**

    К примеру GET /profile/search/user

     Заголовок:
    ```text
    Authorization: Bearer <токен>
    ```

    Ответ на запрос:
    ```json
    [
        {
            "bio": null,
            "is_private": false,
            "user_id": 1,
            "username": "username2"
        },
        {
            "bio": "Я человек. Дальше не придумал",
            "is_private": false,
            "user_id": 2,
            "username": "username1"
        }
    ]
    ```

- GET /profile/<user_id>

    **Получение информации о любом пользователе и статус приватности у каждого пользователя для скрытия конфидициальной информации**

    К примеру GET /profile/2

    Ответ:
    ```json
    {
        "bio": "Я человек. Дальше не придумал",
        "birth_date": null,
        "email": "username1@localhost",
        "is_private": false,
        "location": "страна и город",
        "username": "username1"
    }
    ```
    При ```is_private: true``` ответ:
    ```json
    {
        "bio": "Я человек. Дальше не придумал",
        "is_private": true,
        "username": "username1"
    }
    ```

### Роуты для чатов
- GET /chats

    **Получение списка чатов, в которых состоит пользователь.**
    
    Заголовок:
    ```text
    Authorization: Bearer <токен>
    ```
    Ответ:
    ```json
    [
        {
            "id": 1,
            "name": "Название чата",
            "participants": [1, 2, 3]
        }
    ]
    ```

- POST /chats

    **Создание нового чата.**

    Параметры (JSON):
    ```json
    {
        "name": "Название чата",
        "participant_ids": [2, 3]
    }
    ```
    Ответ:
    ```json
    {
        "id": 1,
        "name": "Название чата",
        "participants": [1, 2, 3]
    }
    ```

### Роуты для сообщений

- GET /chats/<chat_id>/messages

    **Получение всех сообщений в чате.**
    Ответ:
    ```json
    [
        {
            "id": 1,
            "content": "Сообщение",
            "timestamp": "2024-11-21T10:00:00",
            "user_id": 1
        }
    ]
    ```
- POST /chats/<chat_id>/messages

    **Отправка нового сообщения в чат.**

    Параметры (JSON):
    ```json
    {
        "content": "Текст сообщения"
    }
    ```
    Ответ:
    ```json
    {
        "id": 2,
        "content": "Текст сообщения",
        "timestamp": "2024-11-21T10:05:00",
        "user_id": 1
    }
    ```

# Структура проекта

`run.py` - Основной файл запуска Flask API.

`upgrade_tables.py` - Обновление структуры базы данных

`config.py` - Скрипт инициализации переменных с `.env`

`requirements.txt` - Зависимости проекта.

`README.md` - Описание проекта.

# Лицензия
**GNU GENERAL PUBLIC LICENSE Version 3**

