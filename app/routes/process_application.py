from flask import request, redirect, url_for, flash
from app.app_stub import Flask_App_Stub
from app.application_dbhandler import ApplicationRepository
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
        application = application_dbHandler.query_item(application_id)
        
        application_dbHandler.update_status(application,action)
        
        # Redirect back to application list or details page
        return redirect(url_for('application_approval'))