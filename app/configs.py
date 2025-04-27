import os

class Config:
    def __init__(self):
        self.sqlalchemy_track_modifications = False

    def apply_config(self, app):
        app.config['SECRET_KEY'] = os.urandom(24)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.permanent_session_lifetime = 1800