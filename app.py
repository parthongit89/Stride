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
    
    # Engine options for Neon serverless connection stability
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
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

    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print("DB init note:", e)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
