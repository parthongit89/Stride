from app import create_app
from models import db, User, BankAccount
import urllib.parse

app = create_app()

pg_pass = urllib.parse.quote_plus("parthpostgress89##")
pg_url = f"postgresql://postgres:{pg_pass}@localhost:5432/stride"
app.config['SQLALCHEMY_DATABASE_URI'] = pg_url

def init_pg():
    with app.app_context():
        db.create_all()
        print("PostgreSQL tables created successfully in 'stride' database!")

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
            print("Initialized PostgreSQL demo user & bank accounts.")

if __name__ == '__main__':
    init_pg()
