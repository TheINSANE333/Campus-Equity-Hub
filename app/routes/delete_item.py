from app.app_stub import Flask_App_Stub
from app.routes.endpoint import Endpoint
from flask import flash, redirect, url_for, render_template
from app.models.item import Item
from app.extensions import db
from app.models.swap import Swap


class DeleteItem(Endpoint):
    def __init__(self, app: Flask_App_Stub) -> None:
        super().__init__(app)

        self.route = '/delete_item/<int:item_id>'
        self.endpoint = 'delete_item'
        self.callback = self.delete_item
        self.methods = ['POST']

    def delete_item(self, item_id):
        item_to_delete = Item.query.get(item_id)

        if not item_to_delete:
            flash('Item not found.', 'danger')
            return redirect(url_for('dashboard'))

        try:
            # Mark the item as 'deleted'
            item_to_delete.status = 'deleted'
            db.session.add(item_to_delete)

            # Find pending swaps where the deleted item was the primary item (swap.item_id)
            # The "requested user's item" (swap.target_item_id) should revert to 'available'.
            swaps_to_update = Swap.query.filter(
                Swap.item_id == item_to_delete.id,
                Swap.status == 'pending'  # Consider only active pending swaps
            ).all()

            for swap in swaps_to_update:
                # Update the status of the "requested user's item"
                if swap.target_item_id:
                    target_item_of_swap = Item.query.get(swap.target_item_id)
                    if target_item_of_swap and target_item_of_swap.status == 'swapping':
                        target_item_of_swap.status = 'available'
                        db.session.add(target_item_of_swap)

                # Update the swap record itself
                swap.status = 'deleted'  # Changed from 'cancelled_item_unavailable'
                db.session.add(swap)

            db.session.commit()
            flash('Item deleted successfully. Related pending swaps have been updated.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating item status or related swaps: {str(e)}', 'danger')

        return redirect(url_for('dashboard'))