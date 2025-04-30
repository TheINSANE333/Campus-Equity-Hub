from flask import render_template, request, flash, redirect, url_for, session
from app.app_stub import Flask_App_Stub
from app.routes.endpoint import Endpoint
from app.dbhandler import DbHandler

class Login(Endpoint):
    def __init__(self, app: Flask_App_Stub) -> None:
        super().__init__(app)

        self.route = '/login'
        self.endpoint = 'login'
        self.callback = self.login
        self.methods = ['GET', 'POST']

    def login(self):
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            dbHandler = DbHandler(self.flask_app)
            
            # Find user by username
            user = dbHandler.query_user(username)
            
            # Check if user exists and password is correct
            if user and user.username == username and dbHandler.check_password(username, password):
                session.permanent = True
                session['user_id'] = user.id
                session['username'] = user.username

                flash(f'Welcome back, {user.username}!', 'success')
                
                return redirect(url_for('dashboard'))
            else:
                flash('Login unsuccessful. Please check your username and password.', 'danger')
        
        return render_template('login.html')
