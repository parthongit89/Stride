from app import create_app
from models import db, User, BankAccount

app = create_app()

def test_app():
    with app.app_context():
        user = User.query.filter_by(username='demo_user').first()
        if not user:
            user = User(username='demo_user', email='demo@stride.app')
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()

            acc1 = BankAccount(user_id=user.id, account_name='Union Bank of India', balance=0.00, is_cash=False)
            acc5 = BankAccount(user_id=user.id, account_name='Cash', balance=0.00, is_cash=True)
            db.session.add_all([acc1, acc5])
            db.session.commit()

    with app.test_client() as client:
        # 1. Test Login
        login_res = client.post('/auth/login', data={'username': 'demo_user', 'password': 'password123'}, follow_redirects=True)
        print("Login test status code:", login_res.status_code)
        assert login_res.status_code == 200

        # 2. Test Attendance endpoints
        records_res = client.get('/attendance/api/records?year=2026&month=8')
        print("Attendance records API status code:", records_res.status_code)
        assert records_res.status_code == 200
        records_json = records_res.get_json()
        print("Attendance counters:", records_json.get('counters'))

        # Test note validation requirement for leave (absent)
        bad_update = client.post('/attendance/api/update', json={
            'date': '2026-08-16',
            'status': 'absent',
            'schedule_note': '' # Empty note should fail!
        })
        print("Empty note for absent status code:", bad_update.status_code)
        assert bad_update.status_code == 400
        print("Rule enforcement message:", bad_update.get_json().get('message'))

        # Good update with note
        good_update = client.post('/attendance/api/update', json={
            'date': '2026-08-16',
            'status': 'absent',
            'schedule_note': 'Family function attendance'
        })
        print("Valid update with note status code:", good_update.status_code)
        assert good_update.status_code == 200

        # 3. Test Expenses endpoints
        expenses_res = client.get('/expenses/api/data')
        print("Expenses API status code:", expenses_res.status_code)
        assert expenses_res.status_code == 200
        exp_data = expenses_res.get_json()
        print("Accounts count:", len(exp_data.get('accounts')))
        print("Transactions count:", len(exp_data.get('transactions')))

        # Test Nill Expenses endpoint
        nill_res = client.post('/expenses/api/nill')
        print("Nill expenses API status code:", nill_res.status_code)
        assert nill_res.status_code == 200
        assert nill_res.get_json().get('success') is True

        # Test Monthly report download
        report_res = client.get('/expenses/api/download-report?month=Aug2026')
        print("Monthly report download status code:", report_res.status_code)
        assert report_res.status_code == 200

        # 4. Test Assignments endpoints
        ass_res = client.get('/assignments/api/list')
        print("Assignments API status code:", ass_res.status_code)
        assert ass_res.status_code == 200

        # 5. Test Progress stats
        prog_res = client.get('/progress/api/stats')
        print("Progress stats API status code:", prog_res.status_code)
        assert prog_res.status_code == 200
        print("Progress metrics:", prog_res.get_json().get('metrics'))

        print("\nALL VERIFICATION TESTS PASSED SUCCESSFULLY ON POSTGRESQL!")

if __name__ == '__main__':
    test_app()
