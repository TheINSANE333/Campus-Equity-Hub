from flask import render_template, url_for, flash, session, redirect
from app.app_stub import Flask_App_Stub
from app.routes.endpoint import Endpoint
from app.dbhandler import UserRepository # For fetching user role
from app.item_dbhandler import ItemRepository
from app.function import dateCounter, getUnreadCount
from app.swap_dbhandler import SwapRepository

# Import Item and Swap models for querying
from app.models.item import Item
from app.models.swap import Swap
# Ensure db is available if your models need it for queries,
# though usually it's accessed via Model.query
# from app.extensions import db

class Dashboard(Endpoint):
    def __init__(self, app: Flask_App_Stub) -> None:
        super().__init__(app)

        self.route = '/dashboard'
        self.endpoint = 'dashboard'
        self.callback = self.dashboard
        self.methods = ['GET'] # Dashboards are typically loaded via GET

    def dashboard(self):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('login'))

        current_user_id = session['user_id']

        # --- Items for "Discover" tab ---
        items_for_display_query = Item.query.filter(
            Item.user_id != current_user_id,
            Item.status == 'available',
            Item.approval != 'rejected',
            Item.approval != 'pending',
            Item.status != 'deleted',
            Item.status != 'swapping',
            Item.status != 'requested'
        )

        user_dbhandler = UserRepository(self.flask_app)
        user = user_dbhandler.query_user(session.get('username'))

        if user:
            # user_role = user.role
            two_days_ago = dateCounter()

            # if user_role != 'special' and user_role != 'special student':
            items_for_display_query = items_for_display_query.filter(Item.timestamp <= two_days_ago)

            items_for_display = items_for_display_query.all()

        # --- Swaps for "My Swaps" tab ---
        incoming_swap_requests = Swap.query \
            .join(Item, Swap.item_id == Item.id) \
            .filter(Item.user_id == current_user_id) \
            .filter(Item.status != 'deleted') \
            .all()
        
        # Get swaps where user is the requester
        outgoing_swap_requests = Swap.query \
            .filter(Swap.user_id == current_user_id) \
            .all()
        
        # Combine both types of swaps
        merged_swaps = incoming_swap_requests + outgoing_swap_requests
        
        item_dbhandler = ItemRepository(self.flask_app)
        swap_dbhandler = SwapRepository(self.flask_app)
        all_my_items = item_dbhandler.get_user_items(session.get('user_id'))
        my_items_for_display = [item for item in all_my_items if item.status != 'deleted' and item.approval != 'rejected']

        all_item = item_dbhandler.get_available_items()

        item_count = item_dbhandler.get_available_items_count()
        shared_item_count = item_dbhandler.get_shared_item_count(current_user_id)

        swap_completed_count = swap_dbhandler.get_swap_completed_count(current_user_id)

        context = {
            'username': session.get('username', 'User'),
            'items': items_for_display,
            'swaps': merged_swaps,
            'myItems': my_items_for_display,
            'itemCount': item_count,
            'completedSwap': swap_completed_count,
            'sharedItemCount': shared_item_count,
            'allItems': all_item,
            'user': user
        }

        user_id = session['user_id']
        total_unread = getUnreadCount(self.flask_app, user_id)

        return render_template('dashboard.html', **context, total_unread=total_unread)
