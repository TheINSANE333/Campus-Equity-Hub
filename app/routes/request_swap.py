from flask import render_template, request, flash, redirect, url_for, session
from app.app_stub import Flask_App_Stub
from app.routes.endpoint import Endpoint
from app.item_dbhandler import ItemRepository
from app.function import getUnreadCount
from app.swap_dbhandler import SwapRepository

class RequestSwap(Endpoint):
    def __init__(self, app: Flask_App_Stub) -> None:
        super().__init__(app)

        self.route = '/request_swap/<int:item_id>'
        self.endpoint = 'request_swap_page'
        self.callback = self.request_swap_page
        self.methods = ['GET']

    def request_swap_page(self, item_id):
        item_dbhandler = ItemRepository(self.flask_app)
        swap_dbhandler = SwapRepository(self.flask_app)
        item = item_dbhandler.query_item(item_id)

        item_dbhandler.check_item_available(item)

        if 'user_id' not in session:
            flash('Please log in to request a swap.', 'danger')
            return redirect(url_for('login'))

        current_user_id = session.get('user_id')
        all_my_items = item_dbhandler.get_user_items(current_user_id)
        eligible_my_items = swap_dbhandler.get_eligible_item(all_my_items)

        context = {
            'item': item,
            'myItems': eligible_my_items, # Pass the filtered list
        }

        return render_template('request_swap.html', **context)