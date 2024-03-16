from app.extensions import db
from datetime import datetime, timezone

class Render(db.Model):
    __tablename__ = 'renders'
    
    render_id = db.Column('render_id', db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False)
    timestamp = db.Column('timestamp',db.DateTime, default=datetime.now(timezone.utc))
    duration = db.Column('duration', db.Integer, nullable=False)
    aspect_ratio = db.Column('aspect_ratio', db.String(20), nullable=False)
    filename = db.Column('filename', db.String(100), nullable=False)