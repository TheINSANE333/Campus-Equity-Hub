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

class NotificationRepository(DbHandler):

    def create_notification(self, receiver_id: int, sender_id: int, message: str, notification_type: str, status: str, title: str = None) -> None:

        new_notification = Notification(
            receiver_id=receiver_id,
            sender_id=sender_id,
            message=message,
            notification_type=notification_type,
            timestamp=datetime.now(),
            title=title,
            status=status
        )
        
        self.db.session.add(new_notification)
        self.db.session.commit()
    
    def get_user_notifications(self, user_id: int) -> List[Notification]:
        """Get all notifications for a specific user ordered by timestamp (newest first)"""
        return Notification.query.filter_by(receiver_id=user_id).order_by(Notification.timestamp.desc()).all()
    
    def get_unread_notifications(self, user_id: int) -> List[Notification]:
        """Get unread notifications for a specific user"""
        return Notification.query.filter_by(receiver_id=user_id, status='unread').order_by(Notification.timestamp.desc()).all()
    
    def count_unread_notifications(self, user_id: int) -> int:
        """Count unread notifications for a specific user"""
        return Notification.query.filter_by(receiver_id=user_id, status='unread').count()
    
    def mark_as_read(self, notification_id: int) -> None:
        """Mark a specific notification as read"""
        notification = Notification.query.get_or_404(notification_id)
        notification.status = 'read'
        #self.db.session.add(notification)
        self.db.session.commit()
    
    def mark_all_as_read(self, user_id: int) -> None:
        """Mark all notifications for a user as read"""
        notifications = Notification.query.filter_by(receiver_id=user_id, status='unread').all()
        for notification in notifications:
            notification.status = 'read'
        #self.db.session.add_all(notifications)
        self.db.session.commit()
    
    def set_notification_status_to_delete(self, notification_id: int) -> None:
        """Set a specific notification to deleted status to prevent data lost"""
        notification = Notification.query.get_or_404(notification_id)
        notification.status = 'deleted'
        #self.db.session.add(notification)
        self.db.session.commit()

    def set_all_notification_status_to_delete(self, user_id: int) -> None:
        """Set all notifications for a user to deleted status"""
        notifications = Notification.query.filter_by(receiver_id=user_id).all()
        for notification in notifications:
            notification.status = 'deleted'
        #self.db.session.add_all(notifications)
        self.db.session.commit()