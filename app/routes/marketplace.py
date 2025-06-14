from flask import render_template, request, session, flash, redirect, url_for
from app.function import dateCounter
from app.app_stub import Flask_App_Stub
from app.item_dbhandler import ItemRepository
from app.dbhandler import UserRepository
from app.routes.endpoint import Endpoint

class Marketplace(Endpoint):
    def __init__(self, app: Flask_App_Stub) -> None:
        super().__init__(app)

        self.route = '/marketplace'
        self.endpoint = 'marketplace'
        self.callback = self.marketplace
        self.methods = ['GET', 'POST']

    def marketplace(self):
        if 'user_id' not in session:
            flash('Please log in to edit items.', 'danger')
            return redirect(url_for('login'))
        
        category_filter = request.args.get('category')

        item_dbHandler = ItemRepository(self.flask_app)
        user_dbhandler = UserRepository(self.flask_app)

        user = user_dbhandler.query_user(session['username'])
        user_role = user.role
        # user_role = session['user_role']
        
        two_days_ago = dateCounter()

        if category_filter != "All":
            items = item_dbHandler.get_item_by_category(category_filter)
        else:
            items = item_dbHandler.get_available_items()

        if user_role != 'special':
            items = [item for item in items if item.timestamp <= two_days_ago]

        return render_template('marketplace.html', items=items, selected_category=category_filter)
