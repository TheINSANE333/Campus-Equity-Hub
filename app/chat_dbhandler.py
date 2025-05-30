from datetime import datetime
from app.app_stub import Flask_App_Stub
from app.models.chat import Chat
from abc import ABC, abstractmethod
from typing import List
from flask import jsonify, render_template, request, flash, redirect, url_for, session

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

    @abstractmethod
    def get_unread_messages(self, current_user_id: int, user_id: int, last_id: int) -> List[Chat]: ...

    @abstractmethod
    def create_message(self, sender_id: int, receiver_id: int, message: str) -> Chat: ...

    @abstractmethod
    def mark_as_read(self, sender_id: int, receiver_id: int) -> None: ...

    def mark_as_read_sender(self, new_messages: List[Chat], current_user_id: int) -> None: ...

    @abstractmethod
    def get_all_message(self, sender_id: int, receiver_id: int) -> List[Chat]: ...

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
    
    def get_unread_messages(self, current_user_id: int, user_id: int, last_id: int) -> List[Chat]:
        return Chat.query.filter(
            Chat.id > last_id,
            ((Chat.sender_id == current_user_id) & (Chat.receiver_id == user_id)) |
            ((Chat.sender_id == user_id) & (Chat.receiver_id == current_user_id))
        ).order_by(Chat.timestamp).all()
    
    def create_message(self, sender_id: int, receiver_id: int, message: str) -> Chat:
            # Create new chat message
            new_message = Chat(
                sender_id=sender_id,
                receiver_id=receiver_id,
                message=message
            )
            
            self.db.session.add(new_message)
            self.db.session.commit()
            
            return new_message
            
    def mark_as_read(self, sender_id: int, receiver_id: int) -> None:
        unread_messages = Chat.query.filter_by(
            sender_id=sender_id,
            receiver_id=receiver_id,
            read=False
        ).all()
    
        for msg in unread_messages:
            msg.read = True
    
        self.db.session.commit()

    def mark_as_read_sender(self, new_messages: List[Chat], current_user_id: int) -> None:
        unread_messages = [msg for msg in new_messages if msg.receiver_id == current_user_id and not msg.read]
        for msg in unread_messages:
            msg.read = True
        
        self.db.session.commit()

    def get_all_message(self, sender_id: int, receiver_id: int) -> List[Chat]:
       return Chat.query.filter(
            ((Chat.sender_id == sender_id) & (Chat.receiver_id == receiver_id)) |
            ((Chat.sender_id == receiver_id) & (Chat.receiver_id == sender_id))
        ).order_by(Chat.timestamp).all()