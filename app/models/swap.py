from datetime import datetime
from app.extensions import db

class Swap(db.Model):
    __tablename__ = 'swaps'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    item_name = db.Column(db.String(255), nullable=False)
    target_item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    target_item_name = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.String(20), default='pending') # accepted, rejected, pending
    swap_description = db.Column(db.String(255), nullable=True)
    username = db.Column(db.String(255), db.ForeignKey('users.username'), nullable=False)
    dealLocation = db.Column(db.String(255), nullable=True)
    dealTime = db.Column(db.DateTime, nullable=True)

    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], backref='swaps_requested_users')
    item = db.relationship('Item', foreign_keys=[item_id], backref='swaps_items')
    target_item = db.relationship('Item', foreign_keys=[target_item_id], backref='swaps_target_items')

    def __repr__(self):
        return f'<Swap {self.id} - User {self.user_id} - Item {self.item_id}>'

    def to_dict(self, current_user_id=None):
        # Get the target item's owner username
        target_user_username = self.target_item.user.username if self.target_item and self.target_item.user else 'Unknown'

        # Debug: Print current user and swap details
        print(f"Current user ID: {current_user_id}")
        print(f"Swap requester ID: {self.user_id}")
        print(f"Target item owner ID: {self.target_item.user_id if self.target_item else 'None'}")
        print(f"Item name: {self.item_name}")
        print(f"Target item name: {self.target_item_name}")

        # Determine what item to show based on user perspective
        if current_user_id:
            # If current user is the requester, show target item name (what they want to get)
            if current_user_id == self.user_id:
                display_item_name = self.target_item_name
                swap_with_username = target_user_username
                print(f"User is requester - showing target item: {display_item_name}")
            # If current user is the target item owner, show item name (what they're being asked to trade)
            elif self.target_item and current_user_id == self.target_item.user_id:
                display_item_name = self.item_name
                swap_with_username = self.user.username
                print(f"User is target owner - showing requested item: {display_item_name}")
            else:
                # Fallback
                display_item_name = self.item_name
                swap_with_username = target_user_username
                print(f"Fallback case - showing item: {display_item_name}")
        else:
            # Default behavior if no current_user_id provided
            display_item_name = self.item_name
            swap_with_username = target_user_username
            print(f"No current user - default showing: {display_item_name}")

        return {
            'id': self.id,
            'user_id': self.user_id,
            'item_id': self.item_id,
            'date': self.date.strftime('%Y-%m-%d %H:%M:%S'),
            'status': self.status,
            'swap_description': self.swap_description,
            'username': self.user.username,  # Person who initiated the swap
            'swap_with_username': swap_with_username,  # Person they want to swap with
            'item_name': display_item_name,  # Item shown based on user perspective
            'original_item_name': self.item_name,  # Original item being offered
            'target_item_id': self.target_item_id,
            'target_item_name': self.target_item_name,  # Target item being requested
            'dealLocation': self.dealLocation,
            'dealTime': self.dealTime.strftime('%Y-%m-%d %H:%M:%S') if self.dealTime else None
        }