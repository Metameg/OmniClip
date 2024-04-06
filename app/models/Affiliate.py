from app.extensions import db
from sqlalchemy.orm import relationship

class Affiliate(db.Model):
    __tablename__ = 'affiliates'
    
    affiliate_id = db.Column('affiliate_id', db.Integer, primary_key=True, autoincrement=True)
    key = db.Column('key', db.String(50), nullable=False)

    # Define the relationship with User
    user = relationship("User", backref="affiliate")