import os

from flask import request, abort, render_template, redirect, url_for, flash
from flask_login import current_user, login_required

from . import login_manager, csrf
from main import app

from models.user import UserModel
from models.health_status import HealthStatusModel
from models.doctor_feedback import DoctorFeedbackModel
from models.role import RoleModel
from models.user_role import UserRoleModel


@login_manager.user_loader
def load_user(user_id:int):
    return UserModel.query.get(int(user_id)) # Fetch the user from the database

# Doctor make conclusion & recommendation on user health
@app.route('/<int:health_status_id>/doctor/feedback/', methods=['GET', 'POST'])
@login_required
def doctor_feedback(health_status_id:int):
    if request.method == 'GET':
        feedback_records = DoctorFeedbackModel.fetch_by_health_status_id(health_status_id=health_status_id)
        return render_template('doctors_feedback.html', feedback_records=feedback_records)
    if request.method == 'POST':
        health_status = HealthStatusModel.fetch_by_id(id=health_status_id)
        user_roles = UserRoleModel.fetch_by_user_id(current_user.id)
        roles = user_roles.role.role
        if roles!= 'Doctor':
            flash('You are not authorised as a doctor!', 'danger')
            return redirect(url_for('doctor_feedback', health_status_id=health_status_id))
        conclusion = request.form['conclusion']
        recommendation = request.form['recommendation']
        doctor_id = current_user.id
        new_feedback = DoctorFeedbackModel(doctor_id=doctor_id,health_status_id=health_status_id,conclusion=conclusion, recommendation=recommendation)
        new_feedback.insert_record()
        return redirect(url_for('doctor_feedback', health_status_id=health_status_id))

# Doctor approve conclusion & recommendation on user health
@app.route('/doctor/feedback/<int:id>/vote', methods=['GET', 'POST'])
@login_required
def approve_doctor_feedback(id:int):
    if request.method == 'GET': # Get single Doctor feedback
        user_roles = UserRoleModel.fetch_by_user_id(current_user.id)
        roles = user_roles.role.role
        feedback_record = DoctorFeedbackModel.fetch_by_id(id=id)
        health_status_id = feedback_record.health_status_id
        if roles!= 'Doctor':
            flash('You are not authorised as a doctor!', 'danger')
            return redirect(url_for('doctor_feedback', health_status_id=health_status_id))
        feedback_record = DoctorFeedbackModel.count_vote(id=id)
        return redirect(url_for('doctor_feedback', health_status_id=health_status_id))