from flask import render_template
from app.app_stub import Flask_App_Stub
from app.routes.endpoint import Endpoint

class Index(Endpoint):
    def __init__(self, app: Flask_App_Stub) -> None:
        super().__init__(app)

        self.route = '/'
        self.endpoint = 'index'
        self.callback = self.index
        self.methods = None

    def index(self):
        return render_template('index.html')
