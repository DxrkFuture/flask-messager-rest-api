from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.users import Users
from app.models.user_profile import UserProfile
from datetime import datetime
from app import db

bp = Blueprint('user', __name__)


@bp.route('/profile', methods=['GET', 'PUT'])
@jwt_required()
def profile():
    try:
        user_id = get_jwt_identity()
        user = Users.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        if request.method == 'GET':
            profile = user.profile
            if not profile:
                return jsonify({'error': 'Profile not found'}), 404
            return jsonify({
                'username': user.username,
                'email': user.email,
                'bio': profile.bio,
                'location': profile.location,
                'birth_date': profile.birth_date.isoformat() if profile.birth_date else None,
                'is_private': profile.is_private
            }), 200
        
        elif request.method == 'PUT':
            data = request.get_json()
            if not user.profile:
                profile = UserProfile(user_id=user.id)
                db.session.add(profile)
            else:
                profile = user.profile
            
            profile.bio = data.get('bio', profile.bio)
            profile.location = data.get('location', profile.location)
            profile.is_private = data.get('is_private', profile.is_private)
            if 'birth_date' in data:
                profile.birth_date = datetime.strptime(data['birth_date'], '%Y-%m-%d').date()
            
            db.session.commit()
            return jsonify({'message': 'Profile updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.session.remove()  # Очищаем сессию после каждого действия

@bp.route('/profile/search/<string:username>', methods=['GET'])
@jwt_required()
def search_user_by_username(username):
    try:
        # Ищем пользователей с похожими именами
        users = Users.query.filter(Users.username.ilike(f"%{username}%")).all()
        
        if not users:
            return jsonify({'message': 'No users found'}), 404

        # Формируем список результатов
        results = [
            {
                'user_id': user.id,
                'username': user.username,
                'bio': user.profile.bio if user.profile else None,
                'is_private': user.profile.is_private if user.profile else False
            } for user in users
        ]

        return jsonify(results), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.session.remove()  # Очищаем сессию после каждого действия

@bp.route('/profile/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_profile(user_id):
    try:
        # Получаем профиль пользователя по user_id
        user = Users.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        profile = user.profile
        if not profile:
            return jsonify({'error': 'Profile not found'}), 404

        # Проверяем, является ли профиль приватным
        profile_data = {
            'username': user.username,
            'bio': profile.bio,
            'is_private': profile.is_private
        }
        if not profile.is_private:
            profile_data.update({
                'email': user.email,
                'location': profile.location,
                'birth_date': profile.birth_date.isoformat() if profile.birth_date else None,
            })

        return jsonify(profile_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.session.remove()  # Очищаем сессию после каждого действия