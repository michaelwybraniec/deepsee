"""Script to create a user in the database."""

import sys
import bcrypt
from sqlalchemy.orm import Session

# Add parent directory to path
sys.path.insert(0, '.')

from infrastructure.database import SessionLocal, init_db
from domain.models.user import User


def create_user(username: str, email: str, password: str) -> User:
    """
    Create a new user in the database.
    
    Args:
        username: Username (must be unique)
        email: Email address (must be unique)
        password: Plain text password (will be hashed)
    
    Returns:
        Created User object
    """
    db: Session = SessionLocal()
    
    try:
        # Check if user already exists
        existing = db.query(User).filter(
            (User.username == username) | (User.email == email)
        ).first()
        
        if existing:
            print(f"❌ User with username '{username}' or email '{email}' already exists!")
            return None
        
        # Hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Create user
        user = User(
            username=username,
            email=email,
            hashed_password=hashed_password
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        print(f"✅ User created successfully!")
        print(f"   ID: {user.id}")
        print(f"   Username: {user.username}")
        print(f"   Email: {user.email}")
        print(f"   Password: {password}")
        
        return user
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating user: {str(e)}")
        return None
    finally:
        db.close()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Create a user in the database')
    parser.add_argument('username', help='Username')
    parser.add_argument('email', help='Email address')
    parser.add_argument('password', help='Password')
    
    args = parser.parse_args()
    
    # Initialize database
    init_db()
    
    # Create user
    create_user(args.username, args.email, args.password)
