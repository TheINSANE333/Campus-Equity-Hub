from flask import render_template, request, flash, redirect, url_for, session
from app.app_stub import Flask_App_Stub
from app.routes.endpoint import Endpoint
from app.dbhandler import AdminDatabaseTools
import os
import sys

class Reset(Endpoint):
    def __init__(self, app: Flask_App_Stub) -> None:
        super().__init__(app)

        self.route = '/reset'
        self.endpoint = 'reset'
        self.callback = self.reset
        self.methods = ['GET', 'POST']

    def reset(self):
        if 'user_id' not in session or session['user_id'] != 1:
            flash('Please log in as admin to access this page.', 'danger')
            return redirect(url_for('login'))
        
        if request.method == 'POST':
            if request.form.get('confirm') == 'RESET':
                dbHandler = AdminDatabaseTools(self.flask_app)
                dbHandler.reset_database()
                print("Db reset successful")
                flash('Database has been reset successfully. Restarting application...', 'success')
            
                # Restart the application
                os.execv(sys.executable, ['python'] + sys.argv)

            else:
                flash('Confirmation text did not match. Database was not reset.', 'danger')
                
        return render_template('reset.html')



