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
        return {
            'id': self.id,
            'user_id': self.user_id,
            'item_id': self.item_id,
            'date': self.date.strftime('%Y-%m-%d %H:%M:%S'),
            'status': self.status,
            'swap_description': self.swap_description,
            'username': self.user.username,  # Person who initiated the swap
            'original_item_name': self.item_name,  # Original item being offered
            'target_item_id': self.target_item_id,
            'target_item_name': self.target_item_name,  # Target item being requested
            'dealLocation': self.dealLocation,
            'dealTime': self.dealTime.strftime('%Y-%m-%d %H:%M:%S') if self.dealTime else None
        }