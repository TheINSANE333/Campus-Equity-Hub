from flask import render_template, request, flash, redirect, url_for
from app.app_stub import Flask_App_Stub
from app.dbhandler import DbHandler
from app.routes.endpoint import Endpoint

class Signup(Endpoint):
    def __init__(self, app: Flask_App_Stub) -> None:
        super().__init__(app)

        self.route = '/signup'
        self.endpoint = 'signup'
        self.callback = self.signup
        self.methods = ['GET', 'POST']

    def signup(self):
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
        
            # Check if username or email already exists
            dbHandler = DbHandler(self.flask_app)

            user = dbHandler.query_user(username)
            if user != None and user.username == username:
                flash('Username already exists!', 'danger')
                print("Username already exists!")
                return redirect(url_for('signup'))
            
            email_inp = dbHandler.query_email(email)
            if email_inp != None and email_inp == email:
                flash('Email already exists!', 'danger')
                print("Email already exists!")
                print(email_inp)
                return redirect(url_for('signup'))
            
            # Create new user
            dbHandler.add_new_user(username, email, password)
            
            flash('Your account has been created! You can now log in.', 'success')
            return redirect(url_for('login'))
        
        return render_template('signup.html')
