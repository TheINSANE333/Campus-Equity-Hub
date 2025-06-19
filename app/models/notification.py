from app.extensions import db

class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    notification_type = db.Column(db.String(20), default='system')
    title = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(20), default='unread')
    role_to_be_view = db.Column(db.String(20), default='student')
    sender_name = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f'<Notification {self.name}>'
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'message': self.message,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'type': self.notification_type,
            'receiver_id': self.receiver_id,
            'sender_id': self.sender_id,
            'status': self.status,
            'role_to_be_view': self.role_to_be_view,
            'sender_name': self.sender_name
        }