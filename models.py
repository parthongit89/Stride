from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Relationships
    attendance_records = db.relationship('AttendanceRecord', backref='user', lazy=True, cascade="all, delete-orphan")
    bank_accounts = db.relationship('BankAccount', backref='user', lazy=True, cascade="all, delete-orphan")
    transactions = db.relationship('ExpenseTransaction', backref='user', lazy=True, cascade="all, delete-orphan")
    assignments = db.relationship('Assignment', backref='user', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'initial': self.username[0].upper() if self.username else 'U'
        }

class AttendanceRecord(db.Model):
    __tablename__ = 'attendance_records'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False) # 'present', 'absent', 'holiday', 'half_day'
    schedule_note = db.Column(db.Text, nullable=True)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'date', name='_user_date_uc'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'date': self.date.strftime('%Y-%m-%d'),
            'status': self.status,
            'schedule_note': self.schedule_note or ''
        }

class BankAccount(db.Model):
    __tablename__ = 'bank_accounts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    account_name = db.Column(db.String(100), nullable=False)
    balance = db.Column(db.Float, default=0.00)
    is_cash = db.Column(db.Boolean, default=False)
    
    transactions = db.relationship('ExpenseTransaction', backref='account', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'account_name': self.account_name,
            'balance': round(self.balance, 2),
            'is_cash': self.is_cash
        }

class ExpenseTransaction(db.Model):
    __tablename__ = 'expense_transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.String(20), nullable=False) # 'income', 'expense', 'withdrawal', 'deposit', 'transfer'
    amount = db.Column(db.Float, nullable=False)
    reason = db.Column(db.String(255), nullable=True)
    account_id = db.Column(db.Integer, db.ForeignKey('bank_accounts.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'type': self.type,
            'amount': round(self.amount, 2),
            'reason': self.reason or '',
            'account_id': self.account_id,
            'account_name': self.account.account_name if self.account else 'General',
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class Assignment(db.Model):
    __tablename__ = 'assignments'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), default='pending') # 'pending', 'in_progress', 'completed'
    due_date = db.Column(db.Date, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'status': self.status,
            'due_date': self.due_date.strftime('%Y-%m-%d') if self.due_date else None
        }
