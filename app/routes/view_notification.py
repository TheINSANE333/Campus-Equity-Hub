from flask import render_template, request, flash, redirect, url_for, session, jsonify, Blueprint
from app.app_stub import Flask_App_Stub
from app.routes.endpoint import Endpoint
from app.notification_dbhandler import NotificationRepository
from app.function import getUnreadCount

class ViewNotification(Endpoint):
    def __init__(self, app: Flask_App_Stub) -> None:
        super().__init__(app)

        # Keep endpoint name consistent everywhere
        self.route = '/notifications'
        self.endpoint = 'view_notification'  # Changed to match references elsewhere in the code
        self.callback = self.view_notification_page
        self.methods = ['GET']

    def view_notification_page(self):
        """Render the notification HTML page"""
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('login'))
        
        notification_dbHandler = NotificationRepository(self.flask_app)
        notifications = notification_dbHandler.get_user_notifications(session['user_id'])
        
        # Check if there are hidden notifications from update_delete_notification
        update_delete_notification = None
        try:
            # Import inside method to avoid circular imports
            from app.endpoint_factory import EndpointFactory
            factory = EndpointFactory(self.flask_app)
            update_delete_notification = factory.create_endpoint('UpdateDeleteNotification')
        except Exception as e:
            self.flask_app.logger.error(f"Error getting UpdateDeleteNotification instance: {str(e)}")

        # Filter out hidden notifications if any
        if update_delete_notification and hasattr(update_delete_notification, 'hidden_notifications'):
            user_id = session['user_id']
            hidden_ids = update_delete_notification.hidden_notifications.get(user_id, [])
            notifications = [n for n in notifications if n.id not in hidden_ids]

        return render_template('notification.html', notifications=notifications)
