# Chat Application

Этот проект предоставляет простой REST API мессенджер, включая авторизацию, регистрацию, создание и просмотр чатов, а также отправку сообщений. Веб-приложение работает на Python, PostgreSQL и библиотеками Flask

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

    **Запрос:**
    ```json
    {
        "username": "имя_пользователя",
        "email": "email_пользователя",
        "password": "пароль"
    }
    ```
    **Ответы:**

    HTTP 201
    ```json
    {
        "message": "User created successfully"
    }
    ```
    HTTP 400
    ```json
    {
        "error": "Username already exists"
    }
    ```
    ИЛИ
    ```json
    {
        "error": "Email already registered"
    }
    ```
    HTTP 500
    ```json
    {
        "error": "Exception..."
    }
    ```
    
- POST /login

    **Авторизация пользователя.**

    **Запрос:**
    ```json
    {
        "username": "имя_пользователя",
        "password": "пароль"
    }
    ```
    **Ответы:**

    HTTP 200
    ```json
    {
        "access_token": "токен"
    }
    ```
    HTTP 401
    ```json
    {
        "error": "Invalid username or password"
    }
    ```
    HTTP 500
    ```json
    {
        "error": "Exception..."
    }
    ```

## Далее все операции будут выполнятся с этим токеном

**Заголовок:**
    ```
    Authorization: Bearer <токен>
    ```

### Роуты для управления пользователем
- GET /profile

    **Получение информации об своих данных профиля**

    **Ответы:**

    HTTP 200
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
    HTTP 404
    ```json
    {
        "error": "User not found"
    }
    ```
    ИЛИ
    ```json
    {
        "error": "Profile not found"
    }
    ```
    HTTP 500
    ```json
    {
        "error": "Exception..."
    }
    ```

- PUT /profile

    **Обновление информации об своих данных профиля**

    **Запрос:**
    ```json
    {
        "bio": "Я человек. Дальше не придумал",
        "birth_date": 2024-12-4, // или без "birth_date"
        "email": "username1@localhost",
        "is_private": false,
        "location": "страна Россия г. Мариуполь",
        "username": "username1"
    }
    ```
    **Ответы:**

    HTTP 200
    ```json
    {
        "message": "Profile updated successfully"
    }
    ```
    HTTP 500
    ```json
    {
        "error": "Exeption..."
    }
    ```
    
- GET /profile/search/ + username пользователя

    **Поиск пользователей по никнейму и получение user_id для создания чатов**

    К примеру GET /profile/search/user


    **Ответы:**

    HTTP 200
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
    HTTP 500
    ```json
    {
        "error": "Exeption..."
    }
    ```

- GET /profile/<user_id>

    **Получение информации о любом пользователе и статус приватности у каждого пользователя для скрытия конфидициальной информации**

    К примеру GET /profile/2

    **Ответы:**

    HTTP 200
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
    HTTP 404
    ```json
    {
        "error": "User not found"
    }
    ```
    ИЛИ
    ```json
    {
        "error": "Profile not found"
    }
    ```
    HTTP 500
    ```json
    {
        "error": "Exeption..."
    }
    ```

### Роуты для чатов
- GET /chats

    **Получение списка чатов, в которых состоит пользователь.**
    
    **Ответы:**
    HTTP 200
    ```json
    [
        {
            "created_at": "2024-11-13T19:43:47.312036", // дата создания
            "id": 1,
            "name": "Название чата",
            "participants": [1, 2]
        },
        {
        "created_at": "2024-11-13T19:45:48.908727",
        "id": 2,
        "name": "Название 2 чата",
        "participants": [
            1,
            3
        ]
    },
    ]
    ```
    HTTP 500
    ```json
    {
        "error": "Exeption..."
    }
    ```

- POST /chats

    **Создание нового чата.**

    **Запрос:**
    ```json
    {
        "name": "Название чата",
        "participant_ids": [2, 3]
    }
    ```
    **Ответы:**

    HTTP 201
    ```json
    {
        "created_at": "2024-12-04T21:02:07.218768",
        "id": 5,
        "name": "Название чата",
        "participants": [
            1,
            2
        ]
    }
    ```
    HTTP 500
    ```json
    {
        "error": "Exeption..."
    }
    ```
- GET /chats/<chat_id>

    **Вывод выбраного чата**
    
    **Ответы:**

    HTTP 200
    ```json
    {
        "created_at": "2024-11-13T19:43:47.312036",
        "id": 1,
        "name": "Название чата номер 1",
        "participants": [
            1,
            2
        ]
    }
    ```
    HTTP 404
    ```json
    {
        "error": "Chat not found or access denied"
    }
    HTTP 500
    ```json
    {
        "error": "Exeption..."
    }
    ```

- PUT /chats/<chat_id>

    **Обновление названия чата**

    **Запрос:**
    ```json
    {
        "name": "Новое название чата 1"
    }
    ```
    **Ответы:**
    HTTP 200
    ```json
    {
        "created_at": "2024-11-13T19:43:47.312036",
        "id": 1,
        "name": "Новое название чата 1",
        "participants": [
            1,
            2
        ]
    }
    ```
    HTTP 404
    ```json
    {
        "error": "Chat not found or access denied"
    }
    ```
    HTTP 500
    ```json
    {
        "error": "Exception..."
    }
    ```
### Роуты для сообщений

- GET /chats/<chat_id>/messages

    **Получение всех сообщений в чате.**

    **Ответ:**

    HTTP 200
    ```json
    [
        {
            "chat_id": 1, //номер чата
            "content": "Сообщение от пользователя с ID 1",
            "id": 7, //номер сообщения
            "timestamp": "2024-11-16T17:37:01.041250",
            "user_id": 1 //user_id пользователя
        },
        {
            "chat_id": 1, //номер чата
            "content": "Сообщение от пользователя с ID 2",
            "id": 16, //номер сообщения
            "timestamp": "2024-12-01T16:32:39.284799",
            "user_id": 2 //user_id пользователя
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
    **Ответы:**

    HTTP 201
    ```json
    {
        "chat_id": 1,
        "content": "Текст сообщения",
        "id": 19,
        "timestamp": "2024-12-04T21:15:45.784162",
        "user_id": 2
    }
    ```
    HTTP 400
    ```json
    {
        "error": "Content is required"
    }
    ```
    HTTP 404
    ```json
    {
        "error": "Chat not found or access denied"
    }
    ```
    HTTP 500
    ```json
    {
        "error": "Exception..."
    }
    ```

- PUT /messages/<message_id>

    **Изменение структуры сообщения**

    **Запрос:**
    ```json
    {
        "content": "Текст сообщения изменённый"
    }
    ```
    **Ответы:**

    HTTP 200
    ```json
    {
        "chat_id": 1,
        "content": "Текст сообщения изменённый",
        "id": 19,
        "timestamp": "2024-12-04T21:15:45.784162",
        "user_id": 2
    }
    ```
    HTTP 404
    ```json
    {
        "error": "Message not found or access denied"
    }
    ```
    HTTP 500
    ```json
    {
        "error": "Exception..."
    }
    ```

- DELETE /messages/<message_id>

    **Удаление сообщения**

    **Ответы:**

    HTTP 200
    ```json
    {
        "message": "Message deleted successfully"
    }
    ```
    HTTP 404
    ```json
    {
        "error": "Message not found or access denied"
    }
    ```
    HTTP 500
    ```json
    {
        "error": "Exception..."
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

