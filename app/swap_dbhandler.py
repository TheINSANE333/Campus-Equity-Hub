from app.app_stub import Flask_App_Stub
from app.models.item import Item
from abc import ABC, abstractmethod
from app.models.swap import Swap
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

class SwapRepository(DbHandler):
    def query_swap(self, swap_id: str) -> Swap:
        return Swap.query.get_or_404(swap_id)
    
    # Update swap status after a swap is done or rejected
    def update_swap_status(self, swap, status) -> None:
        swap.status = status
        self.db.session.add(swap)
        self.db.session.commit()

    def update_location(self, swap, location):
        swap.dealLocation = location
        self.db.session.add(swap)
        self.db.session.commit()

    def update_time(self, swap, time):
        swap.dealTime = time
        self.db.session.add(swap)
        self.db.session.commit()

    def get_swap_completed_count(self, user_id) -> List[Item]:
        """Get number of available items ordered by timestamp (newest first)"""
        return Swap.query.join(Item, Swap.item_id == Item.id).filter(self.db.or_(
            self.db.and_(Swap.user_id==user_id, Swap.status=='accepted'),
            self.db.and_(Item.user_id==user_id, Swap.status=='accepted')
        )).count()
        
