from app import create_app
from models import db, User, AttendanceRecord, BankAccount, ExpenseTransaction, Assignment

app = create_app()

def reset_and_seed_clean():
    with app.app_context():
        # Clear all existing data
        ExpenseTransaction.query.delete()
        Assignment.query.delete()
        AttendanceRecord.query.delete()
        BankAccount.query.delete()
        User.query.delete()

        db.session.commit()
        print("Database cleared of all mock example data.")

        # Create fresh demo user
        demo_user = User(username='demo_user', email='demo@stride.app')
        demo_user.set_password('password123')
        db.session.add(demo_user)
        db.session.commit()

        # Create default initial bank accounts with 0 balance for the user
        acc1 = BankAccount(user_id=demo_user.id, account_name='Union Bank of India', balance=0.00, is_cash=False)
        acc2 = BankAccount(user_id=demo_user.id, account_name='Indian Post Bank', balance=0.00, is_cash=False)
        acc3 = BankAccount(user_id=demo_user.id, account_name='Fam pay', balance=0.00, is_cash=False)
        acc4 = BankAccount(user_id=demo_user.id, account_name='Maharastra Bank', balance=0.00, is_cash=False)
        acc5 = BankAccount(user_id=demo_user.id, account_name='Cash', balance=0.00, is_cash=True)

        db.session.add_all([acc1, acc2, acc3, acc4, acc5])
        db.session.commit()
        print("Initialized clean bank accounts with 0.00 balance.")

if __name__ == '__main__':
    reset_and_seed_clean()
