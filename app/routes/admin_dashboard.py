from flask import render_template, url_for, flash, session, redirect
from app.app_stub import Flask_App_Stub
from app.routes.endpoint import Endpoint
from app.dbhandler import UserRepository

class AdminDashboard(Endpoint):
    def __init__(self, app: Flask_App_Stub) -> None:
        super().__init__(app)

        self.route = '/admin_dashboard'
        self.endpoint = 'admin_dashboard'
        self.callback = self.adminDashboard
        self.methods = ['GET', 'POST']

    def adminDashboard(self):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('login'))
        
        if session['role'] != "admin":
            flash ('Please log in as admin to access this page.', 'danger')
            return redirect(url_for('login'))
        
        dbHandler = UserRepository(self.flask_app)
        user_id = session['user_id']
        users = dbHandler.get_all_users(user_id)
        myselfs = dbHandler.query_user_id(user_id)
        
        return render_template('admin_dashboard.html', users=users, me=myselfs)