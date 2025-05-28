from datetime import datetime
from app.app_stub import Flask_App_Stub
from app.models.chat import Chat
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
    def get_unread_counts(self) -> List[Chat]: ...

    @classmethod
    def get_instance(cls, app: Flask_App_Stub = None):
        """
        Get the singleton instance of the DbHandler.
        Provide app parameter only on first call.
        """
        if cls._instance is None:
            return cls(app)
        return cls._instance

class ChatRepository(DbHandler):
    def get_unread_counts(self, user_id: int) -> List[Chat]:
        unread_counts = self.db.session.query(
            Chat.sender_id, 
            self.db.func.count(Chat.id).label('count')
        ).filter(
            Chat.receiver_id == user_id,
            Chat.read == False
        ).group_by(Chat.sender_id).all()

        return unread_counts