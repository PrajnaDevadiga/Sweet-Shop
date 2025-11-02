
"""
Script to create an admin user for the Sweet Shop Management System
Run: python scripts/create_admin.py
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, init_db
from app.models import User
from app.auth import get_password_hash, get_user_by_username

def create_admin(username: str, email: str, password: str):
    """Create an admin user"""
    init_db()
    db = SessionLocal()
    
    try:
        # Check if admin already exists
        existing_user = get_user_by_username(db, username)
        if existing_user:
            print(f"User '{username}' already exists!")
            return False
        
        # Warn if password is very long (bcrypt limit is 72 bytes)
        password_bytes = password.encode('utf-8')
        if len(password_bytes) > 72:
            print(f"Warning: Password exceeds 72 bytes. It will be truncated to 72 bytes.")
            print(f"Original length: {len(password_bytes)} bytes")
        
        # Create admin user
        hashed_password = get_password_hash(password)
        admin_user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            is_admin=True
        )
        db.add(admin_user)
        db.commit()
        print(f"Admin user '{username}' created successfully!")
        return True
    except Exception as e:
        print(f"Error creating admin user: {e}")
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    import getpass
    
    print("Create Admin User")
    print("=" * 40)
    username = input("Username: ")
    email = input("Email: ")
    password = getpass.getpass("Password: ")
    
    create_admin(username, email, password)

