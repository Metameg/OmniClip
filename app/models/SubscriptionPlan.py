from app.extensions import db
from sqlalchemy.orm import relationship

class SubscriptionPlan(db.Model):
    __tablename__ = 'subscription_plans'
    
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    paypal_plan_id = db.Column('paypal_plan_id', db.String(50), nullable=False)
    plan_name = db.Column('plan_name', db.String(128), nullable=False)
    description = db.Column('description', db.String(512), nullable=True)

    # Define the relationship with User
    user = relationship("User", backref="subscription_plans")