from app import create_app
from models import db, AttendanceRecord

app = create_app()

def clean_attendance():
    with app.app_context():
        # Clear old demo/test attendance records to ensure 100% accurate user data
        AttendanceRecord.query.delete()
        db.session.commit()
        print("Cleared old attendance records. Database reset to clean slate with Sunday default holidays!")

if __name__ == '__main__':
    clean_attendance()
