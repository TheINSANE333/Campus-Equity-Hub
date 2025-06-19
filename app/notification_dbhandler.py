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

    def create_notification(self, receiver_id: int, sender_id: int, sender_name: str,message: str, notification_type: str, status: str, role_to_be_view: str, title: str = None) -> None:

        new_notification = Notification(
            receiver_id=receiver_id,
            sender_id=sender_id,
            message=message,
            notification_type=notification_type,
            timestamp=datetime.now(),
            title=title,
            status=status,
            role_to_be_view=role_to_be_view,
            sender_name=sender_name
        )

        self.db.session.add(new_notification)
        self.db.session.commit()


    def get_user_notifications(self, user_id: int, role_to_be_view: str) -> List[Notification]:
        """Get all non-deleted notifications for a specific user and role ordered by timestamp (newest first)"""
        if role_to_be_view == 'admin':
            # For admin, show all notifications meant for admins (role_to_be_view = 'admin')
            return Notification.query.filter_by(
                role_to_be_view='admin'
            ).filter(
                Notification.status != 'deleted'
            ).order_by(Notification.timestamp.desc()).all()
        else:
            # For students, show only notifications meant for them specifically
            return Notification.query.filter_by(
                receiver_id=user_id,
                role_to_be_view=role_to_be_view
            ).filter(
                Notification.status != 'deleted'
            ).order_by(Notification.timestamp.desc()).all()

    def count_unread_notifications(self, user_id: int, role_to_be_view: str) -> int:
        """Count unread notifications for a specific user and role"""
        if role_to_be_view == 'admin':
            # For admin, count all unread notifications meant for admins
            return Notification.query.filter_by(
                role_to_be_view='admin',
                status='unread'
            ).count()
        else:
            return Notification.query.filter_by(
                receiver_id=user_id,
                status='unread',
            ).count()

    def set_notification_status_to_delete(self, notification_id: int) -> None:
        """Set a specific notification to deleted status to prevent data lost"""
        notification = Notification.query.get_or_404(notification_id)
        notification.status = 'deleted'
        self.db.session.commit()

    def set_all_notification_status_to_delete(self, user_id: int, role_to_be_view: str) -> None:
        """Set all notifications for a user and role to deleted status"""
        if role_to_be_view == 'admin':
            # For admin, update all admin notifications
            notifications = Notification.query.filter_by(
                role_to_be_view='admin'
            ).filter(
                Notification.status != 'deleted'
            ).all()
        else:
            # For other roles, update only their specific notifications
            notifications = Notification.query.filter_by(
                receiver_id=user_id,
                role_to_be_view=role_to_be_view
            ).filter(
                Notification.status != 'deleted'
            ).all()

        for notification in notifications:
            notification.status = 'deleted'

        self.db.session.commit()