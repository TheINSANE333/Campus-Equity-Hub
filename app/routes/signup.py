from flask import render_template, request, flash, redirect, url_for
from app.app_stub import Flask_App_Stub
from app.dbhandler import UserRepository
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
            campus = request.form['campus']

            dbHandler = UserRepository(self.flask_app)

            command = SignupCommand(dbHandler)
            success, message = command.execute(username, email, password, campus)

            flash(message, 'success' if success else 'danger')
            return redirect(url_for('login' if success else 'signup'))
        
        return render_template('signup.html')

class SignupCommand:
    def __init__(self, dbHandler):
        self._dbHandler = dbHandler

    def execute(self, username, email, password, campus):
        user = self._dbHandler.query_user(username)
        email_inp = self._dbHandler.query_email(email)
        if user!= None and user.username == username:
            return False, 'Username already exists!'

        if email_inp != None and email_inp == email:
            return False, 'Email already exists!'

        self._dbHandler.add_new_user(username, email, password, campus, 'student')
        return True, 'Account created successfully!'