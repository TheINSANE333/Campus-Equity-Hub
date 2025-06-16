import os
import uuid
from flask import render_template, request, url_for, flash, session, redirect
from app.app_stub import Flask_App_Stub
from app.item_dbhandler import ItemRepository
from app.routes.endpoint import Endpoint
from app.function import allowed_file, getUnreadCount

class AddItem(Endpoint):
    def __init__(self, app: Flask_App_Stub) -> None:
        super().__init__(app)

        self.route = '/add_item'
        self.endpoint = 'add_item'
        self.callback = self.add_item
        self.methods = ['GET', 'POST']

    def add_item(self):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('login'))
        
        if request.method == 'POST':
            name = request.form['name']
            description = request.form['description']
            price = request.form['price']
            category = request.form['category']
        
            # Validate form data
            if not name or not price:
                flash('Name and price are required!', 'danger')
                return redirect(url_for('add_item'))
            
            # Handle image upload
            image_filename = None
            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename != '' and allowed_file(file.filename):
                    # Generate unique filename
                    filename = str(uuid.uuid4()) + '.' + file.filename.rsplit('.', 1)[1].lower()
                    os.makedirs('app/static/uploads', exist_ok=True)
                    file.save(os.path.join('app/static/uploads', filename))
                    image_filename = filename
            
            # Create new item
            item_dbHandler = ItemRepository(self.flask_app)

            command = NewItemCommand(item_dbHandler)
            success, message = command.execute(name, description, price, image_filename, category)
            
            flash(message, 'success' if success else 'danger')
            # return redirect(url_for('my_items'))

        user_id = session['user_id']
        total_unread = getUnreadCount(self.flask_app, user_id)
    
        return render_template('add_item.html', total_unread=total_unread)
    
class NewItemCommand:
    def __init__(self, item_dbHandler):
        self._item_dbHandler = item_dbHandler

    def execute(self, name, description, price, image_filename, category):
        user_id = session['user_id']
        self._item_dbHandler.add_new_item(name, description, price, image_filename, user_id, category)
        return True, 'Item created successfully! Item will be available after admin approval!'
