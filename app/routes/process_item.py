from flask import request, redirect, url_for, flash, session
from app.app_stub import Flask_App_Stub
from app.item_dbhandler import ItemRepository
from app.routes.endpoint import Endpoint

class ProcessItem(Endpoint):
    def __init__(self, app: Flask_App_Stub) -> None:
        super().__init__(app)

        self.route = '/process_item/<int:item_id>'
        self.endpoint = 'process_item'
        self.callback = self.process_item
        self.methods = ['POST']
        
    def process_item(self, item_id):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('login'))
        
        if session['role'] != "admin":
            flash ('Please log in as admin to access this page.', 'danger')
            return redirect(url_for('login'))
        
        action = request.form.get('action')
        
        # Get the item from database
        item_dbHandler = ItemRepository(self.flask_app)
        item = item_dbHandler.query_item(item_id)
        
        item_dbHandler.update_status(item,action)
        flash('Item status updated!', 'success')
        # Redirect back to item list or details page
        return redirect(url_for('item_approval'))