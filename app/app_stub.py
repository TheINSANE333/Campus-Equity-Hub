from flask import Flask
from typing import Protocol

class Flask_App_Stub(Protocol):
    
    @property
    def app(self) -> Flask:
        ...

    @property
    def db(self):
        ...
        
    @property
    def bcrypt(self):
        ...
        
    @property
    def session(self):
        ...