from app.app_stub import Flask_App_Stub
from app.routes.endpoint import Endpoint
from flask import flash, redirect, url_for, render_template
from app.item_dbhandler import ItemRepository
from app.extensions import db
from app.swap_dbhandler import SwapRepository
from app.models.item import Item


class DeleteItem(Endpoint):
    def __init__(self, app: Flask_App_Stub) -> None:
        super().__init__(app)

        self.route = '/delete_item/<int:item_id>'
        self.endpoint = 'delete_item'
        self.callback = self.delete_item
        self.methods = ['POST']

    def delete_item(self, item_id):
        item_dbhandler = ItemRepository(self.flask_app)
        swap_dbhandler = SwapRepository(self.flask_app)
        item_to_delete = item_dbhandler.query_item(item_id)

        if not item_to_delete:
            flash('Item not found.', 'danger')
            return redirect(url_for('dashboard'))

        try:
            swaps_to_update = swap_dbhandler.get_swaps_to_update(item_to_delete)
            item_dbhandler.set_item_status(item_to_delete, 'deleted')
            swap_dbhandler.update_status(swaps_to_update, item_dbhandler)

        except Exception as e:
            db.session.rollback()
            flash(f'Error updating item status or related swaps: {str(e)}', 'danger')

        return redirect(url_for('dashboard'))