from app.extensions import db, bcrypt
from app.models.user import User

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
                print("Admin user created successfully.")
            else:
                print("Admin user already exists.")
    
    def seed_all(self):
        """Run all seeding operations."""
        self.seed_admin_user()
        # Add other seeding operations here