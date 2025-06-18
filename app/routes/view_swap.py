import os
import uuid
from flask import render_template, request, url_for, flash, session, redirect
from app.app_stub import Flask_App_Stub
from app.swap_dbhandler import SwapRepository
from app.item_dbhandler import ItemRepository
from app.routes.endpoint import Endpoint
from app.function import allowed_file, getUnreadCount

class ViewSwap(Endpoint):
    def __init__(self, app: Flask_App_Stub) -> None:
        super().__init__(app)

        self.route = '/swap/<int:swap_id>'
        self.endpoint = 'view_swap'
        self.callback = self.view_swap
        self.methods = ['GET', 'POST']

    def view_swap(self, swap_id):
        swap_dbHandler = SwapRepository(self.flask_app)
        item_dbHandler = ItemRepository(self.flask_app)
        swap = swap_dbHandler.query_swap(swap_id)
        item = item_dbHandler.query_item(swap.item_id)
        target = item_dbHandler.query_item(swap.target_item_id)
        current_user = session.get('user_id')
        context = {
            'swap': swap,
            'item': item,
            'target': target,
            'user': current_user
        }

        return render_template('view_swap.html', **context)