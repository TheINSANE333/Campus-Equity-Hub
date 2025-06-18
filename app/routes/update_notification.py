from flask import jsonify
from app.app_stub import Flask_App_Stub
from app.routes.endpoint import Endpoint
from flask_login import login_required
from app.notification_dbhandler import NotificationRepository


class UpdateNotification(Endpoint):
    def __init__(self, app: Flask_App_Stub) -> None:
        super().__init__(app)

        self.route = '/update_notification'
        self.endpoint = 'update_notification'
        self.callback = self.update_notification
        self.methods = ['GET']

        self.notification_dbhandler = NotificationRepository.get_instance(app)

    @login_required
    def update_notification(self):
        if 'user_id' not in self.request.session:
            return jsonify({'error': 'Unauthorized'}), 401

        user_id = self.request.session['user_id']

        try:
            notifications = self.notification_dbhandler.get_user_notifications(user_id)
            notification_data = [
                {
                    'id': n.id,
                    'title': n.title,
                    'message': n.message,
                    'sender_id': n.sender_id,
                    'timestamp': n.timestamp.isoformat(),
                    'read': n.read
                } for n in notifications
            ]

            return jsonify({
                'success': True,
                'new_notifications': notification_data
            })

        except Exception as e:
            self.flask_app.logger.error(f"Error polling notifications: {str(e)}")
            return jsonify({'success': False, 'error': str(e)})
