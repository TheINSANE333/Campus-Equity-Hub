from flask import request, redirect, url_for, flash, session
from app.app_stub import Flask_App_Stub
from app.dbhandler import UserRepository
from app.routes.endpoint import Endpoint

class ProcessItem(Endpoint):
    def __init__(self, app: Flask_App_Stub) -> None:
        super().__init__(app)

        self.route = '/process_profile/<int:user_id>'
        self.endpoint = 'process_profile'
        self.callback = self.process_profile
        self.methods = ['POST']
        
    def process_profile(self, process, newInfo):
        # Get the profile from database
        dbHandler = UserRepository(self.flask_app)
        user = dbHandler.query_user(session['username'])
        
        if process == 'username':
            dbHandler.update_name(user, newInfo)
            flash('User information updated!', 'success')

        elif process == 'email':
            dbHandler.update_email(user, newInfo)
            flash('User information updated!', 'success')

        # Redirect back to item list or details page
        return redirect(url_for('profile'))