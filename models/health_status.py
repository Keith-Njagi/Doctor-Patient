from datetime import datetime
from typing import List

from . import db

class HealthStatusModel(db.Model):
    __tablename__ = 'health_statuses'
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('UserModel')
    status = db.Column(db.Text, nullable=False)

    created = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow(), nullable=True)

    doctors_feedback = db.relationship('DoctorFeedbackModel', lazy='dynamic')

    def insert_record(self) -> None:
        db.session.add(self)
        db.session.commit()

    @classmethod
    def fetch_all(cls) -> List['HealthStatusModel']:
        return cls.query.order_by(cls.id.asc()).all()

    @classmethod
    def fetch_by_id(cls, id:int) -> 'HealthStatusModel':
        return cls.query.get(id)

    @classmethod
    def fetch_by_user_id(cls, user_id:int) -> 'HealthStatusModel':
        return cls.query.filter_by(user_id=user_id).all()
