from flask import Flask, session
from app.configs import Config
from app.extensions import Extensions, db, bcrypt
from app.app import Flask_App
from app.endpoint_factory import EndpointFactory
from app.seeder import DatabaseSeeder

class FlaskAppBuilder: #builder
    """Builder class to set up the Flask application."""
    def __init__(self) -> None:
        self._app = Flask(__name__)
        self._db = None
        self._bcrypt = None
        self._session = None

    def configure_app(self) -> 'FlaskAppBuilder':
        config = Config()
        config.apply_config(self._app)
        return self

    def init_extensions(self) -> 'FlaskAppBuilder':
        extensions = Extensions()
        extensions.init_extensions(self._app)
        self._db = extensions.db
        self._bcrypt = extensions.bcrypt
        return self

    def create_database(self) -> 'FlaskAppBuilder':
        with self._app.app_context():
            self._db.create_all()
        return self
    
    def seed_database(self) -> 'FlaskAppBuilder':
        """Seed the database with initial data."""
        seeder = DatabaseSeeder(self._app)
        seeder.seed_all()
        return self

    def register_endpoints(self) -> 'FlaskAppBuilder':
        flask_app = Flask_App(self._app, self._db, self._bcrypt, self._session)
        endpoint_factory = EndpointFactory(flask_app)
        endpoint_factory.register_endpoints1()
        return self

    def build(self) -> Flask_App:
        print("Build success")
        return Flask_App(self._app, self._db, self._bcrypt, self._session)
        # return self._app
