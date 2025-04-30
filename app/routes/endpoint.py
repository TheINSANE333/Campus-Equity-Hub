from app.app_stub import Flask_App_Stub
from abc import ABC

class Endpoint(ABC): #Abstract factory

    route: str = None
    endpoint: str = None
    callback: str = None
    methods: list = None

    def __init__(self, app: Flask_App_Stub) -> None:
        self.flask_app = app

    def register_endpoints3(self) -> None:
        methods = self.methods if self.methods is not None else ['GET', 'POST']
        self.flask_app.app.add_url_rule(rule=self.route, endpoint=self.endpoint, view_func=self.callback, methods=self.methods)
