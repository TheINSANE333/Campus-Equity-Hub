from flask import render_template
from app.app_stub import Flask_App_Stub
from app.application_dbhandler import ApplicationRepository
from app.routes.endpoint import Endpoint

class ViewApplication(Endpoint):
    def __init__(self, app: Flask_App_Stub) -> None:
        super().__init__(app)

        self.route = '/application/<int:application_id>'
        self.endpoint = 'view_application'
        self.callback = self.view_application
        self.methods = ['GET', 'POST']

    def view_application(self, application_id):
        application_dbHandler = ApplicationRepository(self.flask_app)

        application = application_dbHandler.query_item(application_id)
        return render_template('view_application.html', application = application)