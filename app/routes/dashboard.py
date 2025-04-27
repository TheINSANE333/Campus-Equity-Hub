from flask import render_template, url_for, flash, session, redirect
from app.app_stub import Flask_App_Stub
from app.routes.endpoint import Endpoint

class Dashboard(Endpoint):
    def __init__(self, app: Flask_App_Stub) -> None:
        super().__init__(app)

        self.route = '/dashboard'
        self.endpoint = 'dashboard'
        self.callback = self.dashboard
        self.methods = ['GET', 'POST']

    def dashboard(self):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('login'))
        
        return render_template('dashboard.html', username=session['username'])
