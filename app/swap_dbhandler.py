from datetime import datetime

from flask import flash, redirect, url_for
from app.app_stub import Flask_App_Stub
from app.extensions import db
from app.models.item import Item
from abc import ABC, abstractmethod
from app.models.swap import Swap
from typing import List

class DbHandler(ABC):
    _instance = None

    def __new__(cls, app: Flask_App_Stub = None):
        if cls._instance is None:
            if app is None:
                raise ValueError("App must be provided when initializing DbHandler for the first time")
            cls._instance = super(DbHandler, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, app: Flask_App_Stub) -> None:
        if self._initialized:
            return

        if app is None:
            raise ValueError("App must be provided when initializing DbHandler for the first time")

        self.flask_app = app
        self.db = app.db
        self.bcrypt = app.bcrypt

class SwapRepository(DbHandler):
    def query_swap(self, swap_id: str) -> Swap:
        return Swap.query.get_or_404(swap_id)

    def get_pending_swaps_count(self, user_id: int) -> int:
        from app.models.item import Item
        return Swap.query.join(
            Item, Swap.target_item_id == Item.id
        ).filter(
            Item.user_id == user_id,  # User owns the target item
            Swap.status == 'pending'  # Swap is pending
        ).count()

    def get_incoming_swap_request(self, current_user_id):
          return Swap.query \
                .join(Item, Swap.item_id == Item.id) \
                .filter(Item.user_id == current_user_id) \
                .filter(Item.status != 'deleted') \
                .all()

    def get_outgoing_swap_request(self, current_user_id):
        return Swap.query \
            .filter(Swap.user_id == current_user_id) \
            .all()

    def count_pending_incoming_swaps(self, current_user_id):
        return Swap.query \
            .join(Item, Swap.item_id == Item.id) \
            .filter(Item.user_id == current_user_id) \
            .filter(Swap.status == 'pending') \
            .filter(Item.status != 'deleted') \
            .count()

    def count_pending_outgoing_swaps(self, current_user_id):
        return Swap.query \
            .filter(Swap.user_id == current_user_id) \
            .filter(Swap.status == 'pending') \
            .count()

    def get_requester_swaps(self, user_id):
        return Swap.query.filter(Swap.user_id == user_id).all()
    
    def get_incoming_swap_request(self, current_user_id):
        return Swap.query \
            .join(Item, Swap.item_id == Item.id) \
            .filter(Item.user_id == current_user_id) \
            .filter(Item.status != 'deleted') \
            .all()

    def get_all_swaps_ordered_by_time_desc(self, swap_ids):
        if isinstance(swap_ids, list):
            ids = [swap.id for swap in swap_ids]
            return Swap.query.filter(Swap.id.in_(ids)).order_by(Swap.dealTime.desc()).all()
        return swap_ids.order_by(Swap.dealTime.desc()).all()

    def get_target_item_swaps(self, user_id):
        return Swap.query.join(Item, Swap.target_item_id == Item.id).filter(Item.user_id == user_id).all()

    def query_swap_id(self, user_id):
        return Swap.query.filter(
            (Swap.user_id == user_id) | (Swap.target_item.has(user_id=user_id))
        ).all()
    def get_item_status(self, swap_item: Swap):
        return Swap.query.filter_by(id=swap_item.id).first()

    def item_verify_status(self, updated_swap):
        if updated_swap and updated_swap.status == 'pending':
            flash('Your swap request has been submitted successfully.', 'success')
        else:
            flash('An unexpected error occurred while updating the swap status.', 'danger')
            # Rollback if verification fails to ensure data consistency
            db.session.rollback()

    # Find pending swaps where the deleted item was the primary item (swap.item_id)
    def get_swaps_to_update(self, item_to_delete) :
        return  Swap.query.filter(
            Swap.item_id == item_to_delete.id,
            Swap.status == 'pending'  # Consider only active pending swaps
        ).all()

    # The "requested user's item" (swap.target_item_id) should revert to 'available'.
    def update_status(self, item_to_delete, item) -> None:
        for swap in item_to_delete:
            # Update the status of the "requested user's item"
            if swap.target_item_id:
                target_item_of_swap = item.query_item(swap.target_item_id)
                if target_item_of_swap and target_item_of_swap.status == 'swapping':
                    target_item_of_swap.status = 'available'
                    self.db.session.add(target_item_of_swap)

            # Update the swap record itself
            swap.status = 'deleted'  # Changed from 'cancelled_item_unavailable'
            self.db.session.add(swap)

        self.db.session.commit()
        flash('Item deleted successfully. Related pending swaps have been updated.', 'success')
    # Update swap status after a swap is done or rejected

    def get_eligible_item(self, all_my_items: List[Item]) -> List[Item]:
        return [
            item for item in all_my_items
            if item.status == 'available' and item.approval == 'approved'
        ]

    def check_item_available(self, item):
        if item.status != 'available':
            flash('This item is no longer available for swap.', 'danger')
            return redirect(url_for('dashboard'))

        return True

    def get_swap_item(self, item, target_item, current_user_id, description, user) -> Swap:
        return Swap(
            item_id=item.id,
            user_id=current_user_id,
            item_name=item.name,  # Add item_name
            username=user.username,  # Add username
            status='pending',
            date=datetime.now(),
            swap_description=description,
            target_item_id=target_item.id,
            target_item_name=target_item.name
        )

    def update_all_item_status(self, item):
        db.session.add(item)
        db.session.commit()

    def update_swap_status(self, swap, status) -> None:
        swap.status = status
        self.db.session.add(swap)
        self.db.session.commit()

    def update_location(self, swap, location):
        swap.dealLocation = location
        self.db.session.add(swap)
        self.db.session.commit()

    def update_time(self, swap, time):
        swap.dealTime = time
        self.db.session.add(swap)
        self.db.session.commit()

    def get_swap_completed_count(self, user_id) -> List[Item]:
        return Swap.query.join(Item, Swap.item_id == Item.id).filter(self.db.or_(
            self.db.and_(Swap.user_id==user_id, Swap.status=='accepted'),
            self.db.and_(Item.user_id==user_id, Swap.status=='accepted')
        )).count()
    
    def get_swap_completed(self, user_id) -> List[Item]:
        return Swap.query.join(Item, Swap.item_id == Item.id).filter(self.db.or_(
            self.db.and_(Swap.user_id==user_id, Swap.status=='accepted'),
            self.db.and_(Item.user_id==user_id, Swap.status=='accepted')
        )).all()

