from flask import render_template, request, url_for, flash, session, redirect, jsonify
from app.app_stub import Flask_App_Stub
from app.notification_dbhandler import NotificationRepository
from app.routes.endpoint import Endpoint
from flask_login import login_required, current_user

class UpdateDeleteNotification(Endpoint):
    def __init__(self, app: Flask_App_Stub) -> None:
        super().__init__(app)
        self.notification_repo = NotificationRepository.get_instance(app)
        
        # Define endpoints
        self.routes = [
            {
                'route': '/api/notifications/<int:notification_id>',
                'endpoint': 'delete_notification',
                'callback': self.delete_notification,
                'methods': ['DELETE']
            },
            {
                'route': '/api/notifications',
                'endpoint': 'delete_all_notifications',
                'callback': self.delete_all_notifications,
                'methods': ['DELETE']
            },
            {
                'route': '/api/notifications',
                'endpoint': 'check_new_notifications',
                'callback': self.check_new_notifications,
                'methods': ['GET']
            },
            {
                'route': '/api/notifications/<int:notification_id>/read',
                'endpoint': 'mark_notification_as_read',
                'callback': self.mark_notification_as_read,
                'methods': ['PUT']
            },
            {
                'route': '/api/notifications/read-all',
                'endpoint': 'mark_all_notifications_as_read',
                'callback': self.mark_all_notifications_as_read,
                'methods': ['PUT']
            },
            {
                'route': '/api/notifications/confirm',
                'endpoint': 'confirm_deletion',
                'callback': self.confirm_deletion,
                'methods': ['POST']
            }
        ]
        
        # For storing hidden notifications per user (local only)
        self.hidden_notifications = {}

    def register_endpoints3(self) -> None:
        for route_config in self.routes:
            self.route = route_config['route']
            self.endpoint = route_config['endpoint']
            self.callback = route_config['callback']
            self.methods = route_config['methods']
            super().register_endpoints3()

    @login_required
    def delete_notification(self, notification_id):
        try:
            notification = self.notification_repo.get_notification_by_id(notification_id)
            
            # Check if the notification belongs to the current user
            if notification.receiver_id != current_user.id:
                return jsonify({'error': 'Unauthorized access'}), 403
            
            # Add confirmation step
            if request.headers.get('Confirmation') != 'confirmed':
                return jsonify({
                    'status': 'confirmation_required',
                    'message': 'Are you sure you want to hide this notification?',
                    'notification_id': notification_id
                }), 200
            
            # Instead of deleting from database, just hide it locally
            user_id = current_user.id
            if user_id not in self.hidden_notifications:
                self.hidden_notifications[user_id] = []
            
            if notification_id not in self.hidden_notifications[user_id]:
                self.hidden_notifications[user_id].append(notification_id)
            
            # Update UI message to clarify this is temporary
            return jsonify({
                'success': True, 
                'message': 'Notification hidden temporarily. It will reappear after page refresh.',
                'temporary': True
            }), 200
        except Exception as e:
            self.flask_app.logger.error(f"Error hiding notification: {str(e)}")
            return jsonify({'error': str(e)}), 500
    
    @login_required
    def delete_all_notifications(self):
        try:
            user_id = current_user.id
            
            # Add confirmation step
            if request.headers.get('Confirmation') != 'confirmed':
                return jsonify({
                    'status': 'confirmation_required',
                    'message': 'Are you sure you want to hide all your notifications? They will reappear when you refresh the page.',
                    'user_id': user_id
                }), 200
            
            # Get all user's notifications and store their IDs in hidden list
            notifications = self.notification_repo.get_user_notifications(user_id)
            
            if user_id not in self.hidden_notifications:
                self.hidden_notifications[user_id] = []
            
            for notification in notifications:
                if notification.id not in self.hidden_notifications[user_id]:
                    self.hidden_notifications[user_id].append(notification.id)
            
            # Update UI message to clarify this is temporary
            return jsonify({
                'success': True, 
                'message': 'All notifications hidden temporarily. They will reappear after page refresh.',
                'temporary': True
            }), 200
        except Exception as e:
            self.flask_app.logger.error(f"Error hiding all notifications: {str(e)}")
            return jsonify({'error': str(e)}), 500
    
    @login_required
    def confirm_deletion(self):
        """Endpoint to handle deletion confirmation"""
        try:
            data = request.json
            confirmation = data.get('confirm', False)
            
            if not confirmation:
                return jsonify({'status': 'cancelled', 'message': 'Action cancelled'}), 200
                
            notification_id = data.get('notification_id')
            delete_all = data.get('delete_all', False)
            
            if delete_all:
                return self.delete_all_notifications()
            elif notification_id:
                return self.delete_notification(notification_id)
            else:
                return jsonify({'error': 'Invalid request parameters'}), 400
                
        except Exception as e:
            self.flask_app.logger.error(f"Error in confirmation process: {str(e)}")
            return jsonify({'error': str(e)}), 500
    
    @login_required
    def check_new_notifications(self):
        try:
            user_id = current_user.id
            unread_count = self.notification_repo.count_unread_notifications(user_id)
            
            # Get all notifications for the user, but filter out hidden ones
            all_notifications = self.notification_repo.get_user_notifications(user_id)
            visible_notifications = all_notifications
            
            if user_id in self.hidden_notifications:
                hidden_ids = self.hidden_notifications[user_id]
                visible_notifications = [n for n in all_notifications if n.id not in hidden_ids]
            
            visible_unread = [n for n in visible_notifications if not n.read]
            
            return jsonify({
                'new_notifications': len(visible_unread) > 0,
                'unread_count': len(visible_unread),
                'total_count': len(visible_notifications),
                'hidden_count': len(self.hidden_notifications.get(user_id, []))
            }), 200
        except Exception as e:
            self.flask_app.logger.error(f"Error checking notifications: {str(e)}")
            return jsonify({'error': str(e)}), 500
    
    @login_required
    def mark_notification_as_read(self, notification_id):
        try:
            notification = self.notification_repo.get_notification_by_id(notification_id)
            
            # Check if the notification belongs to the current user
            if notification.receiver_id != current_user.id:
                return jsonify({'error': 'Unauthorized access'}), 403
            
            self.notification_repo.mark_as_read(notification_id)
            return jsonify({'success': True}), 200
        except Exception as e:
            self.flask_app.logger.error(f"Error marking notification as read: {str(e)}")
            return jsonify({'error': str(e)}), 500
    
    @login_required
    def mark_all_notifications_as_read(self):
        try:
            user_id = current_user.id
            self.notification_repo.mark_all_as_read(user_id)
            return jsonify({'success': True}), 200
        except Exception as e:
            self.flask_app.logger.error(f"Error marking all notifications as read: {str(e)}")
            return jsonify({'error': str(e)}), 500
