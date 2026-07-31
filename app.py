import os
from flask import Flask, redirect, url_for, session
from dotenv import load_dotenv
from models import db
from datetime import timedelta

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'stride-default-secret-key-2026')
    db_url = os.getenv('DATABASE_URL', 'sqlite:///stride.db')
    
    # Fix postgres:// URL if needed for SQLAlchemy compatibility
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
        
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Ultra-fast pooling & resilience for Neon serverless PostgreSQL
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_size': 10,
        'max_overflow': 20,
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_timeout': 30,
    }

    # Configure permanent session lifetime for 90 days
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=90)

    db.init_app(app)

    # Register Blueprints
    from routes.auth import auth_bp
    from routes.attendance import attendance_bp
    from routes.expenses import expenses_bp
    from routes.assignments import assignments_bp
    from routes.progress import progress_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(attendance_bp)
    app.register_blueprint(expenses_bp)
    app.register_blueprint(assignments_bp)
    app.register_blueprint(progress_bp)

    @app.route('/')
    def index():
        if 'user_id' in session:
            return redirect(url_for('attendance.attendance_view'))
        return redirect(url_for('auth.login'))

    # Static asset caching headers for lightning-fast loads
    @app.after_request
    def add_cache_headers(response):
        if request_path_is_static():
            response.headers['Cache-Control'] = 'public, max-age=31536000, immutable'
        return response

    return app

def request_path_is_static():
    from flask import request
    return request.path.startswith('/static/')

app = create_app()

if __name__ == '__main__':
    # Initialize DB tables only when running script directly
    with app.app_context():
        try:
            db.create_all()
        except Exception:
            pass
    app.run(host='127.0.0.1', port=5000, debug=True)
