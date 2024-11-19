import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Đảm bảo đường dẫn database chính xác
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_DIR, "../instance/database.db")}'
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Tạo thư mục instance nếu chưa tồn tại
    instance_path = os.path.join(BASE_DIR, "../instance")
    if not os.path.exists(instance_path):
        os.makedirs(instance_path)

    from .routes import main
    app.register_blueprint(main)

    return app
