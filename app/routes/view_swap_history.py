from flask import jsonify, session, render_template, request
from flask_login import login_required
from app.models.swap import Swap
from app.models.item import Item
import datetime
from app.app_stub import Flask_App_Stub
from app.routes.endpoint import Endpoint
from app.function import getUnreadCount

class ViewSwapHistory(Endpoint):
    def __init__(self, app: Flask_App_Stub) -> None:
        super().__init__(app)

        self.route = '/swap-history'
        self.endpoint = 'view_swap_history'
        self.callback = self.view_swap_history
        self.methods = ['GET']

    def view_swap_history(self):
        user_id = session.get('user_id')

        # Base query - find swaps where the current user is involved
        # either as requester or item owner
        requester_swaps = Swap.query.filter(Swap.user_id == user_id)

        # Get swaps where the user is the item owner (uploader)
        uploader_swaps = Swap.query.join(Item, Swap.item_id == Item.id).filter(Item.user_id == user_id)

        # Combine both query results
        all_swaps = requester_swaps.union(uploader_swaps)

        # Execute query and order by dealTime (most recent first)
        swaps = all_swaps.order_by(Swap.dealTime.desc()).all()

        # Format swap data for display
        swap_history = []
        for swap in swaps:
            # Get the item details
            item = Item.query.get(swap.item_id)

            # Determine if current user is the requester
            is_requester = (swap.user_id == user_id)

            # If user is requester, show the item uploader's username
            # If user is uploader, show the requester's username
            if is_requester:
                # Get item uploader username
                swap_with_username = item.user.username
            else:
                # Get requester username
                swap_with_username = swap.username

            swap_data = {
                'id': swap.id,
                'item_name': swap.item_name,
                'dealTime': swap.dealTime.strftime('%Y-%m-%d %H:%M:%S') if swap.dealTime else 'Not scheduled',
                'status': swap.status.capitalize(),
                'swap_with_username': swap_with_username,
                'is_requester': is_requester
            }
            swap_history.append(swap_data)

            user_id = session['user_id']
            total_unread = getUnreadCount(self.flask_app, user_id)

        return render_template('swap_history.html', swaps=swap_history, total_unread=total_unread)