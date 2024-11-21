# Импорт необходимых модулей Flask и расширений
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.models.users import Users  # Импорт модели пользователя
from app import db  # Импорт экземпляра базы данных
from app.services.email_service import send_reset_email  # Импорт сервиса отправки email

# Создание экземпляра Blueprint для маршрутов аутентификации
bp = Blueprint('auth', __name__)

# Маршрут для регистрации пользователя
@bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()  # Получаем данные запроса в формате JSON
        # Проверяем, существует ли пользователь с указанным именем
        if Users.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 400
        # Проверяем, зарегистрирован ли указанный email
        if Users.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 400
        
        # Создаем нового пользователя и задаем ему пароль
        user = Users(username=data['username'], email=data['email'])
        user.set_password(data['password'])
        # Добавляем пользователя в базу данных и сохраняем изменения
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        db.session.rollback()  # Откатываем изменения в случае ошибки
        return jsonify({'error': str(e)}), 500
    finally:
        db.session.remove()  # Очищаем сессию после каждого действия

# Маршрут для входа пользователя
@bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()  # Получаем данные запроса в формате JSON
        # Проверяем, существует ли пользователь с указанным именем и паролем
        user = Users.query.filter_by(username=data['username']).first()
        if user and user.check_password(data['password']):
            access_token = create_access_token(identity=user.id)  # Создаем JWT-токен для авторизации
            return jsonify(access_token=access_token), 200
        return jsonify({'error': 'Invalid username or password'}), 401
    except Exception as e:
        db.session.rollback()  # Откатываем изменения в случае ошибки
        return jsonify({'error': str(e)}), 500
    finally:
        db.session.remove()  # Очищаем сессию после каждого действия

# Маршрут для запроса на сброс пароля
@bp.route('/reset_password', methods=['POST'])
def reset_request():
    try:
        data = request.get_json()  # Получаем данные запроса в формате JSON
        # Ищем пользователя по email
        user = Users.query.filter_by(email=data['email']).first()
        if user:
            send_reset_email(user)  # Отправляем пользователю email с инструкцией по сбросу пароля
        return jsonify({'message': 'An email has been sent with instructions to reset your password.'}), 200
    except Exception as e:
        db.session.rollback()  # Откатываем изменения в случае ошибки
        return jsonify({'error': str(e)}), 500
    finally:
        db.session.remove()  # Очищаем сессию после каждого действия

# Маршрут для сброса пароля по токену
@bp.route('/reset_password/<token>', methods=['POST'])
def reset_token(token):
    try:
        user = Users.verify_reset_token(token)  # Проверка действительности токена
        if user is None:
            return jsonify({'error': 'That is an invalid or expired token'}), 400
        data = request.get_json()  # Получаем новый пароль из данных запроса
        user.set_password(data['password'])  # Устанавливаем новый пароль для пользователя
        db.session.commit()  # Сохраняем изменения в базе данных
        return jsonify({'message': 'Your password has been updated!'}), 200 
    except Exception as e:
        db.session.rollback()  # Откатываем изменения в случае ошибки
        return jsonify({'error': str(e)}), 500
    finally:
        db.session.remove()  # Очищаем сессию после каждого действия