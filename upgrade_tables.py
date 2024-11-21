from app import create_app, db
from app.models.users import Users
from app.models.chat import Chat
from app.models.message import Message
from app.models.user_profile import UserProfile
# Импортируйте все остальные модели

app = create_app()

with app.app_context():
    db.create_all()

print("Tables created successfully")