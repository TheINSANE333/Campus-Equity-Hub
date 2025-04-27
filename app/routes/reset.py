from flask import render_template, request, flash, redirect, url_for, session
from app.app_stub import Flask_App_Stub
from app.routes.endpoint import Endpoint
from app.dbhandler import DbHandler

class Reset(Endpoint):
    def __init__(self, app: Flask_App_Stub) -> None:
        super().__init__(app)

        self.route = '/reset'
        self.endpoint = 'reset'
        self.callback = self.reset
        self.methods = ['GET', 'POST']

    def reset(self):
        if request.method == 'POST':
            if request.form.get('confirm') == 'RESET':
                dbHandler = DbHandler(self.flask_app)
                dbHandler.reset_database()
                flash('Database has been reset successfully. Please log in again.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Confirmation text did not match. Database was not reset.', 'danger')
                
        return render_template('reset.html')
