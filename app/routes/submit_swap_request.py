from flask import request, flash, redirect, url_for, session
from app.app_stub import Flask_App_Stub
from app.models.item import Item
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

            # Create a new swap
            swap_item = Swap(
                item_id=item.id,
                user_id=session['user_id'],  # Assuming user_id is stored in session
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
            if updated_swap.status == 'pending':
                flash('Your swap request has been submitted successfully.', 'success')
            else:
                flash('An unexpected error occurred while updating the swap status.', 'danger')

            # Redirect to the dashboard
            return redirect(url_for('dashboard'))

        except Exception as e:
            db.session.rollback()
            flash('An error occurred while submitting your swap request. Please try again.', 'danger')
            return redirect(url_for('dashboard'))

        return redirect(url_for('dashboard'))