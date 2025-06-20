from flask import session, render_template
from app.app_stub import Flask_App_Stub
from app.dbhandler import UserRepository
from app.routes.endpoint import Endpoint
from app.swap_dbhandler import SwapRepository

class ViewSwapHistory(Endpoint):
    def __init__(self, app: Flask_App_Stub) -> None:
        super().__init__(app)

        self.route = '/view_swap_history'
        self.endpoint = 'view_swap_history'
        self.callback = self.view_swap_history
        self.methods = ['GET']

    def view_swap_history(self):
        user_id = session.get('user_id')

        swap_dbhandler = SwapRepository(self.flask_app)
        user_dbhandler = UserRepository(self.flask_app)

        swaps = swap_dbhandler.get_swap_completed(user_id)
        
        user = user_dbhandler.query_user(user_id)

        context = {
            'swaps': swaps,
            'user': user
        }

        return render_template('swap_history.html', **context)
