from flask import render_template, url_for, flash, session, redirect
from app.app_stub import Flask_App_Stub
from app.routes.endpoint import Endpoint
from app.item_dbhandler import ItemRepository
from app.function import dateCounter
from app.swap_dbhandler import SwapRepository
from app.dbhandler import UserRepository



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
        item_dbhandler = ItemRepository(self.flask_app)
        Item = item_dbhandler.query_item(current_user_id)

        items_for_display_query = item_dbhandler.item_to_display(current_user_id)

        user_dbhandler = UserRepository(self.flask_app)
        user = user_dbhandler.query_user(current_user_id)

        swap_dbhandler = SwapRepository(self.flask_app)
        swap = swap_dbhandler.query_swap(current_user_id)

        if user:
            # user_role = user.role
            two_days_ago = dateCounter()

            # if user_role != 'special' and user_role != 'special student':
            items_for_display_query = items_for_display_query.filter(Item.timestamp <= two_days_ago)

            items_for_display = items_for_display_query.all()

        incoming_swap_requests = swap_dbhandler.get_incoming_swap_request(current_user_id)
        outgoing_swap_requests = swap_dbhandler.get_outgoing_swap_request(current_user_id)
        merged_swaps = incoming_swap_requests + outgoing_swap_requests
        pending_incoming_swaps = swap_dbhandler.count_pending_incoming_swaps(current_user_id)
        pending_swaps_count = pending_incoming_swaps
        item_dbhandler = ItemRepository(self.flask_app)
        swap_dbhandler = SwapRepository(self.flask_app)
        all_my_items = item_dbhandler.get_user_items(session.get('user_id'))
        my_items_for_display = [item for item in all_my_items if item.status != 'deleted' and item.approval != 'rejected']

        all_items_temp = item_dbhandler.get_available_items()
        my_item_ids = {item.id for item in my_items_for_display}
        all_item = [item for item in all_items_temp if item.id not in my_item_ids]

        item_count = item_dbhandler.get_available_items_count()
        shared_item_count = item_dbhandler.get_shared_item_count(current_user_id)
        token_count = user_dbhandler.get_user_tokens(current_user_id)

        swap_completed_count = swap_dbhandler.get_swap_completed_count(current_user_id)
        context = {
            'username': session.get('username', 'User'),
            'swaps': merged_swaps,
            'myItems': my_items_for_display,
            'itemCount': item_count,
            'completedSwap': swap_completed_count,
            'sharedItemCount': shared_item_count,
            'allItems': all_item,
            'user': user,
            'PendingSwapsCount': pending_swaps_count,
            'tokenCount': token_count
        }

        return render_template('dashboard.html', **context)