from flask import Blueprint, render_template, request, jsonify, session
from models import db, Assignment, User
from datetime import datetime
from routes.attendance import login_required

assignments_bp = Blueprint('assignments', __name__, url_prefix='/assignments')

@assignments_bp.route('/')
@login_required
def assignments_view():
    user_id = session['user_id']
    user = User.query.get(user_id)
    return render_template('assignments.html', user=user)

@assignments_bp.route('/api/list')
@login_required
def get_assignments():
    user_id = session['user_id']
    assignments = Assignment.query.filter_by(user_id=user_id).order_by(Assignment.id.desc()).all()
    return jsonify({
        'success': True,
        'assignments': [a.to_dict() for a in assignments]
    })

@assignments_bp.route('/api/add', methods=['POST'])
@login_required
def add_assignment():
    user_id = session['user_id']
    data = request.get_json() or {}

    title = data.get('title', '').strip()
    due_date_str = data.get('due_date')
    status = data.get('status', 'pending')

    if not title:
        return jsonify({'success': False, 'message': 'Assignment title is required.'}), 400

    due_date = None
    if due_date_str:
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()

    assignment = Assignment(
        user_id=user_id,
        title=title,
        status=status,
        due_date=due_date
    )
    db.session.add(assignment)
    db.session.commit()

    return jsonify({'success': True, 'assignment': assignment.to_dict()})

@assignments_bp.route('/api/toggle/<int:a_id>', methods=['POST'])
@login_required
def toggle_status(a_id):
    user_id = session['user_id']
    assignment = Assignment.query.filter_by(id=a_id, user_id=user_id).first()
    
    if not assignment:
        return jsonify({'success': False, 'message': 'Assignment not found.'}), 404

    # Toggle status cycle: pending -> in_progress -> completed -> pending
    if assignment.status == 'pending':
        assignment.status = 'in_progress'
    elif assignment.status == 'in_progress':
        assignment.status = 'completed'
    else:
        assignment.status = 'pending'

    db.session.commit()
    return jsonify({'success': True, 'assignment': assignment.to_dict()})

@assignments_bp.route('/api/delete/<int:a_id>', methods=['POST'])
@login_required
def delete_assignment(a_id):
    user_id = session['user_id']
    assignment = Assignment.query.filter_by(id=a_id, user_id=user_id).first()

    if not assignment:
        return jsonify({'success': False, 'message': 'Assignment not found.'}), 404

    db.session.delete(assignment)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Assignment deleted.'})
