from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# Create extension instances without initializing
db = SQLAlchemy()
bcrypt = Bcrypt()

class Extensions:

    def init_extensions(self, app):
        db.init_app(app)
        bcrypt.init_app(app)

    @property
    def db(self):
        return db

    @property
    def bcrypt(self):
        return bcrypt