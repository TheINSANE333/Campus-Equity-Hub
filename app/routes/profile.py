from flask import render_template, request, flash, redirect, url_for, session
from app.app_stub import Flask_App_Stub
from app.routes.endpoint import Endpoint
from app.dbhandler import UserRepository
from app.function import getUnreadCount

class Profile(Endpoint):
    def __init__(self, app: Flask_App_Stub) -> None:
        super().__init__(app)

        self.route = '/profile'
        self.endpoint = 'profile'
        self.callback = self.profile
        self.methods = ['GET', 'POST']

    def profile(self):
        if 'user_id' not in session:
            flash('Please login first', 'danger')
            return redirect(url_for('login'))
        
        dbHandler = UserRepository(self.flask_app)
        user = dbHandler.query_user_id(session['user_id'])

        user_id = session['user_id']
        total_unread = getUnreadCount(self.flask_app, user_id)
        return render_template('profile.html', user=user, total_unread=total_unread)
