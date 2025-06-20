from flask import request, flash, redirect, url_for, session
from app.app_stub import Flask_App_Stub
from app.extensions import db
from app.routes.endpoint import Endpoint
from app.swap_dbhandler import SwapRepository
from app.item_dbhandler import ItemRepository
from app.dbhandler import UserRepository
from app.notification_dbhandler import NotificationRepository
from app.dbhandler import UserRepository

class SubmitSwapRequest(Endpoint):
    def __init__(self, app: Flask_App_Stub) -> None:
        super().__init__(app)

        self.route = '/submit_swap_request/<int:item_id>'
        self.endpoint = 'submit_swap_request'
        self.callback = self.submit_swap_request
        self.methods = ['POST']

    def submit_swap_request(self, item_id):
        # Find the item to be swapped
        item_dbhandler = ItemRepository(self.flask_app)
        swap_dbhandler = SwapRepository(self.flask_app)
        item = item_dbhandler.query_item(item_id)
        target_item_id = request.form['swapItem']
        target_item = item_dbhandler.query_item(target_item_id)
        notification_dbhandler = NotificationRepository(self.flask_app)
        user_dbhandler = UserRepository(self.flask_app)
        current_user = user_dbhandler.query_user_id(session.get('user_id'))

        swap_dbhandler.check_item_available(item)

        try:
            description = request.form.get('description')
            current_user_id = session.get('user_id')
            current_user_name = current_user.username
            if not current_user_id:
                flash('User not logged in.', 'danger')
                return redirect(url_for('login')) # Or your login route

            user_dbhandler = UserRepository(self.flask_app)
            user = user_dbhandler.query_user_id(current_user_id)

            if not user:
                flash('User not found.', 'danger')
                return redirect(url_for('dashboard'))

            swap_item = swap_dbhandler.get_swap_item(item, target_item, current_user_id, description, user)
            owner_id = item.user_id
            owner = user_dbhandler.query_user_id(owner_id)
            role_to_be_view = owner.role
            # item.status = 'requested'
            # target_item.status = 'swapping'
            swap_dbhandler.update_swap_status(item, 'requested')
            swap_dbhandler.update_swap_status(target_item, 'swapping')
            notification_dbhandler.create_notification(item.user_id, current_user_id, current_user_name, description, 'request swap', 'unread', role_to_be_view, f"Request For'{target_item}'")

            swap_dbhandler.update_all_item_status(swap_item)

            updated_swap = swap_dbhandler.get_item_status(swap_item)
            swap_dbhandler.item_verify_status(updated_swap)
            return redirect(url_for('dashboard'))

        except Exception as e:
            db.session.rollback()
            flash('An error occurred while submitting your swap request. Please try again.', 'danger')
            return redirect(url_for('dashboard'))
