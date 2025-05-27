from app.app_stub import Flask_App_Stub
from app.models.user import User
from abc import ABC, abstractmethod

class DbHandler(ABC):
    _instance = None
    
    def __new__(cls, app: Flask_App_Stub = None):
        if cls._instance is None:
            if app is None:
                raise ValueError("App must be provided when initializing DbHandler for the first time")
            cls._instance = super(DbHandler, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, app: Flask_App_Stub) -> None:
        if self._initialized:
            return
            
        if app is None:
            raise ValueError("App must be provided when initializing DbHandler for the first time")
        
        self.flask_app = app
        self.db = app.db
        self.bcrypt = app.bcrypt

    @abstractmethod
    def add_new_user(self, username: str, email: str, password: str) -> None: ...

    @abstractmethod
    def query_user(self, username: str): ...

    @abstractmethod
    def query_email(self, email: str): ...
    
    @abstractmethod
    def check_password(self, username: str, password: str) -> bool: ...
    
    @abstractmethod
    def reset_database(self) -> None: ...

    @classmethod
    def get_instance(cls, app: Flask_App_Stub = None):
        """
        Get the singleton instance of the DbHandler.
        Provide app parameter only on first call.
        """
        if cls._instance is None:
            return cls(app)
        return cls._instance

class UserRepository(DbHandler):
    def add_new_user(self, username: str, email: str, password: str) -> None:
        hashed_password = self.bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password=hashed_password)
        self.db.session.add(new_user)
        print("User added to session")
        self.db.session.commit()
        print("Commit successful")

    def query_user(self, username: str) -> User:
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
        raise NotImplementedError("UserRepository does not implement check_password")
    
    def reset_database(self) -> None:
        raise NotImplementedError("UserRepository does not implement reset_database")

class Authenticator(DbHandler):
    def check_password(self, username: str, password: str) -> bool:
        try:
            user = self.db.session.query(User).filter_by(username=username).first()
            return self.bcrypt.check_password_hash(user.password, password)
            
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    def add_new_user(self, username: str, email: str, password: str) -> None:
        raise NotImplementedError("Authenticator does not implement add_new_user")

    def query_user(self, username: str) -> User | None:
        raise NotImplementedError("Authenticator does not implement query_user")

    def query_email(self, email: str) -> str | None:
        raise NotImplementedError("Authenticator does not implement query_email")
    
    def reset_database(self) -> None:
        raise NotImplementedError("Authenticator does not implement reset_database")

class AdminDatabaseTools(DbHandler):
    def reset_database(self) -> None:
        try:
            self.db.drop_all()
            self.db.create_all()
            print("Database reset successfully")
        except Exception as e:
            print(f"Error resetting database: {e}")
    
    def add_new_user(self, username: str, email: str, password: str) -> None:
        raise NotImplementedError("AdminDatabaseTools does not implement add_new_user")

    def query_user(self, username: str) -> User | None:
        raise NotImplementedError("AdminDatabaseTools does not implement query_user")

    def query_email(self, email: str) -> str | None:
        raise NotImplementedError("AdminDatabaseTools does not implement query_email")
    
    def check_password(self, username: str, password: str) -> bool:
        raise NotImplementedError("AdminDatabaseTools does not implement check_password")