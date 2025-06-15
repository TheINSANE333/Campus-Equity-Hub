from flask import render_template, request, flash, redirect, url_for, session, jsonify
from app.app_stub import Flask_App_Stub
from app.routes.endpoint import Endpoint
from app.item_dbhandler import ItemRepository

class SearchApi(Endpoint):
    def __init__(self, app: Flask_App_Stub) -> None:
        super().__init__(app)

        self.route = '/api/item-search'
        self.endpoint = 'search_api'
        self.callback = self.item_search_api
        self.methods = ['GET', 'POST']

    def item_search_api(self):
        query = request.args.get('query', '')
        item_dbhandler = ItemRepository(self.flask_app)
        
        if query:
            # Search for campuses that match the query (case-insensitive)
            items = item_dbhandler.find_item(query)
            
            # Format results for JSON response
            results = [
                {
                    'id': item.id,
                    'name': item.name,
                    'text': item.name
                }
                for item in items
            ]
        else:
            # Return empty results if no query provided
            results = []
        
        return jsonify(results)

