from app.app_stub import Flask_App_Stub
from app.routes.endpoint import Endpoint
from flask import flash, redirect, url_for, render_template
from app.models.item import Item
from app.extensions import db  # Assuming db is initialized in your Flask app


class DeleteItem(Endpoint):
    def __init__(self, app: Flask_App_Stub) -> None:
        super().__init__(app)

        self.route = '/delete_item/<int:item_id>'
        self.endpoint = 'delete_item'
        self.callback = self.delete_item
        self.methods = ['POST']

    def delete_item(self, item_id):
        item_to_delete = Item.query.get(item_id)
        try:
            item_to_delete.status = 'deleted'  # Update status to 'deleted'
            db.session.add(item_to_delete)    # Add the updated item to the session
            db.session.commit()               # Commit the changes
            flash('Item status updated to "deleted" successfully.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating item status: {str(e)}', 'danger')
