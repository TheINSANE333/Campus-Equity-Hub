from app.app_stub import Flask_App_Stub
from app.models.user import User

class DbHandler:
    def __init__(self, app: Flask_App_Stub) -> None:
        self.flask_app = app
        self.db = app.db
        self.bcrypt = app.bcrypt

    def add_new_user(self, username: str, email: str, password: str) -> None:
        hashed_password = self.bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password=hashed_password)
        self.db.session.add(new_user)
        print("User added to session")
        self.db.session.commit()
        print("Commit successful")

    def query_user(self, username: str) -> str:
        try:
            user = self.db.session.query(User).filter_by(username=username).first()
            if user:
                return user
            else:
                return None
            
        except Exception as e:
            print(f"Error querying user: {e}")
            return None
        
    def query_email(self, email_inp: str) -> str:
        try:
            email_inp = self.db.session.query(User).filter_by(email=email_inp).first()
            if email_inp:
                print(email_inp)
                return email_inp.email
            else:
                return None
            
        except Exception as e:
            print(f"Error querying user: {e}")
            return None
            
    def check_password(self, username: str, password: str) -> bool:
        try:
            user = self.db.session.query(User).filter_by(username=username).first()
            return self.bcrypt.check_password_hash(user.password, password)
            
        except Exception as e:
            print(f"Error: {e}")
            return False
        
    def reset_database(self) -> None:
        try:
            self.db.drop_all()
            self.db.create_all()
            print("Database reset successfully")
        except Exception as e:
            print(f"Error resetting database: {e}")