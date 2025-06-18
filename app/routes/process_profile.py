from flask import request, redirect, url_for, flash, session
from app.app_stub import Flask_App_Stub
from app.dbhandler import UserRepository
from app.routes.endpoint import Endpoint

class ProcessProfile(Endpoint):  # Changed class name to match endpoint
    def __init__(self, app: Flask_App_Stub) -> None:
        super().__init__(app)

        self.route = '/process_profile'
        self.endpoint = 'process_profile'
        self.callback = self.process_profile
        self.methods = ['POST']
        
    def process_profile(self):  #
        process = request.form.get('process')
        newInfo = request.form.get('newInfo')

        dbHandler = UserRepository(self.flask_app)
        current_user = dbHandler.query_user(session['username'])
        
        if process == 'username':
            duplicate_user = dbHandler.query_user(newInfo)
            if duplicate_user:
                flash('Username already exists!', 'danger')
                return redirect(url_for('profile'))
            session['username'] = newInfo
            dbHandler.update_name(current_user, newInfo)
            flash('Username updated successfully!', 'success')

        elif process == 'email':
            duplicate_email = dbHandler.query_email(newInfo)
            if duplicate_email:
                flash('Email already exists!', 'danger')
                return redirect(url_for('profile'))
            dbHandler.update_email(current_user, newInfo)
            flash('Email updated successfully!', 'success')

        return redirect(url_for('profile'))