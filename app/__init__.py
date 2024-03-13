import os
from dotenv import load_dotenv
from flask import Flask
from app.extensions import csrf, db, migrate
from app.views import tutorial, general, create_content, affiliate,quote_generator, media_uploader, login
from datetime import timedelta


def register_blueprints(app):
    app.register_blueprint(tutorial.blueprint, url_prefix='/user')
    app.register_blueprint(general.blueprint)
    app.register_blueprint(create_content.blueprint)
    app.register_blueprint(affiliate.blueprint, url_prefix='/affiliate-program')
    app.register_blueprint(quote_generator.blueprint, url_prefix='/quote-generator')
    app.register_blueprint(media_uploader.blueprint)
    app.register_blueprint(login.blueprint)

app = Flask(__name__, template_folder=os.path.join('..', 'frontend', 'src', 'templates'))
app.permanent_session_lifetime = timedelta(minutes=1)

load_dotenv()
mysql_pwd = os.getenv('MYSQL_PWD')
flask_key = os.getenv('FLASK_KEY')
# Config MySQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:' + mysql_pwd + '@localhost/omniclip_users'
# Config CSRF for form
app.config['SECRET_KEY'] = flask_key

csrf.init_app(app)
db.init_app(app)
migrate.init_app(app)

register_blueprints(app)
