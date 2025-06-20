from flask import jsonify, request as flask_request, session
from app.app_stub import Flask_App_Stub
from app.routes.endpoint import Endpoint
from app.notification_dbhandler import NotificationRepository


class DeleteNotification(Endpoint):
    def __init__(self, app: Flask_App_Stub) -> None:
        super().__init__(app)

        self.route = '/delete_notification'
        self.endpoint = 'delete_notification'
        self.callback = self.delete_notification
        self.methods = ['POST', 'DELETE']

        self.notification_dbhandler = NotificationRepository(self.flask_app)

    def delete_notification(self):

        user_id = session['user_id']
        role = session.get('role', 'student')  # Default to 'student' if no role

        if flask_request.method == 'POST':
            data = flask_request.get_json()
            notification_id = data.get('notification_id')

            if not notification_id:
                return jsonify({'success': False, 'error': 'Missing notification ID'})

            try:
                self.notification_dbhandler.set_notification_status_to_delete(notification_id)
                return jsonify({'success': True})
            except Exception as e:
                self.flask_app.logger.error(f"Error deleting notification: {str(e)}")
                return jsonify({'success': False, 'error': str(e)})

        elif flask_request.method == 'DELETE':
            try:
                # Pass the role to properly handle admin notifications
                self.notification_dbhandler.set_all_notification_status_to_delete(user_id, role)
                return jsonify({'success': True})
            except Exception as e:
                self.flask_app.logger.error(f"Error deleting all notifications: {str(e)}")
                return jsonify({'success': False, 'error': str(e)})