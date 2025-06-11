from app.extensions import db

class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    read = db.Column(db.Boolean, default=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_notifications')
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_notifications')
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    notification_type = db.Column(db.String(20), default='system')
    title = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f'<Notification {self.name}>'
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'message': self.message,
            'read': self.read,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'type': self.notification_type,
            'receiver_id': self.receiver_id,
            'sender_id': self.sender_id,
            'sender_name': self.sender.username,
            'receiver_name': self.receiver.username
        }

    def mark_as_read(self):
        self.read = True
        db.session.commit()
        return self.to_dict()