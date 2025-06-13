from flask import render_template, request, flash, redirect, url_for, session
from app.app_stub import Flask_App_Stub
from app.models.item import Item
from app.extensions import db
from datetime import datetime
from app.routes.endpoint import Endpoint
from app.models.swap import Swap

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

        # Render the request swap page
        return render_template('request_swap.html', item=item)