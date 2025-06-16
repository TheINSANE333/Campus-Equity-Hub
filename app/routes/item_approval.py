import os
import uuid
from flask import render_template, request, url_for, flash, session, redirect
from app.app_stub import Flask_App_Stub
from app.item_dbhandler import ItemRepository
from app.routes.endpoint import Endpoint
from app.function import getUnreadCount

class ItemApproval(Endpoint):
    def __init__(self, app: Flask_App_Stub) -> None:
        super().__init__(app)

        self.route = '/item_approval'
        self.endpoint = 'item_approval'
        self.callback = self.item_approval
        self.methods = ['GET', 'POST']

    def item_approval(self):
        item_dbHandler = ItemRepository(self.flask_app)

        approval = item_dbHandler.get_pending_items()

        user_id = session['user_id']
        total_unread = getUnreadCount(self.flask_app, user_id)

        return render_template('item_approval.html', approval=approval, total_unread=total_unread)
