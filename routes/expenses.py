from flask import Blueprint, render_template, request, jsonify, session, Response
from models import db, BankAccount, ExpenseTransaction, User
from datetime import datetime
from routes.attendance import login_required
import csv
import io

expenses_bp = Blueprint('expenses', __name__, url_prefix='/expenses')

@expenses_bp.route('/')
@login_required
def expenses_view():
    user_id = session['user_id']
    user = User.query.get(user_id)
    return render_template('expenses.html', user=user)

@expenses_bp.route('/api/data')
@login_required
def get_expenses_data():
    user_id = session['user_id']
    
    accounts = BankAccount.query.filter_by(user_id=user_id).all()
    transactions = ExpenseTransaction.query.filter_by(user_id=user_id).order_by(ExpenseTransaction.created_at.desc()).all()

    total_income = sum(t.amount for t in transactions if t.type in ['income', 'deposit'])
    total_expense = sum(t.amount for t in transactions if t.type in ['expense', 'withdrawal'])

    return jsonify({
        'success': True,
        'accounts': [a.to_dict() for a in accounts],
        'transactions': [t.to_dict() for t in transactions],
        'summary': {
            'total_income': round(total_income, 2),
            'total_expense': round(total_expense, 2),
            'net_balance': round(total_income - total_expense, 2)
        }
    })

@expenses_bp.route('/api/accounts/add', methods=['POST'])
@login_required
def add_account():
    user_id = session['user_id']
    data = request.get_json() or {}
    
    account_name = data.get('account_name', '').strip()
    initial_balance = data.get('initial_balance', 0.0)
    is_cash = data.get('is_cash', False)

    if not account_name:
        return jsonify({'success': False, 'message': 'Account name is required.'}), 400

    account = BankAccount(
        user_id=user_id,
        account_name=account_name,
        balance=float(initial_balance),
        is_cash=bool(is_cash)
    )
    db.session.add(account)
    db.session.commit()

    return jsonify({'success': True, 'account': account.to_dict()})

@expenses_bp.route('/api/transactions/add', methods=['POST'])
@login_required
def add_transaction():
    user_id = session['user_id']
    data = request.get_json() or {}

    t_type = data.get('type') # 'income', 'expense', 'withdrawal', 'deposit', 'transfer'
    amount = data.get('amount', 0.0)
    reason = data.get('reason', '').strip()
    account_id = data.get('account_id')

    if not t_type or not amount or float(amount) <= 0:
        return jsonify({'success': False, 'message': 'Valid type and positive amount are required.'}), 400

    account = None
    if account_id:
        account = BankAccount.query.filter_by(id=account_id, user_id=user_id).first()

    amount_val = float(amount)

    transaction = ExpenseTransaction(
        user_id=user_id,
        type=t_type,
        amount=amount_val,
        reason=reason,
        account_id=account.id if account else None
    )
    db.session.add(transaction)

    # Adjust account balance if linked
    if account:
        if t_type in ['income', 'deposit']:
            account.balance += amount_val
        elif t_type in ['expense', 'withdrawal']:
            account.balance -= amount_val

    db.session.commit()

    return jsonify({'success': True, 'transaction': transaction.to_dict()})

@expenses_bp.route('/api/transactions/edit/<int:t_id>', methods=['POST'])
@login_required
def edit_transaction(t_id):
    user_id = session['user_id']
    data = request.get_json() or {}
    
    transaction = ExpenseTransaction.query.filter_by(id=t_id, user_id=user_id).first()
    if not transaction:
        return jsonify({'success': False, 'message': 'Transaction not found.'}), 404

    new_reason = data.get('reason', '').strip()
    new_amount = data.get('amount')

    if new_reason:
        transaction.reason = new_reason

    if new_amount is not None and float(new_amount) > 0:
        diff = float(new_amount) - transaction.amount
        transaction.amount = float(new_amount)
        if transaction.account:
            if transaction.type in ['income', 'deposit']:
                transaction.account.balance += diff
            elif transaction.type in ['expense', 'withdrawal']:
                transaction.account.balance -= diff

    db.session.commit()

    return jsonify({'success': True, 'transaction': transaction.to_dict()})

@expenses_bp.route('/api/transactions/delete/<int:t_id>', methods=['POST'])
@login_required
def delete_transaction(t_id):
    user_id = session['user_id']
    data = request.get_json() or {}
    deletion_reason = data.get('deletion_reason', '').strip()

    if not deletion_reason:
        return jsonify({'success': False, 'message': 'Reason for deleting transaction is required.'}), 400

    transaction = ExpenseTransaction.query.filter_by(id=t_id, user_id=user_id).first()
    if not transaction:
        return jsonify({'success': False, 'message': 'Transaction not found.'}), 404

    # Reverse account balance impact if linked
    if transaction.account:
        if transaction.type in ['income', 'deposit']:
            transaction.account.balance -= transaction.amount
        elif transaction.type in ['expense', 'withdrawal']:
            transaction.account.balance += transaction.amount

    db.session.delete(transaction)
    db.session.commit()

    return jsonify({'success': True, 'message': f'Transaction deleted. Reason logged: {deletion_reason}'})

@expenses_bp.route('/api/download-report')
@login_required
def download_report():
    user_id = session['user_id']
    month_str = request.args.get('month', datetime.now().strftime('%b%Y')) # e.g. Aug2026
    
    transactions = ExpenseTransaction.query.filter_by(user_id=user_id).order_by(ExpenseTransaction.created_at.asc()).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Date & Time', 'Type', 'Amount (INR)', 'Account', 'Reason'])

    for t in transactions:
        acc_name = t.account.account_name if t.account else 'General'
        writer.writerow([t.id, t.created_at.strftime('%Y-%m-%d %H:%M:%S'), t.type.upper(), f"₹{t.amount:.2f}", acc_name, t.reason or 'N/A'])

    filename = f"Stride-repport-trans-{month_str}.csv"

    response = Response(output.getvalue(), mimetype='text/csv')
    response.headers['Content-Disposition'] = f'attachment; filename={filename}'
    return response
