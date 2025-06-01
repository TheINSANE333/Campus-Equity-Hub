from app.app_stub import Flask_App_Stub
from app.models.item import Item
from abc import ABC, abstractmethod
from app.models.application import Application
from typing import List

class DbHandler(ABC):
    _instance = None
    
    def __new__(cls, app: Flask_App_Stub = None):
        if cls._instance is None:
            if app is None:
                raise ValueError("App must be provided when initializing DbHandler for the first time")
            cls._instance = super(DbHandler, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, app: Flask_App_Stub) -> None:
        if self._initialized:
            return
            
        if app is None:
            raise ValueError("App must be provided when initializing DbHandler for the first time")
        
        self.flask_app = app
        self.db = app.db
        self.bcrypt = app.bcrypt

class ApplicationRepository(DbHandler):
    def add_application(self, user_id: int, name: str, ic: str, cgpa: float, pdf_filename: str,
                        hpnumber: str, income: int) -> None:
        new_application = Application(user_id = user_id,
                                      name = name,
                                      ic = ic,
                                      cgpa = cgpa,
                                      pdf_filename = pdf_filename,
                                      hpnumber = hpnumber,
                                      income = income,
                                      status = 'pending')
        self.db.session.add(new_application)
        self.db.session.commit()

    def get_pending_approval(self) -> List[Application]:
        # Get all pending approval
        return Application.query.filter_by(status='pending').all()
    
    def query_item(self, application_id: str) -> Application:
        return Application.query.get_or_404(application_id)
    
    def update_status(self, application, status) -> None:
        application.status = status
        self.db.session.commit()
        
