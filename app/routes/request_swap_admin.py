from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models.swap import Swap
from app.extensions import db
from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('swap_admin', __name__, url_prefix='/api/admin/swaps')

@bp.route('/pending', methods=['GET'])
@login_required
def get_pending_swaps():
    """Get all pending swap requests requiring admin approval"""
    if not current_user.is_admin:
        logger.warning(f"Unauthorized access attempt to pending swaps by user {current_user.id}")
        return jsonify({
            'success': False,
            'error': 'Unauthorized access',
            'message': 'Only admin users can access this endpoint'
        }), 403

    try:
        pending_swaps = Swap.query.filter_by(status='pending').all()
        logger.info(f"Retrieved {len(pending_swaps)} pending swaps for admin {current_user.id}")
        return jsonify({
            'success': True,
            'count': len(pending_swaps),
            'swaps': [swap.to_dict() for swap in pending_swaps]
        })
    except SQLAlchemyError as e:
        logger.error(f"Database error while fetching pending swaps: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Database error',
            'message': str(e)
        }), 500

@bp.route('/<int:swap_id>/approve', methods=['POST'])
@login_required
def approve_swap(swap_id):
    """Approve a specific swap request"""
    if not current_user.is_admin:
        logger.warning(f"Unauthorized approval attempt for swap {swap_id} by user {current_user.id}")
        return jsonify({
            'success': False,
            'error': 'Unauthorized',
            'message': 'Only admin users can approve swaps'
        }), 403

    try:
        swap = Swap.query.get_or_404(swap_id)
        notes = request.json.get('notes', '')

        swap.approve_by_admin(current_user, notes)
        logger.info(f"Swap {swap_id} approved by admin {current_user.id}")
        return jsonify({
            'success': True,
            'message': 'Swap approved successfully',
            'swap': swap.to_dict()
        })
    except ValueError as e:
        logger.error(f"Validation error approving swap {swap_id}: {str(e)}")
        logger.error(f"Validation error rejecting swap {swap_id}: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Validation error',
            'message': str(e)
        }), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Database error',
            'message': str(e)
        }), 500

@bp.route('/<int:swap_id>/reject', methods=['POST'])
@login_required
def reject_swap(swap_id):
    """Reject a specific swap request"""
    if not current_user.is_admin:
        logger.warning(f"Unauthorized rejection attempt for swap {swap_id} by user {current_user.id}")
        return jsonify({
            'success': False,
            'error': 'Unauthorized',
            'message': 'Only admin users can reject swaps'
        }), 403

    try:
        swap = Swap.query.get_or_404(swap_id)
        notes = request.json.get('notes', '')

        swap.reject_by_admin(current_user, notes)
        logger.info(f"Swap {swap_id} rejected by admin {current_user.id}")
        return jsonify({
            'success': True,
            'message': 'Swap rejected successfully',
            'swap': swap.to_dict()
        })
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': 'Validation error',
            'message': str(e)
        }), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Database error',
            'message': str(e)
        }), 500

@bp.route('/<int:swap_id>', methods=['GET'])
@login_required
def get_swap_details(swap_id):
    """Get details of a specific swap request"""
    if not current_user.is_admin:
        logger.warning(f"Unauthorized view attempt for swap {swap_id} by user {current_user.id}")
        return jsonify({
            'success': False,
            'error': 'Unauthorized',
            'message': 'Only admin users can view swap details'
        }), 403

    try:
        swap = Swap.query.get_or_404(swap_id)
        logger.info(f"Swap {swap_id} details viewed by admin {current_user.id}")
        return jsonify({
            'success': True,
            'swap': swap.to_dict()
        })
    except SQLAlchemyError as e:
        return jsonify({
            'success': False,
            'error': 'Database error',
            'message': str(e)
        }), 500


class SwapAdmin:
    """Endpoint class for swap admin operations"""

    def __init__(self, app):
        self.app = app

    def register_endpoints3(self):
        """Register all swap admin endpoints with the Flask application"""
        self.app.app.register_blueprint(bp)