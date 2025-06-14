from flask import render_template, request, flash, redirect, url_for, session
from app.app_stub import Flask_App_Stub
from app.models.item import Item
from app.extensions import db
from datetime import datetime
from app.routes.endpoint import Endpoint
from app.models.swap import Swap
from app.item_dbhandler import ItemRepository

class RequestSwap(Endpoint):
    def __init__(self, app: Flask_App_Stub) -> None:
        super().__init__(app)

        self.route = '/request_swap/<int:item_id>'
        self.endpoint = 'request_swap_page'
        self.callback = self.request_swap_page
        self.methods = ['GET']

    def request_swap_page(self, item_id):
        # Find the item to be swapped
        item = Item.query.get_or_404(item_id)

        # Check if the item is available for swap
        if item.status != 'available':
            flash('This item is no longer available for swap.', 'danger')
            return redirect(url_for('dashboard'))

        if 'user_id' not in session:
            flash('Please log in to request a swap.', 'danger')
            return redirect(url_for('login'))

        current_user_id = session.get('user_id')
        item_dbhandler = ItemRepository(self.flask_app)
        all_my_items = item_dbhandler.get_user_items(current_user_id)

        # Filter user's items: must be 'available' and 'approved'
        eligible_my_items = [
            item for item in all_my_items
            if item.status == 'available' and item.approval == 'approved'
        ]

        context = {
            'item': item,
            'myItems': eligible_my_items, # Pass the filtered list
        }

        # Render the request swap page
        return render_template('request_swap.html', **context)