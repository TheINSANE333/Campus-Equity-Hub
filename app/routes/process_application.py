from flask import request, redirect, url_for, flash
from app.app_stub import Flask_App_Stub
from app.application_dbhandler import ApplicationRepository
from app.dbhandler import UserRepository  # Add this import
from app.routes.endpoint import Endpoint

class ProcessApplication(Endpoint):
    def __init__(self, app: Flask_App_Stub) -> None:
        super().__init__(app)

        self.route = '/process_application/<int:application_id>'
        self.endpoint = 'process_application'
        self.callback = self.process_application
        self.methods = ['POST']
        
    def process_application(self, application_id):
        action = request.form.get('action')
        
        # Get the application from database
        application_dbHandler = ApplicationRepository(self.flask_app)
        user_dbHandler = UserRepository(self.flask_app)  # Add this
        
        application = application_dbHandler.query_item(application_id)
        
        application_dbHandler.update_status(application, action)
        
        # If application is approved, update user role to special
        if action == 'approved':
            user = user_dbHandler.query_user_id(application.user_id)
            user_dbHandler.update_role(user, 'special')
            flash('Application approved and user role updated to special!', 'success')
        else:
            flash('Application rejected!', 'danger')
        
        # Redirect back to application list or details page
        return redirect(url_for('application_approval'))