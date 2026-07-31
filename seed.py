from app import create_app
from models import db, User, AttendanceRecord, BankAccount, ExpenseTransaction, Assignment
from datetime import datetime, date

app = create_app()

def seed_data():
    with app.app_context():
        # Create default demo user if not exists
        user = User.query.filter_by(username='demo_user').first()
        if not user:
            user = User(username='demo_user', email='demo@stride.app')
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
            print("Demo user created: demo_user / password123")

        # Bank accounts
        if BankAccount.query.filter_by(user_id=user.id).count() == 0:
            acc1 = BankAccount(user_id=user.id, account_name='Union Bank of India', balance=15400.00, is_cash=False)
            acc2 = BankAccount(user_id=user.id, account_name='Indian Post Bank', balance=4250.00, is_cash=False)
            acc3 = BankAccount(user_id=user.id, account_name='Fam pay', balance=1200.00, is_cash=False)
            acc4 = BankAccount(user_id=user.id, account_name='Maharastra Bank', balance=28900.00, is_cash=False)
            acc5 = BankAccount(user_id=user.id, account_name='Cash', balance=850.00, is_cash=True)

            db.session.add_all([acc1, acc2, acc3, acc4, acc5])
            db.session.commit()
            print("Bank accounts seeded.")

        # Attendance records for June, July, August 2026
        if AttendanceRecord.query.filter_by(user_id=user.id).count() == 0:
            sample_records = [
                # June 2026
                (date(2026, 6, 1), 'present', 'Semester start'),
                (date(2026, 6, 2), 'present', ''),
                (date(2026, 6, 3), 'absent', 'Medical checkup'),
                (date(2026, 6, 4), 'present', ''),
                (date(2026, 6, 5), 'half_day', 'Library research'),
                (date(2026, 6, 15), 'holiday', 'Summer festival'),

                # July 2026
                (date(2026, 7, 1), 'present', ''),
                (date(2026, 7, 2), 'present', ''),
                (date(2026, 7, 3), 'absent', 'Family visit'),
                (date(2026, 7, 10), 'holiday', 'Midterm recess'),
                (date(2026, 7, 15), 'present', ''),
                (date(2026, 7, 20), 'half_day', 'Workshop attendance'),

                # August 2026
                (date(2026, 8, 1), 'present', ''),
                (date(2026, 8, 2), 'present', ''),
                (date(2026, 8, 3), 'absent', 'Sick leave - Fever & cold'),
                (date(2026, 8, 4), 'present', ''),
                (date(2026, 8, 5), 'half_day', 'Doctor appointment in afternoon'),
                (date(2026, 8, 6), 'holiday', 'Independence Day rehearsal'),
                (date(2026, 8, 7), 'present', ''),
                (date(2026, 8, 8), 'present', ''),
                (date(2026, 8, 9), 'present', ''),
                (date(2026, 8, 10), 'present', ''),
                (date(2026, 8, 11), 'absent', 'Family emergency event'),
                (date(2026, 8, 12), 'present', ''),
                (date(2026, 8, 13), 'half_day', 'College festival setup'),
                (date(2026, 8, 14), 'present', ''),
                (date(2026, 8, 15), 'holiday', 'Independence Day'),
            ]
            for d, st, nt in sample_records:
                ar = AttendanceRecord(user_id=user.id, date=d, status=st, schedule_note=nt)
                db.session.add(ar)
            db.session.commit()
            print("Multi-month attendance records seeded.")

        # Assignments
        if Assignment.query.filter_by(user_id=user.id).count() == 0:
            ass1 = Assignment(user_id=user.id, title='Physics Assignment', status='pending', due_date=date(2026, 8, 20))
            ass2 = Assignment(user_id=user.id, title='Data Structures Graph Algorithms', status='in_progress', due_date=date(2026, 8, 18))
            ass3 = Assignment(user_id=user.id, title='Database Systems Lab Report 3', status='completed', due_date=date(2026, 8, 10))
            db.session.add_all([ass1, ass2, ass3])
            db.session.commit()
            print("Assignments seeded.")

        # Transactions
        if ExpenseTransaction.query.filter_by(user_id=user.id).count() == 0:
            acc1 = BankAccount.query.filter_by(user_id=user.id, account_name='Union Bank of India').first()
            acc5 = BankAccount.query.filter_by(user_id=user.id, account_name='Cash').first()

            t1 = ExpenseTransaction(user_id=user.id, type='income', amount=25000.00, reason='Monthly Internship Stipend', account_id=acc1.id)
            t2 = ExpenseTransaction(user_id=user.id, type='expense', amount=1200.00, reason='Reason : Glocery', account_id=acc1.id)
            t3 = ExpenseTransaction(user_id=user.id, type='withdrawal', amount=500.00, reason='Cash', account_id=acc1.id)
            t4 = ExpenseTransaction(user_id=user.id, type='deposit', amount=350.00, reason='Cash', account_id=acc1.id)

            db.session.add_all([t1, t2, t3, t4])
            db.session.commit()
            print("Transactions seeded.")

if __name__ == '__main__':
    seed_data()
