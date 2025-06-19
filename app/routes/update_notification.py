from flask import jsonify, session
import time
from flask import jsonify, session
from app.app_stub import Flask_App_Stub
from app.routes.endpoint import Endpoint
from app.notification_dbhandler import NotificationRepository

class UpdateNotification(Endpoint):
    def __init__(self, app: Flask_App_Stub) -> None:
        super().__init__(app)

        self.route = '/update_notification'
        self.endpoint = 'update_notification'
        self.callback = self.update_notification
        self.methods = ['GET']

        self.notification_dbhandler = NotificationRepository(self.flask_app)

    def update_notification(self):
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized'}), 401

        user_id = session.get('user_id')
        role = session.get('role', 'student')  # Default to 'student' if no role

        try:
            notifications = self.notification_dbhandler.get_user_notifications(user_id, role)
            notification_data = [
                {
                    'id': n.id,
                    'title': n.title,
                    'message': n.message,
                    'sender_id': n.sender_id,
                    'sender_name': n.sender_name,
                    'timestamp': n.timestamp.isoformat(),
                    'status': n.status,
                    'notification_type': n.notification_type
                } for n in notifications
            ]

            # Update session cache for unread count
            unread_count = sum(1 for n in notifications if n.status == 'unread')
            session['unread_count_' + str(user_id)] = unread_count
            session['unread_count_time_' + str(user_id)] = time.time()

            return jsonify({
                'success': True,
                'new_notifications': notification_data,
                'unread_count': unread_count
            })

        except Exception as e:
            self.flask_app.logger.error(f"Error polling notifications: {str(e)}")
            return jsonify({'success': False, 'error': str(e)})