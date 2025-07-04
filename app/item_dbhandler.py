from datetime import datetime
import os
import uuid
from app.app_stub import Flask_App_Stub
from app.models.item import Item
from app.function import allowed_file
from abc import ABC, abstractmethod
from typing import List
from sqlalchemy import or_, and_
from flask import flash, redirect, url_for

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
                        category = category)
        self.db.session.add(new_item)
        self.db.session.commit()

    def item_to_display(self, current_user_id: int):
        return Item.query.filter(
                Item.user_id != current_user_id,
                Item.status == 'available',
                Item.approval != 'rejected',
                Item.approval != 'pending',
                Item.status != 'deleted',
                Item.status != 'swapping',
                Item.status != 'requested'
            )
    
    def query_item(self, item_id: str) -> Item:
        return Item.query.get_or_404(item_id)

    def set_item_status(self, item, status):
        item.status = status
        self.db.session.commit()

    def check_item_available(self, item):
        if item.status != 'available':
            flash('This item is no longer available for swap.', 'danger')
            return redirect(url_for('dashboard'))
        return True

    def get_available_items(self) -> List[Item]:
        """Get all available items ordered by timestamp (newest first)"""
        return Item.query.filter_by(approval='approved', status='available').order_by(Item.timestamp.desc()).all()
    
    def get_available_items_count(self) -> List[Item]:
        """Get number of available items ordered by timestamp (newest first)"""
        return Item.query.filter_by(approval='approved', status='available').count()
    
    def get_user_items(self, userId) -> List[Item]:
        """Get all available items ordered by timestamp (newest first)"""
        return Item.query.filter_by(user_id=userId).order_by(Item.timestamp.desc()).all()
    
    def get_pending_items(self) -> List[Item]:
        """Get all pending items ordered by timestamp (newest first)"""
        return Item.query.filter_by(approval='pending', status='available').order_by(Item.timestamp.desc()).all()
    
    def get_shared_item_count(self, userId) -> List[Item]:
        return Item.query.filter_by(user_id=userId, status='sold').count()
    
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
            os.makedirs('app/static/uploads', exist_ok=True)
            file.save(os.path.join('app/static/uploads', filename))
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
        # if(status == 'approved'):
        #     item.approval = 'approved'
        # elif (status == 'rejected'):
        #     item.approval = 'rejected'
        item.approval = status
        self.db.session.commit()

    def update_item_status(self, item, status) -> None:
        item.status = status
        #self.db.session.add(item)
        self.db.session.commit()

    def get_item_by_category(self, category) -> List[Item]:
        return Item.query.filter_by(status="available", approval='approved', category=category).order_by(Item.timestamp.desc()).all()
    
    def find_item(self, item_name: str, category: str, user_id: int) -> List[Item]:
        
        # Find specific item in specific categories
        if category != 'All' and item_name !='':
            return Item.query.filter(
                and_(
                    Item.status == "available",
                    Item.approval == "approved",
                    Item.category == category,
                    Item.name.ilike(f"%{item_name}%"),
                    Item.user_id != user_id
                )
            ).order_by(Item.timestamp.desc()).limit(10).all()

        # Find all items in specific category
        elif category !='All' and item_name == '':
            return Item.query.filter(
                and_(
                    Item.status == "available",
                    Item.approval == "approved",
                    Item.category == category,
                    Item.user_id != user_id
                )
            ).order_by(Item.timestamp.desc()).limit(10).all()
        
        # Find specific items in all categories
        elif category =='All' and item_name != '':
            return Item.query.filter(
                and_(
                    Item.status == "available",
                    Item.approval == "approved",
                    Item.name.ilike(f"%{item_name}%"),
                    Item.user_id != user_id
                )
            ).order_by(Item.timestamp.desc()).limit(10).all()
        
        # Find all items in all categories
        return Item.query.filter(
            and_(
                Item.status == "available",
                Item.approval == "approved",
                Item.user_id != user_id
            )
        ).order_by(Item.timestamp.desc()).limit(10).all()
