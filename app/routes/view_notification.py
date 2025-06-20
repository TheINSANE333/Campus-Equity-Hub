from flask import render_template, flash, redirect, url_for, session
from app.app_stub import Flask_App_Stub
from app.routes.endpoint import Endpoint
from app.notification_dbhandler import NotificationRepository

class ViewNotification(Endpoint):
    def __init__(self, app: Flask_App_Stub) -> None:
        super().__init__(app)

        self.route = '/notifications'
        self.endpoint = 'view_notification'
        self.callback = self.view_notification_page
        self.methods = ['GET']

    def view_notification_page(self):
        user_id = session.get('user_id')
        role = session.get('role', 'student')

        if 'user_id' not in session:
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('login'))

        notification_dbHandler = NotificationRepository(self.flask_app)
        # Get all notifications for the user and role, not just unread ones
        notifications = notification_dbHandler.get_user_notifications(user_id, role)

        return render_template('notification.html', notifications=notifications)