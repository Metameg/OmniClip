import os
from dotenv import load_dotenv
from flask import Flask
from app.extensions import csrf, db, migrate, jwt
from datetime import datetime, timedelta, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
# Needed for sqlalchemy mappings
from app.models import Affiliate, SubscriptionPlan, User, Render, Media  

def create_app():
    app = Flask(__name__, static_folder=('static'), template_folder=('templates'))
    CORS(app, origins=["https://www.paypal.com", "https://www.sandbox.paypal.com"])
    # Set session length time
    app.permanent_session_lifetime = timedelta(hours=24)
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

    load_dotenv()
    mysql_pwd = os.getenv('MYSQL_PWD')
    flask_key = os.getenv('FLASK_KEY')
    jwt_secret = os.getenv('JWT_SECRET_KEY')
    # Config MySQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:' + mysql_pwd + '@localhost/omniclip_users_dev'
    # Config CSRF for form
    app.config['SECRET_KEY'] = flask_key
    app.config['JWT_SECRET_KEY'] = jwt_secret
    
    csrf.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Start scheduler for removing old render records
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=delete_old_records, args=[app], trigger="interval", days=1)
    scheduler.start()

    register_blueprints(app)

    return app

def register_blueprints(app):
    from app.views import general, create_content, affiliate, quote_generator, media_uploader, login, subscriptions, payments, profile
    
    app.register_blueprint(general.blueprint)
    app.register_blueprint(create_content.blueprint)
    # app.register_blueprint(affiliate.blueprint, url_prefix='/affiliate-program')
    app.register_blueprint(quote_generator.blueprint, url_prefix='/quote-generator')
    app.register_blueprint(media_uploader.blueprint)
    app.register_blueprint(login.blueprint)
    app.register_blueprint(profile.blueprint, url_prefix='/profile')
    # app.register_blueprint(subscriptions.blueprint)
    # app.register_blueprint(payments.blueprint, url_prefix='/payments')

def delete_old_records(app):
    with app.app_context():
        threshold_date = datetime.now() - timedelta(days=14)
        try:
            old_records = Render.Render.query.filter(Render.Render.timestamp < threshold_date).all()
            for record in old_records:
                db.session.delete(record)
            db.session.commit()

        except Exception as e:
            print("Error querying old records:", e)
        
        

# def create_db_session():
#     load_dotenv()
#     mysql_pwd = os.getenv('MYSQL_PWD')
#     db_connection_string = 'mysql+pymysql://root:' + mysql_pwd + '@localhost/omniclip_users_dev'
#     # Create the SQLAlchemy engine
#     engine = create_engine(db_connection_string)

#     # Create a sessionmaker bound to the engine
#     Session = sessionmaker(bind=engine)

#     return Session()
