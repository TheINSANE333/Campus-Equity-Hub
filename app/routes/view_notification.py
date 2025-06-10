from flask import render_template, request, flash, redirect, url_for, session, jsonify, Blueprint
from app.app_stub import Flask_App_Stub
from app.routes.endpoint import Endpoint
from app.models.notification import Notification
from app.models.user import User
from app.extensions import db
from datetime import datetime

class ViewNotification(Endpoint):
    def __init__(self, app: Flask_App_Stub) -> None:
        super().__init__(app)

        self.route = '/view_notification'
        self.endpoint = 'view_notification'
        self.callback = self.view_notification_page
        self.methods = ['GET']

    def view_notification_page(self):
        """Render the notification HTML page"""
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('login'))

        return render_template('notification.html')

    def register_endpoints3(self):
        # Create API blueprint if not exists
        if not hasattr(self, 'api_blueprint'):
            self.api_blueprint = Blueprint('api', __name__, url_prefix='/api')

            @self.api_blueprint.route('/notifications', methods=['GET'])
            def get_notifications():
                """Get all notifications for current user with pagination and filtering"""
                user_id = request.args.get('user_id', type=int)
                if not user_id:
                    return jsonify({'error': 'User ID is required'}), 400

                # Pagination parameters
                page = request.args.get('page', 1, type=int)
                per_page = request.args.get('per_page', 10, type=int)

                # Filter parameters
                notification_type = request.args.get('type')
                unread_only = request.args.get('unread_only', 'false').lower() == 'true'

                # Base query
                query = Notification.query.filter_by(receiver_id=user_id)

                # Apply filters
                if notification_type:
                    query = query.filter_by(notification_type=notification_type)
                if unread_only:
                    query = query.filter_by(read=False)

                # Order by timestamp descending
                query = query.order_by(Notification.timestamp.desc())

                # Paginate results
                paginated_notifications = query.paginate(page=page, per_page=per_page, error_out=False)

                notifications = [n.to_dict() for n in paginated_notifications.items]

                return jsonify({
                    'notifications': notifications,
                    'total': paginated_notifications.total,
                    'pages': paginated_notifications.pages,
                    'current_page': page
                })

            @self.api_blueprint.route('/notifications/<int:notification_id>/read', methods=['POST'])
            def mark_notification_as_read(notification_id):
                """Mark a specific notification as read"""
                notification = Notification.query.get_or_404(notification_id)
                notification.mark_as_read()
                return jsonify(notification.to_dict())

            @self.api_blueprint.route('/notifications/mark_all_read', methods=['POST'])
            def mark_all_notifications_as_read():
                """Mark all notifications for a user as read"""
                user_id = request.json.get('user_id')
                if not user_id:
                    return jsonify({'error': 'User ID is required'}), 400

                Notification.query.filter_by(receiver_id=user_id, read=False).update(
                    {'read': True}, synchronize_session=False)
                db.session.commit()

                return jsonify({'message': 'All notifications marked as read'})

            @self.api_blueprint.route('/notifications/unread_count', methods=['GET'])
            def get_unread_count():
                """Get count of unread notifications for a user"""
                user_id = request.args.get('user_id', type=int)
                if not user_id:
                    return jsonify({'error': 'User ID is required'}), 400

                count = Notification.query.filter_by(receiver_id=user_id, read=False).count()
                return jsonify({'unread_count': count})

            @self.api_blueprint.route('/notifications', methods=['DELETE'])
            def delete_all_notifications():
                """Delete all notifications for current user"""
                user_id = request.json.get('user_id')
                if not user_id:
                    return jsonify({'error': 'User ID is required'}), 400

                try:
                    # Delete all notifications for this user
                    Notification.query.filter_by(receiver_id=user_id).delete()
                    db.session.commit()
                    return jsonify({'message': 'All notifications deleted'})
                except Exception as e:
                    db.session.rollback()
                    return jsonify({'error': str(e)}), 500

            # Register the API blueprint
            self.flask_app.app.register_blueprint(self.api_blueprint)

        # Register the main endpoint
        super().register_endpoints3()
