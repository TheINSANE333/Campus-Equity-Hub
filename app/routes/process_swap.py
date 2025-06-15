from datetime import datetime
from flask import render_template, request, redirect, url_for, flash
from app.app_stub import Flask_App_Stub
from app.item_dbhandler import ItemRepository
from app.swap_dbhandler import SwapRepository  # Add this import
from app.routes.endpoint import Endpoint

class ProcessSwap(Endpoint):
    def __init__(self, app: Flask_App_Stub) -> None:
        super().__init__(app)

        self.route = '/process_swap/<int:swap_id>'
        self.endpoint = 'process_swap'
        self.callback = self.process_swap
        self.methods = ['POST']
        
    def process_swap(self, swap_id):
        action = request.form.get('action')
        
        # Get the swap and items related from database
        swap_dbHandler = SwapRepository(self.flask_app)
        item_dbHandler = ItemRepository(self.flask_app)

        swap = swap_dbHandler.query_swap(swap_id)
        item = item_dbHandler.query_item(swap.item_id)
        target = item_dbHandler.query_item(swap.target_item_id)

        if action == 'accepted':
            location = request.form.get('location')
            timeStr = request.form.get('trade_time')
            time = datetime.strptime(timeStr, '%Y-%m-%dT%H:%M')
            item_dbHandler.update_item_status(item,'sold')
            item_dbHandler.update_item_status(target,'sold')
            swap_dbHandler.update_swap_status(swap, 'accepted')
            swap_dbHandler.update_location(swap, location)
            swap_dbHandler.update_time(swap, time)
            flash('Swap Accepted!', 'success')
        else:
            item_dbHandler.update_item_status(item, 'available')
            item_dbHandler.update_item_status(target, 'available')
            swap_dbHandler.update_swap_status(swap, 'rejected')
            flash('Swap Rejected!', 'success')

        context = {
            'swap': swap,
            'item': item,
            'target': target
        }
        
        return render_template('view_swap.html', **context)