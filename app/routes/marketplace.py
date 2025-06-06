import os
import uuid
from flask import render_template, request, url_for, flash, session, redirect
from app.app_stub import Flask_App_Stub
from app.item_dbhandler import ItemRepository
from app.routes.endpoint import Endpoint

class Marketplace(Endpoint):
    def __init__(self, app: Flask_App_Stub) -> None:
        super().__init__(app)

        self.route = '/marketplace'
        self.endpoint = 'marketplace'
        self.callback = self.marketplace
        self.methods = ['GET', 'POST']

    def marketplace(self):
        item_dbHandler = ItemRepository(self.flask_app)

        items = item_dbHandler.get_available_items()
        return render_template('marketplace.html', items=items)
