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