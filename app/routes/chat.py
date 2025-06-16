from flask import render_template, request, flash, redirect, url_for, session
from app.app_stub import Flask_App_Stub
from app.routes.endpoint import Endpoint
from app.chat_dbhandler import ChatRepository
from app.dbhandler import UserRepository

class Chat(Endpoint):
    def __init__(self, app: Flask_App_Stub) -> None:
        super().__init__(app)

        self.route = '/chat'
        self.endpoint = 'chat'
        self.callback = self.chat
        self.methods = ['GET', 'POST']

    def chat(self):
        if 'user_id' not in session:
            flash('Please log in to access the chat.', 'danger')
            return redirect(url_for('login'))
        
        # Get all users except the current user
        dbHandler = UserRepository(self.flask_app)
        user_id = session['user_id']
        users = dbHandler.get_all_users(user_id)
        
        # Get unread message counts for navbar indicator
        chat_dbHandler = ChatRepository(self.flask_app)
        unread_counts = chat_dbHandler.get_unread_counts(user_id)
        
        unread_by_user = {sender_id: count for sender_id, count in unread_counts}
        total_unread = chat_dbHandler.get_total_unread(user_id)
        
        return render_template('chat.html', users=users, unread_by_user=unread_by_user, total_unread=total_unread   )
