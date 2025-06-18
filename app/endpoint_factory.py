from app.app_stub import Flask_App_Stub
from app.routes.index import Index
from app.routes.signup import Signup
from app.routes.login import Login
from app.routes.logout import Logout
from app.routes.dashboard import Dashboard
from app.routes.admin_dashboard import AdminDashboard
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
from app.routes.process_application import ProcessApplication
from app.routes.item_approval import ItemApproval
from app.routes.item_approval_detail import ItemApprovalDetail
from app.routes.process_item import ProcessItem
from app.routes.view_notification import ViewNotification
from app.routes.update_notification import UpdateNotification
from app.routes.profile import Profile
from app.routes.process_profile import ProcessProfile
from app.routes.request_swap import RequestSwap
from app.routes.submit_swap_request import SubmitSwapRequest
from app.routes.view_swap import ViewSwap
from app.routes.delete_item import DeleteItem
from app.routes.process_swap import ProcessSwap
from app.routes.search_api import SearchApi
from app.routes.search_api_item import SearchApiItem
from app.routes.view_swap_history import ViewSwapHistory
from app.routes.signup_admin import SignupAdmin
from app.routes.reset import Reset
from app.routes.delete_notification import DeleteNotification
from app.routes.achievement import Achievement

class EndpointFactory: #factory method
    def __init__(self, app: Flask_App_Stub) -> None:
        self.app = app
        self.endpoint_classes = {
            'Index': Index,
            'Signup': Signup,
            'Login': Login,
            'Dashboard': Dashboard,
            'AdminDashboard': AdminDashboard,
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
            'ViewApplication': ViewApplication,
            'ProcessApplication': ProcessApplication,
            'ItemApproval': ItemApproval,
            'ItemApprovalDetail': ItemApprovalDetail,
            'ProcessItem': ProcessItem,
            'ViewNotification': ViewNotification,
            'UpdateNotification': UpdateNotification,
            'Profile': Profile,
            'ProcessProfile': ProcessProfile,
            'RequestSwap': RequestSwap,
            'SubmitSwapRequest': SubmitSwapRequest,
            'ViewSwap': ViewSwap,
            'DeleteItem': DeleteItem,
            'ProcessSwap': ProcessSwap, 
            'SearchApi': SearchApi,
            'SearchApiItem': SearchApiItem,
            'ViewSwapHistory': ViewSwapHistory, 
            'SignupAdmin': SignupAdmin,
            'DeleteNotification': DeleteNotification,
            'Achievement': Achievement
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
