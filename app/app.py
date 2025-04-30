from flask import Flask

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Flask_App(metaclass = Singleton):
    
    def __init__(self, app: Flask, db, bcrypt, session) -> None:
        self._app = app
        self._db = db
        self._bcrypt = bcrypt
        self._session = session

    @property
    def app(self) -> Flask:
        return self._app
        
    @property
    def db(self):
        return self._db
        
    @property
    def bcrypt(self):
        return self._bcrypt
        
    @property
    def session(self):
        return self._session
    
    def run(self, *args, **kwargs) -> None:
        self.app.run(*args, **kwargs)

    