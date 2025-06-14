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
    status = db.Column(db.String(20), default='pending')
    swap_description = db.Column(db.String(255), nullable=True)
    username = db.Column(db.String(255), db.ForeignKey('users.username'), nullable=False)

    # Explicitly specify the foreign keys for the relationships
    user = db.relationship('User', foreign_keys=[user_id], backref='swaps_requested_users')
    item = db.relationship('Item', foreign_keys=[item_id], backref='swaps_items')

    def __repr__(self):
        return f'<Swap {self.id} - User {self.user_id} - Item {self.item_id}>'
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'item_id': self.item_id,
            'date': self.date.strftime('%Y-%m-%d %H:%M:%S'),
            'status': self.status,
            'swap_description': self.swap_description,
            'username': self.user.username,
            'item_name': self.item.name,
            'target_item_id': self.target_item_id,
            'target_item_name': self.target_item_name
        }