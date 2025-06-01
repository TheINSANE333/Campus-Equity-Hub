from app.routes.index import Index
from app.routes.signup import Signup
from app.routes.login import Login
from app.routes.logout import Logout
from app.routes.dashboard import Dashboard
from app.routes.reset import Reset
from app.routes.add_item import AddItem
from app.routes.marketplace import Marketplace
from app.routes.view_item import ViewItem
from app.routes.chat_with_user import ChatWithUser
from app.routes.chat import Chat
from app.routes.message_api import MessageApi
from app.routes.unread_api import UnreadApi
from app.routes.apply_status import ApplyStatus
from app.routes.edit_item import EditItem
from app.routes.application_approval import ApplicationApproval
from app.routes.view_application import ViewApplication
from app.app_stub import Flask_App_Stub

class EndpointFactory: #factory method
    def __init__(self, app: Flask_App_Stub) -> None:
        self.app = app
        self.endpoint_classes = {
            'Index': Index,
            'Signup': Signup,
            'Login': Login,
            'Dashboard': Dashboard,
            'Logout': Logout,
            'Reset': Reset,
            'AddItem': AddItem, 
            'Marketplace': Marketplace,
            'ViewItem': ViewItem,
            'Chat': Chat,
            'ChatWithUser': ChatWithUser,
            'MessageApi': MessageApi,
            'UnreadApi': UnreadApi,
            'ApplyStatus': ApplyStatus, 
            'EditItem': EditItem,
            'ApplicationApproval': ApplicationApproval,
            'ViewApplication': ViewApplication
        }
        self._cache = {}

    def create_endpoint(self, endpoint_name: str):
        if endpoint_name not in self._cache:
            endpoint_class = self.endpoint_classes[endpoint_name]
            self._cache[endpoint_name] = endpoint_class(self.app)
        
        return self._cache[endpoint_name]
    
    def register_endpoints1(self) -> None:
        for endpoint_name in self.endpoint_classes.keys():
            endpoint = self.create_endpoint(endpoint_name)
            endpoint.register_endpoints3()