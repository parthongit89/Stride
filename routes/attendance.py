from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from models import db, AttendanceRecord, User
from datetime import datetime, timedelta
import calendar
from functools import wraps

attendance_bp = Blueprint('attendance', __name__, url_prefix='/attendance')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def calculate_streak(user_id, target_month, target_year, record_map):
    current_streak = 0
    max_streak = 0

    _, days_in_month = calendar.monthrange(target_year, target_month)
    
    for day in range(1, days_in_month + 1):
        d_str = f"{target_year:04d}-{target_month:02d}-{day:02d}"
        rec = record_map.get(d_str)
        status = rec.get('status') if isinstance(rec, dict) else (rec.status if rec else None)
        
        if status in ['present', 'half_day']:
            current_streak += 1
            if current_streak > max_streak:
                max_streak = current_streak
        elif status == 'holiday':
            # Holidays do not break present streaks
            continue
        else:
            current_streak = 0
            
    return max_streak

@attendance_bp.route('/')
@login_required
def attendance_view():
    user_id = session['user_id']
    user = User.query.get(user_id)
    return render_template('attendance.html', user=user)

@attendance_bp.route('/api/records')
@login_required
def get_records():
    user_id = session['user_id']
    year = request.args.get('year', datetime.now().year, type=int)
    month = request.args.get('month', datetime.now().month, type=int)

    records = AttendanceRecord.query.filter(
        AttendanceRecord.user_id == user_id,
        db.extract('year', AttendanceRecord.date) == year,
        db.extract('month', AttendanceRecord.date) == month
    ).all()

    records_dict = {r.date.strftime('%Y-%m-%d'): r.to_dict() for r in records}

    # Automatically set Sundays (weekday == 6) as default 'holiday' if not explicitly recorded
    _, days_in_month = calendar.monthrange(year, month)
    for day in range(1, days_in_month + 1):
        d_obj = datetime(year, month, day).date()
        d_str = d_obj.strftime('%Y-%m-%d')
        if d_obj.weekday() == 6:  # 6 is Sunday
            if d_str not in records_dict:
                records_dict[d_str] = {
                    'id': None,
                    'user_id': user_id,
                    'date': d_str,
                    'status': 'holiday',
                    'schedule_note': 'Sunday Holiday'
                }

    # Summary counters
    total_present = sum(1 for r in records_dict.values() if r.get('status') == 'present')
    total_absent = sum(1 for r in records_dict.values() if r.get('status') == 'absent')
    total_holiday = sum(1 for r in records_dict.values() if r.get('status') == 'holiday')
    total_half_day = sum(1 for r in records_dict.values() if r.get('status') == 'half_day')
    monthly_streak = calculate_streak(user_id, month, year, records_dict)

    return jsonify({
        'success': True,
        'records': records_dict,
        'counters': {
            'present': total_present,
            'absent': total_absent,
            'holiday': total_holiday,
            'half_day': total_half_day,
            'streak': monthly_streak
        }
    })

@attendance_bp.route('/api/update', methods=['POST'])
@login_required
def update_record():
    user_id = session['user_id']
    data = request.get_json() or {}

    date_str = data.get('date')
    status = data.get('status')
    schedule_note = data.get('schedule_note', '').strip()

    if not date_str or not status:
        return jsonify({'success': False, 'message': 'Date and Status are required.'}), 400

    if status not in ['present', 'absent', 'holiday', 'half_day']:
        return jsonify({'success': False, 'message': 'Invalid status.'}), 400

    # Rule check: Note is mandatory for leave (absent) and half_day
    if status in ['absent', 'half_day'] and not schedule_note:
        return jsonify({
            'success': False, 
            'message': f'Record note is strictly required for status: {status.replace("_", " ").title()}'
        }), 400

    record_date = datetime.strptime(date_str, '%Y-%m-%d').date()

    record = AttendanceRecord.query.filter_by(user_id=user_id, date=record_date).first()
    if record:
        record.status = status
        record.schedule_note = schedule_note
    else:
        record = AttendanceRecord(
            user_id=user_id,
            date=record_date,
            status=status,
            schedule_note=schedule_note
        )
        db.session.add(record)

    db.session.commit()

    return jsonify({'success': True, 'record': record.to_dict()})
