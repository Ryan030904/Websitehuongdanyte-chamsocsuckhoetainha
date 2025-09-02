from flask import Flask, render_template
from flask_login import LoginManager
from flask_cors import CORS
from models import db, User
from routes import main, auth, api, admin
from config import config
import os
import tempfile

# OPTIONAL: load .env when running locally
try:
    from dotenv import load_dotenv  # requirements.txt của bạn đã có python-dotenv
    load_dotenv()
except Exception:
    pass

def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(__name__)

    # ----- Load configuration -----
    # Ưu tiên APP_ENV (production/staging/development), fallback sang đối số
    env_name = os.getenv('APP_ENV', config_name)
    app.config.from_object(config.get(env_name, config['default']))

    # ----- Firebase credentials qua ENV (nếu có) -----
    # Để không cần commit file JSON lên repo
    creds_json = os.getenv("FIREBASE_CREDENTIALS_JSON")
    if creds_json and not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tf:
            tf.write(creds_json.encode("utf-8"))
            tf.flush()
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = tf.name

    # ----- Initialize extensions -----
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Vui lòng đăng nhập để truy cập trang này.'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return User.query.get(int(user_id))
        except Exception:
            return None

    # ----- CORS -----
    CORS(app)

    # ----- Register blueprints -----
    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(admin, url_prefix='/admin')

    # ----- Error handlers -----
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    # ----- DB init / seed -----
    with app.app_context():
        # Tạo bảng nếu chưa có (demo nhanh với SQLite)
        db.create_all()

        # Tạo admin mặc định nếu chưa tồn tại
        admin_user = User.query.filter_by(email='admin@healthfirst.com').first()
        if not admin_user:
            admin_user = User(
                email='admin@healthfirst.com',
                display_name='Admin',
                is_admin=True
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            db.session.commit()
            print("[DB] Admin user created: admin@healthfirst.com / admin123")

    return app


# Create app instance (mặc định lấy theo APP_ENV nếu có)
app = create_app(os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    # Khi chạy local: đọc PORT từ env (mặc định 5000)
    port = int(os.getenv("PORT", 5000))
    # Gợi ý: đặt APP_ENV=development khi chạy local để bật debug
    debug = os.getenv('APP_ENV', 'development') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
