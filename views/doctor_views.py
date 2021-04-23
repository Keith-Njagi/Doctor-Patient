import os

from flask import request, abort, render_template, redirect, url_for, flash
from flask_login import current_user, login_required

from . import login_manager, csrf
from main import app

from models.user import UserModel
from models.health_status import HealthStatusModel
from models.doctor_feedback import DoctorFeedbackModel


@login_manager.user_loader
def load_user(user_id:int):
    return UserModel.get(int(user_id)) # Fetch the user from the database

# Doctor make conclusion & recommendation on user health
@app.route('/<int:health_status_id>/doctor/feedback/', methods=['GET', 'POST'])
@login_required
def doctor_feedback(health_status_id:int):
    if request.method == 'GET':
        feedback_records = DoctorFeedbackModel.fetch_by_health_status_id(health_status_id=health_status_id)
        return render_template('doctors_feedback.html', feedback_records=feedback_records)
    if request.method == 'POST':
        return render_template('doctors_feedback.html')

# Doctor approve conclusion & recommendation on user health
@app.route('/doctor/feedback/<int:id>/vote', methods=['GET', 'POST'])
@login_required
def approve_doctor_feedback(id:int):
    if request.method == 'GET': # Get single Doctor feedback
        feedback_record = DoctorFeedbackModel.count_vote(id=id)
        feedback_records = DoctorFeedbackModel.fetch_by_health_status_id(health_status_id=feedback_record.health_status_id)
        return render_template('doctors_feedback.html', feedback_records=feedback_records)
