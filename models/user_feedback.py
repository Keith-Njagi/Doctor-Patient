from datetime import datetime
from typing import List

from . import db

class UserFeedbackModel(db.Model):
    __tablename__ = 'user_feedback'
    id = db.Column(db.Integer, primary_key=True)

    doctor_feedback_id = db.Column(db.Integer, db.ForeignKey('doctors_feedback.id'), nullable=False)
    doctor_feedback = db.relationship('DoctorFeedbackModel')

    feedback = db.Column(db.Text, nullable=False)

    created = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow(), nullable=True)

    def insert_record(self) -> None:
        db.session.add(self)
        db.session.commit()

    @classmethod
    def fetch_all(cls) -> List['UserFeedbackModel']:
        return cls.query.order_by(cls.id.asc()).all()

    @classmethod
    def fetch_by_id(cls, id:int) -> 'UserFeedbackModel':
        return cls.query.get(id)

    @classmethod
    def fetch_by_doctor_feedback_id(cls, doctor_feedback_id:int) -> 'UserFeedbackModel':
        return cls.query.filter_by(doctor_feedback_id=doctor_feedback_id).all()
