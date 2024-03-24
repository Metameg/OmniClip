from app.extensions import db
from datetime import datetime, timezone

class Media(db.Model):
    __tablename__ = 'medias'
    
    media_id = db.Column('media_id', db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False)
    path = db.Column('path', db.String(255), unique=True, nullable=False)
    filename = db.Column('filename', db.String(128), nullable=False)
    timestamp = db.Column('timestamp',db.DateTime, default=datetime.now(timezone.utc))
    duration = db.Column('duration', db.String(50), nullable=True)
    resolution = db.Column('resolution', db.String(25), nullable=True)
    size = db.Column('size', db.Integer, nullable=True)

    