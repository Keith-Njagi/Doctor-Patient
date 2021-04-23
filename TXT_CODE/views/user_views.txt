import os

from flask import request, abort, render_template, redirect, url_for, flash
from flask_login import current_user, login_required

from . import login_manager #, csrf
from main import app

from models.user import UserModel
from models.health_status import HealthStatusModel
from models.user_feedback import UserFeedbackModel
from models.doctor_feedback import DoctorFeedbackModel

@login_manager.user_loader
def load_user(user_id:int):
    return UserModel.query.get(int(user_id)) # Fetch the user from the database

@app.route('/')
def index():
    users = UserModel.fetch_all()
    return render_template('index.html', users=users, current_user=current_user)

# User update health status 
@app.route('/user/<int:id>', methods=['GET', 'POST'])
@login_required
def health_status(id):
    if request.method == 'GET':
        health_statuses = HealthStatusModel.fetch_by_user_id(user_id=id)
        return render_template('health_status.html', health_statuses=health_statuses)
    if request.method == 'POST':
        status = request.form['status']
        user_id = current_user.id
        new_status = HealthStatusModel(status=status, user_id=user_id)
        new_status.insert_record()
        return redirect(url_for('health_status', id=user_id))

# give feedback on diagnosis
@app.route('/doctor/<int:doctor_feedback_id>/user-feedback', methods=['GET', 'POST'])
@login_required
def user_feedback(doctor_feedback_id):
    if request.method == 'GET':
        doctor_feedback = DoctorFeedbackModel.fetch_by_id(id=doctor_feedback_id)
        user_feedbacks = doctor_feedback.user_feedback
        return render_template('user_feedback.html', user_feedbacks=user_feedbacks)
    if request.method == 'POST':
        feedback = request.form['user_feedback']
        new_feedback = UserFeedbackModel(doctor_feedback_id=doctor_feedback_id,feedback=feedback)
        new_feedback.insert_record()
        return redirect(url_for('user_feedback', doctor_feedback_id=doctor_feedback_id))

