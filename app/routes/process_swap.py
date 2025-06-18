from datetime import datetime
from flask import render_template, request, redirect, url_for, flash, session
from app.app_stub import Flask_App_Stub
from app.item_dbhandler import ItemRepository
from app.swap_dbhandler import SwapRepository
from app.routes.endpoint import Endpoint
from app.dbhandler import UserRepository
from app.extensions import db


class ProcessSwap(Endpoint):
    def __init__(self, app: Flask_App_Stub) -> None:
        super().__init__(app)

        self.route = '/process_swap/<int:swap_id>'
        self.endpoint = 'process_swap'
        self.callback = self.process_swap
        self.methods = ['POST']

    def process_swap(self, swap_id):
        action = request.form.get('action')

        swap_dbHandler = SwapRepository(self.flask_app)
        item_dbHandler = ItemRepository(self.flask_app)
        user_dbHandler = UserRepository(self.flask_app)

        try:
            swap = swap_dbHandler.query_swap(swap_id)
            item = item_dbHandler.query_item(swap.item_id)
            target = item_dbHandler.query_item(swap.target_item_id)

            requester_id = item.user_id
            owner_id = target.user_id

            requester = user_dbHandler.query_user_id(requester_id)
            owner = user_dbHandler.query_user_id(owner_id)

            if not requester or not owner:
                flash("One or more users could not be found.", "danger")
                return redirect(url_for('dashboard'))

            if action == 'accepted':
                location = request.form.get('location')
                time_str = request.form.get('trade_time')
                trade_time = datetime.strptime(time_str, '%Y-%m-%dT%H:%M')
                item_dbHandler.update_item_status(item, 'sold')
                item_dbHandler.update_item_status(target, 'sold')
                swap_dbHandler.update_swap_status(swap, 'accepted')
                swap_dbHandler.update_location(swap, location)
                swap_dbHandler.update_time(swap, trade_time)

                if requester_id == owner_id:
                    user_dbHandler.add_token(requester, 5)

                else:
                    user_dbHandler.add_token(requester, 5)
                    user_dbHandler.add_token(owner, 5)

                if item.category == 'Donate':
                    user_dbHandler.add_achievement_points(owner, 1)

                flash('Swap Accepted! Both users have been rewarded with tokens.', 'success')

            elif action == 'rejected':
                item_dbHandler.update_item_status(item, 'available')
                item_dbHandler.update_item_status(target, 'available')
                swap_dbHandler.update_swap_status(swap, 'rejected')
                flash('Swap Rejected!', 'info')

            else:
                flash('Unknown action received.', 'warning')
                return redirect(url_for('dashboard'))

        except Exception as e:

            db.session.rollback()
            flash('An error occurred while processing the swap. Please try again.', 'danger')
            print(f"[ERROR] {str(e)}")
            return redirect(url_for('dashboard'))

        context = {
            'swap': swap,
            'item': item,
            'target': target
        }

        return render_template('view_swap.html', **context)
