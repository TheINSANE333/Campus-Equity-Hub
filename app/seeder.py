from app.extensions import db, bcrypt
from datetime import datetime
from app.models.user import User
from app.models.item import Item

class DatabaseSeeder:
    """Handles database seeding operations."""
    
    def __init__(self, app):
        self.app = app
    
    def seed_admin_user(self):
        """Create default admin user if it doesn't exist."""
        with self.app.app_context():
            # Check if admin user already exists
            admin_user = User.query.filter_by(username='admin').first()
            
            if not admin_user:
                # Create admin user
                admin_password = bcrypt.generate_password_hash('admin123').decode('utf-8')
                admin = User(
                    username='admin', 
                    email='admin@example.com', 
                    password=admin_password,
                    role='admin', 
                    campus='MMU'
                )
                db.session.add(admin)
                db.session.commit()

    def seed_user_1(self):
        """Create default user if it doesn't exist."""
        with self.app.app_context():
            # Check if user1 already exists
            user_1 = User.query.filter_by(username='user1').first()
            
            if not user_1:
                # Create user1
                user_password = bcrypt.generate_password_hash('user1123').decode('utf-8')
                user1 = User(
                    username='user1', 
                    email='user1@example.com', 
                    password=user_password,
                    role='special', 
                    campus='MMU'
                )
                db.session.add(user1)
                db.session.commit()

    def seed_user_2(self):
        """Create default user if it doesn't exist."""
        with self.app.app_context():
            # Check if user1 already exists
            user_2 = User.query.filter_by(username='user2').first()
            
            if not user_2:
                # Create user2
                user_password = bcrypt.generate_password_hash('user2123').decode('utf-8')
                user2 = User(
                    username='user2', 
                    email='user2@example.com', 
                    password=user_password,
                    role='student', 
                    campus='MMU'
                )
                db.session.add(user2)
                db.session.commit()

    # def seed_item_1(self):
    #     """Create default item if it doesn't exist."""
    #     with self.app.app_context():
    #         # Check if item1 already exists
    #         item_1 = Item.query.filter_by(name='Item1').first()
            
    #         if not item_1:
    #             # Create item1
    #             item1 = Item(
    #                 name = 'Item1',
    #                 description = "Lorem ipsum dolor sit amet, " \
    #                 "consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. " \
    #                 "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. " \
    #                 "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. " \
    #                 "Excepteur sint occaecat cupidatat non proident, " \
    #                 "sunt in culpa qui officia deserunt mollit anim id est laborum.", 
    #                 price = 447243.74,
    #                 image_filename = 'bitcoin.png',
    #                 timestamp = datetime.utcnow(),
    #                 user_id = 2, 
    #                 category = "Electronics", 
    #                 status = 'available',   # available, hidden, sold
    #                 approval = 'pending'
    #             )
    #             db.session.add(item1)
    #             db.session.commit()

    # def seed_item_2(self):
    #     """Create default item if it doesn't exist."""
    #     with self.app.app_context():
    #         # Check if item1 already exists
    #         item_2 = Item.query.filter_by(name='Item2').first()
            
    #         if not item_2:
    #             # Create item1
    #             item2 = Item(
    #                 name = 'Item2',
    #                 description = "Lorem ipsum dolor sit amet, " \
    #                 "consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. " \
    #                 "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. " \
    #                 "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. " \
    #                 "Excepteur sint occaecat cupidatat non proident, " \
    #                 "sunt in culpa qui officia deserunt mollit anim id est laborum.", 
    #                 price = 14371.70,
    #                 image_filename = 'gold.jpg',
    #                 timestamp = datetime.utcnow(),
    #                 user_id = 3, 
    #                 category = "Dorm Essentials", 
    #                 status = 'available',   # available, hidden, sold
    #                 approval = 'approved'
    #             )
    #             db.session.add(item2)
    #             db.session.commit()

    def seed_all(self):
        """Run all seeding operations."""
        self.seed_admin_user()
        self.seed_user_1()
        self.seed_user_2()
        # self.seed_item_1()
        # self.seed_item_2()
        # Add other seeding operations here