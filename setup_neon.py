from app import create_app
from models import db, User, BankAccount, AttendanceRecord, ExpenseTransaction, Assignment

neon_url = "postgresql://neondb_owner:npg_3Mwy8uNStxsb@ep-empty-shape-atx8rqzu-pooler.c-9.us-east-1.aws.neon.tech/stride?sslmode=require"

app = create_app()
app.config['SQLALCHEMY_DATABASE_URI'] = neon_url

def setup_neon_db():
    with app.app_context():
        # Create tables in Neon PostgreSQL
        db.create_all()
        print("Neon PostgreSQL tables created successfully in 'stride' database!")

        # Initialize demo user if not existing
        user = User.query.filter_by(username='demo_user').first()
        if not user:
            user = User(username='demo_user', email='demo@stride.app')
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()

            acc1 = BankAccount(user_id=user.id, account_name='Union Bank of India', balance=0.00, is_cash=False)
            acc2 = BankAccount(user_id=user.id, account_name='Indian Post Bank', balance=0.00, is_cash=False)
            acc3 = BankAccount(user_id=user.id, account_name='Fam pay', balance=0.00, is_cash=False)
            acc4 = BankAccount(user_id=user.id, account_name='Maharastra Bank', balance=0.00, is_cash=False)
            acc5 = BankAccount(user_id=user.id, account_name='Cash', balance=0.00, is_cash=True)

            db.session.add_all([acc1, acc2, acc3, acc4, acc5])
            db.session.commit()
            print("Initialized Neon PostgreSQL default demo user & accounts.")

if __name__ == '__main__':
    setup_neon_db()
