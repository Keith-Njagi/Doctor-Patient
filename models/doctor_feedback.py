from datetime import datetime
from typing import List

from . import db

class DoctorFeedbackModel(db.Model):
    __tablename__ = 'doctors_feedback'
    id = db.Column(db.Integer, primary_key=True)

    doctor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    doctor = db.relationship('UserModel')

    health_status_id = db.Column(db.Integer, db.ForeignKey('health_statuses.id'), nullable=False)
    health_status = db.relationship('HealthStatusModel')

    conclusion = db.Column(db.Text, nullable=False)
    recommendation = db.Column(db.Text, nullable=False)
    vote = db.Column(db.Integer, nullable=False, default=0)

    created = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow(), nullable=True)

    user_feedback = db.relationship('UserFeedbackModel', lazy='dynamic')

    def insert_record(self) -> None:
        db.session.add(self)
        db.session.commit()

    @classmethod
    def fetch_all(cls) -> List['DoctorFeedbackModel']:
        return cls.query.order_by(cls.id.asc()).all()

    @classmethod
    def fetch_by_id(cls, id:int) -> 'DoctorFeedbackModel':
        return cls.query.get(id)

    @classmethod
    def fetch_by_health_status_id(cls, health_status_id:int) -> 'DoctorFeedbackModel':
        return cls.query.filter_by(health_status_id=health_status_id).all()
    
    @classmethod  
    def count_vote(cls, id:int) -> None:
        record = cls.fetch_by_id(id)

        record.vote = record.vote + 1
        db.session.commit()

    @classmethod  
    def update(cls, id:int, conclusion:str=None, recommendation:str=None) -> None:
        record = cls.fetch_by_id(id)

        if conclusion:
            record.conclusion = conclusion
        if recommendation:
            record.recommendation = recommendation
        db.session.commit()

    @classmethod
    def delete_by_id(cls, id:int) -> None:
        record = cls.query.filter_by(id=id)
        record.delete()
        db.session.commit()
