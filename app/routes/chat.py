from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.chat import Chat
from app.models.users import Users
from app import db

bp = Blueprint('chat', __name__)

@bp.route('/chats', methods=['GET']) # вывод всех чатов в которых находится пользователь
@jwt_required()
def get_chats():
    try:
        user_id = get_jwt_identity()
        chats = Chat.query.filter(Chat.participants.any(id=user_id)).all()
        return jsonify([chat.to_dict() for chat in chats]), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.session.remove()  # Очищаем сессию после каждого действия

@bp.route('/chats', methods=['POST']) 
@jwt_required()
def create_chat(): # принимает user_id(когда bearar токен используется) + name(название чата) + participant_ids список пользователей(группа/личка)
    try:
        user_id = get_jwt_identity() # индификация пользователя по токену
        data = request.get_json()
        
        if 'name' not in data or 'participant_ids' not in data: # где participant_ids это id пользователей списком [1,2,3] к примеру
            return jsonify({'error': 'Name and participant_ids are required'}), 400
        
        participant_ids = data['participant_ids'] 
        if user_id not in participant_ids: # проверка сушествуюших пользователей в participant_ids
            participant_ids.append(user_id)
        
        chat = Chat(name=data['name']) #создание чата с пользователями
        for participant_id in participant_ids:
            participant = Users.query.get(participant_id)
            if participant:
                chat.participants.append(participant)
        
        db.session.add(chat) # применение в базе данных
        db.session.commit()
        
        return jsonify(chat.to_dict()), 201 # всё клёво
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 # серверная критическая ошибка при создании чата
    finally:
        db.session.remove()  # Очищаем сессию после каждого действия

@bp.route('/chats/<int:chat_id>', methods=['GET']) # вывод выбраного чата в которых находится пользователь
@jwt_required()
def get_chat(chat_id): #
    try:
        user_id = get_jwt_identity() # индификация пользователя по токену
        chat = Chat.query.filter_by(id=chat_id).first()
        
        if not chat or user_id not in [p.id for p in chat.participants]:
            return jsonify({'error': 'Chat not found or access denied'}), 404
        
        return jsonify(chat.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.session.remove()  # Очищаем сессию после каждого действия

@bp.route('/chats/<int:chat_id>', methods=['PUT']) # забыл, вроде меняет название чата
@jwt_required()
def update_chat(chat_id):
    try:
        user_id = get_jwt_identity()
        chat = Chat.query.filter_by(id=chat_id).first()
        
        if not chat or user_id not in [p.id for p in chat.participants]:
            return jsonify({'error': 'Chat not found or access denied'}), 404
        
        data = request.get_json()
        if 'name' in data:
            chat.name = data['name']
        
        db.session.commit()
        return jsonify(chat.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.session.remove()  # Очищаем сессию после каждого действия