import os
from dotenv import load_dotenv
from flask import Flask
from app.extensions import csrf, db, migrate
from datetime import timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Affiliate, SubscriptionPlan, User, Render, Media  

def create_app():
    app = Flask(__name__, static_folder=('static'), template_folder=('templates'))
    # Set session length time
    app.permanent_session_lifetime = timedelta(days=2)

    load_dotenv()
    mysql_pwd = os.getenv('MYSQL_PWD')
    flask_key = os.getenv('FLASK_KEY')
    # Config MySQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:' + mysql_pwd + '@localhost/omniclip_users_dev'
    # Config CSRF for form
    app.config['SECRET_KEY'] = flask_key

    csrf.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    
    # from app.models import Affiliate, SubscriptionPlan, User, Render, Media  # Import your model classes
    # migrate = Migrate(app, db)


    register_blueprints(app)

    return app

def register_blueprints(app):
    from app.views import general, create_content, affiliate,quote_generator, media_uploader, login
    
    app.register_blueprint(general.blueprint)
    app.register_blueprint(create_content.blueprint)
    app.register_blueprint(affiliate.blueprint, url_prefix='/affiliate-program')
    app.register_blueprint(quote_generator.blueprint, url_prefix='/quote-generator')
    app.register_blueprint(media_uploader.blueprint)
    app.register_blueprint(login.blueprint)

def create_db_session():
    load_dotenv()
    mysql_pwd = os.getenv('MYSQL_PWD')
    db_connection_string = 'mysql+pymysql://root:' + mysql_pwd + '@localhost/omniclip_users_dev'
    # Create the SQLAlchemy engine
    engine = create_engine(db_connection_string)

    # Create a sessionmaker bound to the engine
    Session = sessionmaker(bind=engine)

    return Session()
