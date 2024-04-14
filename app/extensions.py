from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
# from flask_jwt_extended import JWTManager

csrf = CSRFProtect()
db = SQLAlchemy()
migrate = Migrate()
# jwt = JWTManager()
