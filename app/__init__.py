from flask import Flask
from flask_cors import CORS # Добавляет поддержку кросс-доменных запросов с куки
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from config import Config

db = SQLAlchemy()
jwt = JWTManager()
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app, supports_credentials=True) # Добавляет поддержку кросс-доменных запросов с куки

    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    from app.routes import auth, users, chat, message, search_gif
    app.register_blueprint(auth.bp)
    app.register_blueprint(users.bp)
    app.register_blueprint(chat.bp)
    app.register_blueprint(message.bp)
    app.register_blueprint(search_gif.bp)

    return app