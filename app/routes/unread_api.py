from flask import session, jsonify
from app.app_stub import Flask_App_Stub
from app.routes.endpoint import Endpoint
from app.chat_dbhandler import ChatRepository
class UnreadApi(Endpoint):
    def __init__(self, app: Flask_App_Stub) -> None:
        super().__init__(app)

        self.route = '/api/messages/unread-counts'
        self.endpoint = 'unread_api'
        self.callback = self.get_unread_counts
        self.methods = ['GET', 'POST']

    def get_unread_counts(self):
        if 'user_id' not in session:
            return jsonify({'error': 'Not authenticated'}), 401

        current_user_id = session['user_id']

        # Get unread message counts
        chat_dbhandler = ChatRepository(self.flask_app)
        unread_counts = chat_dbhandler.get_unread_counts(current_user_id)

        unread_by_user = {str(sender_id): count for sender_id, count in unread_counts}
        total_unread = sum(unread_by_user.values())

        return jsonify({
            'by_user': unread_by_user,
            'total': total_unread
        })