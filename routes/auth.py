from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from models import db, User, BankAccount

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

        # Seed default bank accounts for new user
        acc1 = BankAccount(user_id=user.id, account_name='Union Bank of India', balance=0.00, is_cash=False)
        acc2 = BankAccount(user_id=user.id, account_name='Indian Post Bank', balance=0.00, is_cash=False)
        acc3 = BankAccount(user_id=user.id, account_name='Fam pay', balance=0.00, is_cash=False)
        acc4 = BankAccount(user_id=user.id, account_name='Maharastra Bank', balance=0.00, is_cash=False)
        acc5 = BankAccount(user_id=user.id, account_name='Cash', balance=0.00, is_cash=True)

        db.session.add_all([acc1, acc2, acc3, acc4, acc5])
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

@auth_bp.route('/firebase-login', methods=['POST'])
def firebase_login():
    data = request.get_json(silent=True) or {}
    email = data.get('email', '').strip()
    name = data.get('name', '').strip()
    uid = data.get('uid', '').strip()

    if not email:
        return jsonify({'success': False, 'message': 'Email missing from Firebase authentication.'}), 400

    username = name if name else email.split('@')[0]
    
    # Find existing user by email or username
    user = User.query.filter((User.email == email) | (User.username == username)).first()
    if not user:
        # Create new user for Firebase Google login
        user = User(username=username, email=email)
        user.set_password(f"firebase_{uid[:12]}")
        db.session.add(user)
        db.session.commit()

        # Seed default bank accounts for the new user
        acc1 = BankAccount(user_id=user.id, account_name='Union Bank of India', balance=0.00, is_cash=False)
        acc2 = BankAccount(user_id=user.id, account_name='Indian Post Bank', balance=0.00, is_cash=False)
        acc3 = BankAccount(user_id=user.id, account_name='Fam pay', balance=0.00, is_cash=False)
        acc4 = BankAccount(user_id=user.id, account_name='Maharastra Bank', balance=0.00, is_cash=False)
        acc5 = BankAccount(user_id=user.id, account_name='Cash', balance=0.00, is_cash=True)

        db.session.add_all([acc1, acc2, acc3, acc4, acc5])
        db.session.commit()

    session['user_id'] = user.id
    session['username'] = user.username

    return jsonify({'success': True, 'redirect': url_for('attendance.attendance_view')})

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('auth.login'))
