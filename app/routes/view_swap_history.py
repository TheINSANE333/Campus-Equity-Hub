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

        self.route = '/swap_history'
        self.endpoint = 'view_swap_history'
        self.callback = self.view_swap_history
        self.methods = ['GET']

    def view_swap_history(self):
        user_id = session.get('user_id')

        # Base query - find swaps where the current user is involved
        # Case 1: User is the requester (user_id matches swap.user_id)
        requester_swaps = Swap.query.filter(Swap.user_id == user_id)

        # Case 2: User owns the target item (the item being requested)
        target_item_swaps = Swap.query.join(Item, Swap.target_item_id == Item.id).filter(Item.user_id == user_id)

        # Combine both query results
        all_swaps = requester_swaps.union(target_item_swaps)

        # Execute query and order by dealTime (most recent first)
        swaps = all_swaps.order_by(Swap.dealTime.desc()).all()

        # Format swap data for display
        swap_history = []
        for swap in swaps:
            print(f"=== Debug Swap ID: {swap.id} ===")
            print(f"Current user_id: {user_id}")
            print(f"Swap requester user_id: {swap.user_id}")
            print(f"Swap item_name: {swap.item_name}")
            print(f"Swap target_item_name: {swap.target_item_name}")

            # Get the item details
            item = Item.query.get(swap.item_id)
            target_item = Item.query.get(swap.target_item_id)

            print(f"Item owner user_id: {item.user_id if item else 'None'}")
            print(f"Target item owner user_id: {target_item.user_id if target_item else 'None'}")

            # Determine if current user is the requester
            is_requester = (swap.user_id == user_id)
            print(f"Is requester: {is_requester}")

            # Determine which item to show based on user perspective
            if is_requester:
                # User is the requester - show the item they want to GET (the offered item)
                display_item_name = swap.item_name
                # Show who they're swapping with (owner of the item they want)
                swap_with_username = item.user.username if item else 'Unknown'
                item_context = "Item you want"
                print(f"Requester view - showing desired item: {display_item_name}, swapping with: {swap_with_username}")
            else:
                # User owns the target item - show their item being requested
                display_item_name = swap.target_item_name
                # Show who wants to swap with them (the requester)
                swap_with_username = swap.username
                item_context = "Your item"
                print(f"Target owner view - showing their item: {display_item_name}, swapping with: {swap_with_username}")

            print("=" * 30)

            swap_data = {
                'id': swap.id,
                'item_name': display_item_name,
                'dealTime': swap.dealTime.strftime('%Y-%m-%d %H:%M:%S') if swap.dealTime else 'Not scheduled',
                'status': swap.status.capitalize(),
                'swap_with_username': swap_with_username,
                'is_requester': is_requester,
                'item_context': item_context
            }
            swap_history.append(swap_data)

        return render_template('swap_history.html', swaps=swap_history)