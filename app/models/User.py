from app.extensions import db, csrf
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(300), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    subscription_id = db.Column(db.Integer, db.ForeignKey('subscription_plans.plan_id'), nullable=True)
    affiliate_id = db.Column(db.Integer, db.ForeignKey('affiliates.affiliate_id'), nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    # Establish relationships with renders and medias
    renders = db.relationship('Render', backref='user_renders', lazy=True)
    medias = db.relationship('Media', backref='user_medias', lazy=True)
    @property
    def password(self):
        raise AttributeError('password is not a readable attribue!')
    
    @password.setter
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return '<Name %r>' % self.name



