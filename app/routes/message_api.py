from flask import request, session, jsonify
from app.app_stub import Flask_App_Stub
from app.routes.endpoint import Endpoint
from app.chat_dbhandler import ChatRepository

class MessageApi(Endpoint):
    def __init__(self, app: Flask_App_Stub) -> None:
        super().__init__(app)

        self.route = '/api/messages/<int:user_id>'
        self.endpoint = 'message_api'
        self.callback = self.get_new_message
        self.methods = ['GET', 'POST']

    def get_new_message(self, user_id):
        if 'user_id' not in session:
            return jsonify({'error': 'Not authenticated'}), 401
    
        current_user_id = session['user_id']
        last_id = request.args.get('last_id', 0, type=int)
        
        # Get new messages that the current user hasn't seen yet
        chat_dbhandler = ChatRepository(self.flask_app)
        new_messages = chat_dbhandler.get_unread_messages(current_user_id, user_id, last_id)
        
        # Mark messages as read
        chat_dbhandler.mark_as_read_sender(new_messages, current_user_id)
        
        return jsonify([message.to_dict() for message in new_messages])