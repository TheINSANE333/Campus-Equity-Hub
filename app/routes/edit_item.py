import os
import uuid
from flask import render_template, request, url_for, flash, session, redirect
from app.app_stub import Flask_App_Stub
from app.item_dbhandler import ItemRepository
from app.routes.endpoint import Endpoint
from app.function import allowed_file

class EditItem(Endpoint):
    def __init__(self, app: Flask_App_Stub) -> None:
        super().__init__(app)

        self.route = '/edit_item/<int:item_id>'
        self.endpoint = 'edit_item'
        self.callback = self.edit_item
        self.methods = ['GET', 'POST']

    def edit_item(self, item_id):
        if 'user_id' not in session:
            flash('Please log in to edit items.', 'danger')
            return redirect(url_for('login'))
        
        item_dbhandler = ItemRepository(self.flask_app)
        item = item_dbhandler.query_item(item_id)
        
        # Check if user owns the item or is admin
        if item.user_id != session['user_id']:
            flash('You do not have permission to edit this item.', 'danger')
            return redirect(url_for('marketplace'))
        
        if request.method == 'POST':
            name = request.form['name']
            description = request.form['description']
            price = float(request.form['price'])
            category = request.form['category']
            status = request.form['status']

            item_dbhandler.edit_item(item, name, description, price, category, status)
            
            # Handle image upload
            if 'image' in request.files:
                item_dbhandler.upload_image(item, request.files['image'])
            
            flash('Your item has been updated successfully!', 'success')
            # return redirect(url_for('my_items'))
        
        return render_template('edit_item.html', item=item)