from flask import render_template, request, flash, redirect, url_for, session, jsonify
from app.app_stub import Flask_App_Stub
from app.routes.endpoint import Endpoint
from app.chat_dbhandler import ChatRepository
from app.item_dbhandler import ItemRepository

class SearchApiItem(Endpoint):
    def __init__(self, app: Flask_App_Stub) -> None:
        super().__init__(app)

        self.route = '/api/item-search/<int:item_id>'
        self.endpoint = 'search_api_item'
        self.callback = self.item_details
        self.methods = ['GET', 'POST']

    def item_details(self, item_id):
        item_dbhandler = ItemRepository(self.flask_app)
        item = item_dbhandler.query_item(item_id)
        return jsonify({
            'id': item.id,
            'name': item.name,
        })

