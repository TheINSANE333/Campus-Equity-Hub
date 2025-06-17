import os
import uuid
from flask import render_template, request, url_for, flash, session, redirect
from app.app_stub import Flask_App_Stub
from app.item_dbhandler import ItemRepository
from app.routes.endpoint import Endpoint
from app.function import allowed_file, getUnreadCount

class ViewItem(Endpoint):
    def __init__(self, app: Flask_App_Stub) -> None:
        super().__init__(app)

        self.route = '/item/<int:item_id>'
        self.endpoint = 'view_item'
        self.callback = self.view_item
        self.methods = ['GET', 'POST']

    def view_item(self, item_id):
        item_dbHandler = ItemRepository(self.flask_app)

        item = item_dbHandler.query_item(item_id)

        user_id = c
        total_unread = getUnreadCount(self.flask_app, user_id)
        return render_template('view_item.html', item=item, total_unread=total_unread)