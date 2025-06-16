from flask import render_template, request, flash, redirect, url_for, session, jsonify
from app.app_stub import Flask_App_Stub
from app.routes.endpoint import Endpoint
from app.chat_dbhandler import ChatRepository
from app.dbhandler import UserRepository
from app.item_dbhandler import ItemRepository
from app.function import getUnreadCount

class ChatWithUser(Endpoint):
    def __init__(self, app: Flask_App_Stub) -> None:
        super().__init__(app)

        self.route = '/chat/<int:user_id>'
        self.endpoint = 'chat_with_user'
        self.callback = self.chat_with_user
        self.methods = ['GET', 'POST']

    def chat_with_user(self, user_id):
        if 'user_id' not in session:
            flash('Please log in to access the chat.', 'danger')
            return redirect(url_for('login'))
    
        current_user_id = session['user_id']
        item_id = request.args.get('item_id')
    
        # Check if the user exists
        user_dbhandler = UserRepository(self.flask_app)
        chat_dbhandler = ChatRepository(self.flask_app)
        chat_partner = user_dbhandler.query_user_id(user_id)

        item = None
        if item_id:
            item_dbhandler = ItemRepository(self.flask_app)  # Assuming you have an ItemRepository
            item = item_dbhandler.query_item(item_id)
    
        if request.method == 'POST':
            message = request.form.get('message')
        
            if message:
                # Create new chat message
                
                new_message = chat_dbhandler.create_message(current_user_id, user_id, message)

                # If AJAX request, return the new message as JSON
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return jsonify(new_message.to_dict())
            
            # For normal form submission, redirect back to the chat
            return redirect(url_for('chat_with_user', user_id=user_id))
    
        # Mark messages as read
        chat_dbhandler.mark_as_read(user_id, current_user_id)
    
        # Get all messages between the current user and the selected user
        messages = chat_dbhandler.get_all_message(user_id, current_user_id)
        
        # Get all users except the current user for the sidebar
        users = user_dbhandler.get_all_users(current_user_id)
        
        # Get unread message counts
        unread_counts = chat_dbhandler.get_unread_counts(current_user_id)
        
        unread_by_user = {sender_id: count for sender_id, count in unread_counts}

        total_unread = getUnreadCount(self.flask_app, current_user_id)
        
        return render_template(
            'chat_with_user.html',
            chat_partner=chat_partner,
            messages=messages,
            users=users,
            unread_by_user=unread_by_user, 
            total_unread=total_unread, 
            item=item
        )
