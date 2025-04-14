# reset_db.py - Run this script from command line

from app import app, db, User, bcrypt
import sys

def reset_database():
    with app.app_context():
        print("WARNING: This will delete all data in the database!")
        confirm = input("Type 'RESET' to confirm: ")
        
        if confirm == "RESET":
            print("Dropping all tables...")
            db.drop_all()
            
            print("Creating tables...")
            db.create_all()
            
            print("Creating admin user...")
            admin_password = bcrypt.generate_password_hash('admin123').decode('utf-8')
            admin = User(username='admin', email='admin@example.com', 
                         password=admin_password, token=0, is_admin=True, campus='MMU')
            db.session.add(admin)
            db.session.commit()

            print("Creating user1...")
            user1_password = bcrypt.generate_password_hash('user1123').decode('utf-8')
            user_1 = User(username='user1', email='user1@example.com', 
                         password=user1_password, token=0, is_admin=False, campus='MMU')
            db.session.add(user_1)
            db.session.commit()
            
            print("Database reset complete!")
        else:
            print("Database reset cancelled.")

if __name__ == "__main__":
    reset_database()