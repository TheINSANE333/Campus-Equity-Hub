from app.extensions import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(128), nullable=False, default="student")
    campus = db.Column(db.String(120), nullable=False)
    token = db.Column(db.Integer, nullable=False, default=0)

    print("User model created")

    def __repr__(self):
        return f'<User {self.username}>'
    
