from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.message import Message
from app.models.chat import Chat
from app import db

bp = Blueprint('message', __name__)

@bp.route('/chats/<int:chat_id>/messages', methods=['GET'])
@jwt_required()
def get_messages(chat_id):
    user_id = get_jwt_identity()
    chat = Chat.query.filter_by(id=chat_id).first()
    
    if not chat or user_id not in [p.id for p in chat.participants]:
        return jsonify({'error': 'Chat not found or access denied'}), 404
    
    messages = Message.query.filter_by(chat_id=chat_id).order_by(Message.timestamp.asc()).all()
    return jsonify([message.to_dict() for message in messages]), 200

@bp.route('/chats/<int:chat_id>/messages', methods=['POST'])
@jwt_required()
def create_message(chat_id):
    try:
        user_id = get_jwt_identity()
        chat = Chat.query.filter_by(id=chat_id).first()
        
        if not chat or user_id not in [p.id for p in chat.participants]:
            return jsonify({'error': 'Chat not found or access denied'}), 404
        
        data = request.get_json()
        if 'content' not in data:
            return jsonify({'error': 'Content is required'}), 400
        
        message = Message(content=data['content'], user_id=user_id, chat_id=chat_id)
        db.session.add(message)
        db.session.commit()
        
        return jsonify(message.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.session.remove()  # Очищаем сессию после каждого действия

@bp.route('/messages/<int:message_id>', methods=['PUT'])
@jwt_required()
def update_message(message_id):
    try:
        user_id = get_jwt_identity()
        message = Message.query.filter_by(id=message_id, user_id=user_id).first()
        
        if not message:
            return jsonify({'error': 'Message not found or access denied'}), 404
        
        data = request.get_json()
        if 'content' in data:
            message.content = data['content']
        
        db.session.commit()
        return jsonify(message.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.session.remove()  # Очищаем сессию после каждого действия

@bp.route('/messages/<int:message_id>', methods=['DELETE'])
@jwt_required()
def delete_message(message_id):
    try:
        user_id = get_jwt_identity()
        message = Message.query.filter_by(id=message_id, user_id=user_id).first()
        
        if not message:
            return jsonify({'error': 'Message not found or access denied'}), 404
        
        db.session.delete(message)
        db.session.commit()
        return jsonify({'message': 'Message deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.session.remove()  # Очищаем сессию после каждого действия