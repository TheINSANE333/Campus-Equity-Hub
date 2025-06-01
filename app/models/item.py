from datetime import datetime
from app.extensions import db

class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    image_filename = db.Column(db.String(255), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(20), default='available')  # available, sold, hidden, pending
    
    # Define relationship
    user = db.relationship('User', backref=db.backref('items', lazy=True))

    print("Item model created")
    
    def __repr__(self):
        return f'<Item {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'image_url': f'/static/uploads/{self.image_filename}' if self.image_filename else None,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'user_id': self.user_id,
            'category': self.category,
            'status': self.status,
            'seller': self.user.username
        }