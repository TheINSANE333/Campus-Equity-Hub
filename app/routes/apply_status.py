import os
import uuid
from flask import render_template, request, url_for, flash, session, redirect
from sqlalchemy.sql.functions import current_user

from app.app_stub import Flask_App_Stub
from app.application_dbhandler import ApplicationRepository
from app.routes.endpoint import Endpoint
from app.function import pdfVerification, getUnreadCount
from app.notification_dbhandler import NotificationRepository
from app.dbhandler import UserRepository

class ApplyStatus(Endpoint):
    def __init__(self, app: Flask_App_Stub) -> None:
        super().__init__(app)

        self.route = '/apply_status'
        self.endpoint = 'apply_status'
        self.callback = self.apply_status
        self.methods = ['GET', 'POST']

    def apply_status(self):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('login'))

        notification_dbHandler = NotificationRepository(self.flask_app)
        user_dbHandler = UserRepository(self.flask_app)
        current_user_id = session.get('user_id')
        user = user_dbHandler.query_user_id(current_user_id)

        if request.method == 'POST':
            name = request.form['name']
            ic = request.form['ic']
            cgpa = request.form['cgpa']
            hpnumber = request.form['hpnum']
            income = request.form['income']

            # Handle documents uploaded
            pdf_filename = None
            pdf = request.files['pdf']
            if pdf and pdf.filename != '' and pdfVerification(pdf.filename):
                # Generate unique filename
                filename = str(uuid.uuid4()) + '.' + pdf.filename.rsplit('.', 1)[1].lower()
                os.makedirs('app/static/uploads', exist_ok=True)
                pdf.save(os.path.join('app/static/uploads', filename))
                pdf_filename = filename
            
            # Create new application
            application_dbHandler = ApplicationRepository(self.flask_app)
            command = NewApplicationCommand(application_dbHandler)
            success, message = command.execute(name, ic, cgpa, pdf_filename, hpnumber, income)
            notification_dbHandler.create_notification(0, session['user_id'], user.username, f"New Application, '{user.username}' has applied for a Priority Access.", 'Special Approval','unread', 'admin', 'Application for Priority Access')
            
            flash(message, 'success' if success else 'danger')
            if success:
                return render_template('dashboard.html')
    
        return render_template('apply_status.html')
    
class NewApplicationCommand:
    def __init__(self, application_dbHandler):
        self._application_dbHandler = application_dbHandler

    def execute(self, name, ic, cgpa, pdf_filename, hpnumber, income):
        user_id = session['user_id']
        self._application_dbHandler.add_application(user_id, name, ic, cgpa, pdf_filename, hpnumber, income)
        return True, 'Application created successfully!'
