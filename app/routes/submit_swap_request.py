from flask import request, flash, redirect, url_for, session
from app.app_stub import Flask_App_Stub
from app.models.item import Item
from app.models.user import User # Import the User model
from app.extensions import db
from datetime import datetime
from app.routes.endpoint import Endpoint
from app.models.swap import Swap

class SubmitSwapRequest(Endpoint):
    def __init__(self, app: Flask_App_Stub) -> None:
        super().__init__(app)

        self.route = '/submit_swap_request/<int:item_id>'
        self.endpoint = 'submit_swap_request'
        self.callback = self.submit_swap_request
        self.methods = ['POST']

    def submit_swap_request(self, item_id):
        # Find the item to be swapped
        item = Item.query.get_or_404(item_id)

        # Check if the item is available for swap
        if item.status != 'available':
            flash('This item is no longer available for swap.', 'danger')
            return redirect(url_for('dashboard'))

        try:
            # Get the description from the form
            description = request.form.get('description')

            # Get the current user
            current_user_id = session.get('user_id')
            if not current_user_id:
                flash('User not logged in.', 'danger')
                return redirect(url_for('login')) # Or your login route

            user = User.query.get(current_user_id)
            if not user:
                flash('User not found.', 'danger')
                return redirect(url_for('dashboard'))

            # Create a new swap
            swap_item = Swap(
                item_id=item.id,
                user_id=current_user_id,
                item_name=item.name,  # Add item_name
                username=user.username,  # Add username
                status='pending',
                date=datetime.now(),
                swap_description=description
            )

            # Update the item status to "requested"
            item.status = 'requested'

            # Add the swap item to the database
            db.session.add(swap_item)
            db.session.commit()

            # Verify the status update
            updated_swap = Swap.query.filter_by(id=swap_item.id).first()
            if updated_swap and updated_swap.status == 'pending':
                flash('Your swap request has been submitted successfully.', 'success')
            else:
                flash('An unexpected error occurred while updating the swap status.', 'danger')
                # Rollback if verification fails to ensure data consistency
                db.session.rollback()


            # Redirect to the dashboard
            return redirect(url_for('dashboard'))

        except Exception as e:
            db.session.rollback()
            # For debugging, you might want to log the error e
            # import logging
            # logging.error(f"Error submitting swap request: {e}")
            flash('An error occurred while submitting your swap request. Please try again.', 'danger')
            return redirect(url_for('dashboard'))

        # This line is likely unreachable due to the try/except block always redirecting.
        # However, if it were reachable, it should probably redirect to a more specific page
        # or the same page with an error if the try block was not entered.
        return redirect(url_for('dashboard'))