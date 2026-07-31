from flask import Blueprint, render_template, jsonify, session, request
from models import db, AttendanceRecord, User
from routes.attendance import login_required
from datetime import datetime
import calendar

progress_bp = Blueprint('progress', __name__, url_prefix='/progress')

@progress_bp.route('/')
@login_required
def progress_view():
    user_id = session['user_id']
    user = User.query.get(user_id)
    return render_template('progress.html', user=user)

@progress_bp.route('/api/stats')
@login_required
def get_stats():
    user_id = session['user_id']
    now = datetime.now()
    
    # Target month and year (defaults to current real-time month and year)
    end_year = request.args.get('year', now.year, type=int)
    end_month = request.args.get('month', now.month, type=int)

    # Generate last 6 months dynamically ending at target month
    month_list = []
    curr_y = end_year
    curr_m = end_month

    for _ in range(6):
        month_list.append((curr_y, curr_m))
        curr_m -= 1
        if curr_m < 1:
            curr_m = 12
            curr_y -= 1

    month_list.reverse() # Chronological order

    chart_data = {
        'labels': [],
        'present': [],
        'absent': [],
        'half_day': []
    }

    total_all_present = 0
    total_all_absent = 0
    total_all_half_day = 0
    total_all_records = 0

    for y, m in month_list:
        m_name = calendar.month_name[m][:3]
        chart_data['labels'].append(f"{m_name}")

        records = AttendanceRecord.query.filter(
            AttendanceRecord.user_id == user_id,
            db.extract('year', AttendanceRecord.date) == y,
            db.extract('month', AttendanceRecord.date) == m
        ).all()

        p = sum(1 for r in records if r.status == 'present')
        a = sum(1 for r in records if r.status == 'absent')
        h = sum(1 for r in records if r.status == 'half_day')

        chart_data['present'].append(p)
        chart_data['absent'].append(a)
        chart_data['half_day'].append(h)

        total_all_present += p
        total_all_absent += a
        total_all_half_day += h
        total_all_records += len(records)

    # Calculate exact real-time metrics
    if total_all_records > 0:
        present_pct = round((total_all_present / total_all_records) * 100, 1)
        absent_pct = round((total_all_absent / total_all_records) * 100, 1)
        half_day_pct = round((total_all_half_day / total_all_records) * 100, 1)
        overall_performance = round(((total_all_present + (0.5 * total_all_half_day)) / total_all_records) * 100, 1)
    else:
        present_pct, absent_pct, half_day_pct, overall_performance = 0.0, 0.0, 0.0, 0.0

    return jsonify({
        'success': True,
        'chart_data': chart_data,
        'metrics': {
            'present_pct': present_pct,
            'absent_pct': absent_pct,
            'half_day_pct': half_day_pct,
            'overall_performance': overall_performance,
            'total_recorded_days': total_all_records
        }
    })
