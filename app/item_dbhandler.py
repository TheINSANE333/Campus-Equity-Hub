from datetime import datetime
import os
import uuid
from app.app_stub import Flask_App_Stub
from app.models.item import Item
from app.function import allowed_file
from abc import ABC, abstractmethod
from typing import List

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
    def query_item(self, item_id: str) -> Item: ...

    @abstractmethod
    def get_available_items(self) -> List[Item]: ...

    # @abstractmethod
    # def get_item_by_cateogory(self, category: str) -> List[Item]: ...
    
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
    UPLOAD_FOLDER = 'app/static/uploads'
    def add_new_item(self, name: str, description: str, price: float, image_filename: str, 
                     user_id: int, category: str) -> None:
        new_item = Item(name = name, 
                        description = description, 
                        price = price, 
                        image_filename = image_filename, 
                        timestamp = datetime.utcnow(),
                        user_id = user_id,
                        category = category, 
                        status = 'pending')  # pending status for admin approval
        self.db.session.add(new_item)
        print("Item added to database")
        self.db.session.commit()
        print("Commit successful")

    def query_item(self, item_id: str) -> Item:
        return Item.query.get_or_404(item_id)

    def get_available_items(self) -> List[Item]:
        """Get all available items ordered by timestamp (newest first)"""
        return Item.query.filter_by(status='available').order_by(Item.timestamp.desc()).all()
    
    def get_pending_items(self) -> List[Item]:
        """Get all pending items ordered by timestamp (newest first)"""
        return Item.query.filter_by(status='pending').order_by(Item.timestamp.desc()).all()
    
    def upload_image(self, item, file) -> None:
        # Handle image upload
        file = file
        if file and file.filename != '' and allowed_file(file.filename):
            # Remove old image if exists
            if item.image_filename:
                try:
                    old_image_path = os.path.join(self.app.config['UPLOAD_FOLDER'], item.image_filename)
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)
                except Exception as e:
                    print(f"Error removing old image: {e}")
            
            # Generate unique filename
            filename = str(uuid.uuid4()) + '.' + file.filename.rsplit('.', 1)[1].lower()
            file.save(os.path.join(self.app.config['UPLOAD_FOLDER'], filename))
            item.image_filename = filename
    
            self.db.session.commit()

    def edit_item(self, item, name, description, price, category, status) -> None:
        item.name = name
        item.description = description
        item.price = price
        item.category = category
        item.status = status
        self.db.session.commit()

    def update_status(self, item, status) -> None:
        if(status == 'approved'):
            item.status = 'available'
        elif (status == 'rejected'):
            item.status = 'rejected'
        self.db.session.commit()

    def get_item_by_category(self, category) -> List[Item]:
        return Item.query.filter_by(category=category).order_by(Item.timestamp.desc()).all()
