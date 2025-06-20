from flask import flash, redirect, session
from app.app_stub import Flask_App_Stub
from app.routes.endpoint import Endpoint

class Logout(Endpoint):
    def __init__(self, app: Flask_App_Stub) -> None:
        super().__init__(app)

        self.route = '/logout'
        self.endpoint = 'logout'
        self.callback = self.logout
        self.methods = ['GET', 'POST']

    def logout(self):
        if 'user_id' in session:
            session.pop('user_id', None)
            session.pop('username', None)
            flash('You have been logged out.', 'info')
        
        return redirect('/')
