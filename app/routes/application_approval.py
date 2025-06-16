import os
import uuid
from flask import render_template, request, url_for, flash, session, redirect
from app.app_stub import Flask_App_Stub
from app.application_dbhandler import ApplicationRepository
from app.routes.endpoint import Endpoint
from app.function import getUnreadCount

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

        user_id = session['user_id']
        total_unread = getUnreadCount(self.flask_app, user_id)

        return render_template('application_approval.html', approval=approval, total_unread=total_unread)
