from flask import jsonify, session, render_template, request
from app.app_stub import Flask_App_Stub
from app.routes.endpoint import Endpoint
from app.swap_dbhandler import SwapRepository
from app.item_dbhandler import ItemRepository

class ViewSwapHistory(Endpoint):
    def __init__(self, app: Flask_App_Stub) -> None:
        super().__init__(app)

        self.route = '/view_swap_history'
        self.endpoint = 'view_swap_history'
        self.callback = self.view_swap_history
        self.methods = ['GET']

    def view_swap_history(self):
        user_id = session.get('user_id')

        item_repository = ItemRepository(self.flask_app)
        swap_repository = SwapRepository(self.flask_app)

        requester_swaps = swap_repository.get_requester_swaps(user_id)
        target_item_swaps = swap_repository.get_target_item_swaps(user_id)

        # Combine lists and pass to the function
        combined_swaps = list(set(requester_swaps + target_item_swaps))  # Removes duplicates
        all_swaps = swap_repository.get_all_swaps_ordered_by_time_desc(combined_swaps)

        swap_history = []
        for swap in all_swaps:
            item = item_repository.query_item(swap.item_id)
            target_item = item_repository.query_item(swap.target_item_id)

            is_requester = (swap.user_id == user_id)

            if is_requester:
                display_item_name = swap.item_name
                swap_with_username = item.user.username if item else 'Unknown'
                item_context = "Item you want"
            else:
                display_item_name = swap.target_item_name
                swap_with_username = swap.username
                item_context = "Your item"

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
