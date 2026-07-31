from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from models import db, User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form if request.form else request.get_json(silent=True) or {}
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')

        if not username or not email or not password:
            if request.is_json:
                return jsonify({'success': False, 'message': 'All fields are required.'}), 400
            flash('All fields are required.', 'error')
            return render_template('auth/login.html', mode='register')

        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            if request.is_json:
                return jsonify({'success': False, 'message': 'Username or Email already exists.'}), 400
            flash('Username or Email already exists.', 'error')
            return render_template('auth/login.html', mode='register')

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        session['user_id'] = user.id
        session['username'] = user.username
        
        if request.is_json:
            return jsonify({'success': True, 'redirect': url_for('attendance.attendance_view')})
        return redirect(url_for('attendance.attendance_view'))

    return render_template('auth/login.html', mode='register')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form if request.form else request.get_json(silent=True) or {}
        username = data.get('username', '').strip()
        password = data.get('password', '')

        user = User.query.filter((User.username == username) | (User.email == username)).first()
        if not user or not user.check_password(password):
            if request.is_json:
                return jsonify({'success': False, 'message': 'Invalid username/email or password.'}), 400
            flash('Invalid username/email or password.', 'error')
            return render_template('auth/login.html', mode='login')

        session['user_id'] = user.id
        session['username'] = user.username

        if request.is_json:
            return jsonify({'success': True, 'redirect': url_for('attendance.attendance_view')})
        return redirect(url_for('attendance.attendance_view'))

    return render_template('auth/login.html', mode='login')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('auth.login'))
