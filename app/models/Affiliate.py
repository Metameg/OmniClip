from app.extensions import db
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

class Affiliate(db.Model):
    __tablename__ = 'affiliates'
    
    affiliate_id = db.Column('affiliate_id', db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    addr1 = db.Column(db.String(150), nullable=False)
    addr2 = db.Column(db.String(50), nullable=True, default=None)
    city =  db.Column(db.String(150), nullable=False)
    state = db.Column(db.String(5), nullable=False)
    zip_code = db.Column(db.String(25), nullable=False)
    domain = db.Column(db.String(150), nullable=True, unique=True, default=None)
    telephone = db.Column(db.String(20), nullable=True, unique=True, default=None)
    business_type = db.Column(db.String(25), nullable=True, default=None)
    twitter = db.Column(db.String(150), nullable=True, default=None)
    fb = db.Column(db.String(150), nullable=True, default=None)
    instagram = db.Column(db.String(150), nullable=True, default=None)
    youtube = db.Column(db.String(150), nullable=True, default=None)
    tiktok = db.Column(db.String(150), nullable=True, default=None)
    twitch = db.Column(db.String(150), nullable=True, default=None)
    paypal = db.Column(db.String(150), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    key = db.Column('key', db.String(50), nullable=False)

    # Define the relationship with User
    user = relationship("User", backref="affiliate")