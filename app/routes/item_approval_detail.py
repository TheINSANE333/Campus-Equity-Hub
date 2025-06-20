from flask import render_template, url_for, flash, session, redirect
from app.app_stub import Flask_App_Stub
from app.item_dbhandler import ItemRepository
from app.routes.endpoint import Endpoint

class ItemApprovalDetail(Endpoint):
    def __init__(self, app: Flask_App_Stub) -> None:
        super().__init__(app)

        self.route = '/item_approval_detail/<int:item_id>'
        self.endpoint = 'item_approval_detail'
        self.callback = self.item_approval_detail
        self.methods = ['GET', 'POST']

    def item_approval_detail(self, item_id):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('login'))
        
        if session['role'] != "admin":
            flash ('Please log in as admin to access this page.', 'danger')
            return redirect(url_for('login'))
        
        item_dbHandler = ItemRepository(self.flask_app)

        item = item_dbHandler.query_item(item_id)

        return render_template('item_approval_detail.html', item=item)