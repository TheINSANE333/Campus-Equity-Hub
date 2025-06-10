from datetime import datetime, UTC
from app.extensions import db
from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger(__name__)

class Swap(db.Model):
    """Swap model representing item exchange requests between users"""
    __tablename__ = 'swaps'

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    requester_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='pending', nullable=False)
    request_message = db.Column(db.Text)
    admin_decision = db.Column(db.String(20))
    admin_notes = db.Column(db.Text)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))
    admin_decided_at = db.Column(db.DateTime)

    # Relationships
    item = db.relationship('Item', backref='swap_requests')
    requester = db.relationship('User', foreign_keys=[requester_id], backref='swap_requests_made')
    owner = db.relationship('User', foreign_keys=[owner_id], backref='swap_requests_received')
    admin = db.relationship('User', foreign_keys=[admin_id])

    def approve_by_admin(self, admin_user, notes=None):
        """Approve this swap request by admin"""
        if not admin_user.is_admin:
            raise ValueError("Only admin users can approve swaps")

        try:
            self.status = 'approved'
            self.admin_decision = 'approved'
            self.admin_notes = notes
            self.admin_id = admin_user.id
            self.admin_decided_at = datetime.now(UTC)
            db.session.commit()
            logger.info(f"Swap {self.id} approved by admin {admin_user.id}. Notes: {notes}")
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Failed to approve swap {self.id}: {str(e)}")
            raise e

    def reject_by_admin(self, admin_user, notes=None):
        """Reject this swap request by admin"""
        if not admin_user.is_admin:
            raise ValueError("Only admin users can reject swaps")

        try:
            self.status = 'rejected'
            self.admin_decision = 'rejected'
            self.admin_notes = notes
            self.admin_id = admin_user.id
            self.admin_decided_at = datetime.now(UTC)
            db.session.commit()
            logger.info(f"Swap {self.id} rejected by admin {admin_user.id}. Notes: {notes}")
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Failed to reject swap {self.id}: {str(e)}")
            raise e

    def to_dict(self):
        """Serialize swap object to dictionary"""
        return {
            'id': self.id,
            'item_id': self.item_id,
            'requester_id': self.requester_id,
            'owner_id': self.owner_id,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'admin_decision': self.admin_decision,
            'admin_decided_at': self.admin_decided_at.isoformat() if self.admin_decided_at else None
        }

    def __repr__(self):
        return f'<Swap {self.id} - {self.status}>'
