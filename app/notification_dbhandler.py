from app.app_stub import Flask_App_Stub
from app.models.notification import Notification
from abc import ABC, abstractmethod
from typing import List
from datetime import datetime

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
        self._initialized = True

    @abstractmethod
    def create_notification(self, receiver_id: int, sender_id: int, message: str, notification_type: str, title: str = None) -> None: ...

    @abstractmethod
    def get_user_notifications(self, user_id: int) -> List[Notification]: ...

    @abstractmethod
    def mark_as_read(self, notification_id: int) -> None: ...

    @abstractmethod
    def delete_notification(self, notification_id: int) -> None: ...

    @classmethod
    def get_instance(cls, app: Flask_App_Stub = None):
        """
        Get the singleton instance of the DbHandler.
        Provide app parameter only on first call.
        """
        if cls._instance is None:
            return cls(app)
        return cls._instance

class NotificationRepository(DbHandler):
    def create_notification(self, receiver_id: int, sender_id: int, message: str, notification_type: str, title: str = None) -> None:
        """
        Create a new notification for a user
        
        Parameters:
        receiver_id (int): The ID of the user to receive the notification
        sender_id (int): The ID of the user sending the notification
        message (str): The notification message
        notification_type (str): Type of notification (e.g., 'item', 'application', 'system')
        title (str, optional): Title of the notification
        """
        new_notification = Notification(
            receiver_id=receiver_id,
            sender_id=sender_id,
            message=message,
            notification_type=notification_type,
            read=False,
            timestamp=datetime.utcnow(),
            title=title
        )
        
        self.db.session.add(new_notification)
        self.db.session.commit()
    
    def get_user_notifications(self, user_id: int) -> List[Notification]:
        """Get all notifications for a specific user ordered by timestamp (newest first)"""
        return Notification.query.filter_by(receiver_id=user_id).order_by(Notification.timestamp.desc()).all()
    
    def get_unread_notifications(self, user_id: int) -> List[Notification]:
        """Get unread notifications for a specific user"""
        return Notification.query.filter_by(receiver_id=user_id, read=False).order_by(Notification.timestamp.desc()).all()
    
    def count_unread_notifications(self, user_id: int) -> int:
        """Count unread notifications for a specific user"""
        return Notification.query.filter_by(receiver_id=user_id, read=False).count()
    
    def mark_as_read(self, notification_id: int) -> None:
        """Mark a specific notification as read"""
        notification = Notification.query.get_or_404(notification_id)
        notification.read = True
        self.db.session.commit()
    
    def mark_all_as_read(self, user_id: int) -> None:
        """Mark all notifications for a user as read"""
        notifications = Notification.query.filter_by(receiver_id=user_id, read=False).all()
        for notification in notifications:
            notification.read = True
        self.db.session.commit()
    
    def delete_notification(self, notification_id: int) -> None:
        """Delete a specific notification"""
        notification = Notification.query.get_or_404(notification_id)
        self.db.session.delete(notification)
        self.db.session.commit()
    
    def delete_all_notifications(self, user_id: int) -> None:
        """Delete all notifications for a user"""
        notifications = Notification.query.filter_by(receiver_id=user_id).all()
        for notification in notifications:
            self.db.session.delete(notification)
        self.db.session.commit()
    
    def get_notification_by_id(self, notification_id: int) -> Notification:
        """Get a specific notification by ID"""
        return Notification.query.get_or_404(notification_id)
