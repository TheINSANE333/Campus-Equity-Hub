from flask import request, redirect, url_for, flash, session
from app.app_stub import Flask_App_Stub
from app.application_dbhandler import ApplicationRepository
from app.dbhandler import UserRepository  # Add this import
from app.routes.endpoint import Endpoint
from app.notification_dbhandler import NotificationRepository

class ProcessApplication(Endpoint):
    def __init__(self, app: Flask_App_Stub) -> None:
        super().__init__(app)

        self.route = '/process_application/<int:application_id>'
        self.endpoint = 'process_application'
        self.callback = self.process_application
        self.methods = ['POST']
        
    def process_application(self, application_id):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('login'))


        
        if session['role'] != "admin":
            flash ('Please log in as admin to access this page.', 'danger')
            return redirect(url_for('login'))
        
        action = request.form.get('action')
        
        # Get the application from database
        application_dbHandler = ApplicationRepository(self.flask_app)
        user_dbHandler = UserRepository(self.flask_app)  # Add this

        notification_dbHandler = NotificationRepository(self.flask_app)

        application = application_dbHandler.query_item(application_id)
        
        application_dbHandler.update_status(application, action)
        sender_id = session.get('user_id')
        sender = user_dbHandler.query_user_id(sender_id)
        name =  sender.username
        user = user_dbHandler.query_user_id(application.user_id)


        # If application is approved, update user role to special
        if action == 'approved':

            user_dbHandler.update_role(user, 'special')
            role_to_be_view = user.role
            # delete all the notification when status is student
            notification_dbHandler.set_all_notification_status_to_delete(user.id, 'student')
            notification_dbHandler.create_notification(user.id, sender_id, name, 'Your status has been approved and updated to Priority Access','Special Approval', 'unread', role_to_be_view, 'Updated Status For Priority Access')
            flash('Application approved and user role updated to special!', 'success')
        else:
            role_to_be_view = user.role
            flash('Application rejected!', 'danger')
            notification_dbHandler.create_notification(user.id, sender_id, name, 'Your status has been approved and updated to Priority Access','Special Approval', 'unread', role_to_be_view, 'Updated Status For Priority Access')
        
        # Redirect back to application list or details page
        return redirect(url_for('application_approval'))