from datetime import datetime
from app.app_stub import Flask_App_Stub
from app.models.item import Item
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
    def add_new_item(self, name: str, description: str, price: float, image_filename: str, 
                     user_id: int, category: str) -> None: ...

    @abstractmethod
    def query_item(self, username: str): ...
    
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

class ItemRepository(DbHandler):
    def add_new_item(self, name: str, description: str, price: float, image_filename: str, 
                     user_id: int, category: str) -> None:
        new_item = Item(name = name, 
                        description = description, 
                        price = price, 
                        image_filename = image_filename, 
                        timestamp = datetime.utcnow(),
                        user_id = user_id,
                        category = category, 
                        status = 'available')
        self.db.session.add(new_item)
        print("Item added to database")
        self.db.session.commit()
        print("Commit successful")

    def query_item(self, name: str) -> Item:
        try:
            item = self.db.session.query(Item).filter_by(name=name).first()
            if item:
                return item
            else:
                return None
            
        except Exception as e:
            print(f"Error querying item: {e}")
            return None
    
    def reset_database(self) -> None:
        raise NotImplementedError("UserRepository does not implement reset_database")

class AdminDatabaseTools(DbHandler):
    def reset_database(self) -> None:
        try:
            self.db.drop_all()
            self.db.create_all()
            print("Database reset successfully")
        except Exception as e:
            print(f"Error resetting database: {e}")
    
    def add_new_item(self, name: str, description: str, price: float, image_filename: str, 
                     user_id: int, category: str) -> None:
        raise NotImplementedError("AdminDatabaseTools does not implement add_new_item")

    def query_item(self, name: str) -> Item | None:
        raise NotImplementedError("AdminDatabaseTools does not implement query_user")