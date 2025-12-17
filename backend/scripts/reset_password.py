"""Script to reset a user's password in the database."""

import sys
import bcrypt
from sqlalchemy.orm import Session

# Add parent directory to path
sys.path.insert(0, '.')

from infrastructure.database import SessionLocal, init_db
from domain.models.user import User


def reset_password(username: str, new_password: str) -> bool:
    """
    Reset a user's password.
    
    Args:
        username: Username or email
        new_password: New plain text password
    
    Returns:
        True if successful, False otherwise
    """
    db: Session = SessionLocal()
    
    try:
        # Find user by username or email
        user = db.query(User).filter(
            (User.username == username) | (User.email == username)
        ).first()
        
        if not user:
            print(f"❌ User '{username}' not found!")
            return False
        
        # Hash new password
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Update password
        user.hashed_password = hashed_password
        db.commit()
        
        print(f"✅ Password reset successfully for user '{user.username}'!")
        return True
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error resetting password: {str(e)}")
        return False
    finally:
        db.close()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Reset a user password')
    parser.add_argument('username', help='Username or email')
    parser.add_argument('password', help='New password')
    
    args = parser.parse_args()
    
    # Initialize database
    init_db()
    
    # Reset password
    reset_password(args.username, args.password)
