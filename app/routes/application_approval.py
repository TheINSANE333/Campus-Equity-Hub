import os
import uuid
from flask import render_template, request, url_for, flash, session, redirect
from app.app_stub import Flask_App_Stub
from app.application_dbhandler import ApplicationRepository
from app.routes.endpoint import Endpoint

class ApplicationApproval(Endpoint):
    def __init__(self, app: Flask_App_Stub) -> None:
        super().__init__(app)

        self.route = '/application_approval'
        self.endpoint = 'application_approval'
        self.callback = self.application_approval
        self.methods = ['GET', 'POST']

    def application_approval(self):
        application_dbHandler = ApplicationRepository(self.flask_app)

        approval = application_dbHandler.get_pending_approval()
        return render_template('application_approval.html', approval=approval)
