from src import db, login, bcrypt, Config
from flask_login import UserMixin
from sqlalchemy import Enum, func

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password = db.Column(db.LargeBinary, nullable=False)
    username = db.Column(db.String(32), nullable=True)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def validate_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Memory(db.Model):
    __tablename__ = 'memories'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prompt = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    training_status = db.Column(Enum('active', 'inactive', 'completed'), nullable=False, default='active')
    recall_duration_days = db.Column(db.Integer, nullable=False, default=0)
    total_recall_count = db.Column(db.Integer, nullable=False, default=0)
    failed_recall_count = db.Column(db.Integer, nullable=False, default=0)
    partial_recall_count = db.Column(db.Integer, nullable=False, default=0)
    perfect_recall_count = db.Column(db.Integer, nullable=False, default=0)
    last_recall_outcome = db.Column(Enum('perfect', 'partial', 'failed'), nullable=True)
    next_recall_at = db.Column(db.DateTime(timezone=True), nullable=False, default=func.timezone('UTC', func.current_timestamp()))
    last_recall_at = db.Column(db.DateTime(timezone=True))
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=func.timezone('UTC', func.current_timestamp()))
    last_modified_at = db.Column(db.DateTime(timezone=True), nullable=False, default=func.timezone('UTC', func.current_timestamp()))

    user = db.relationship('User', backref='memories', lazy=True)

    @classmethod
    def get_all_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id = user_id).all()

    def serialize(self):
        return {
            "id": self.id,
            "prompt": self.prompt,
            "answer": self.answer,
            "user_id": self.user_id,
            "training_status": self.training_status,
            "recall_duration_days": self.recall_duration_days,
            "total_recall_count": self.total_recall_count,
            "failed_recall_count": self.failed_recall_count,
            "partial_recall_count": self.partial_recall_count,
            "perfect_recall_count": self.perfect_recall_count,
            "last_recall_outcome": self.last_recall_outcome,
            "next_recall_at": self.next_recall_at,
            "last_recall_at": self.last_recall_at,
            "created_at": self.created_at,
            "last_modified_at": self.last_modified_at
        }
    