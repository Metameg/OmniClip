from app import db
from datetime import datetime


class Users(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(10), nullable=False, unique=True)
    subscription_id = db.Column(db.Integer, nullable=True)
    affiliate_id = db.Column(db.Integer, nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<Name %r>' % self.name



