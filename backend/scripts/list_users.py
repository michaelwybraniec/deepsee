"""Script to list all users in the database."""

import sys

# Add parent directory to path
sys.path.insert(0, '.')

from infrastructure.database import SessionLocal, init_db
from domain.models.user import User
from domain.models.task import Task

def list_users():
    """List all users and their task counts."""
    db = SessionLocal()
    
    try:
        users = db.query(User).order_by(User.id).all()
        
        if not users:
            print("❌ No users found in database.")
            return
        
        print(f"\n📊 Found {len(users)} user(s):\n")
        print(f"{'ID':<5} {'Username':<20} {'Email':<30} {'Tasks':<10}")
        print("-" * 70)
        
        for user in users:
            task_count = db.query(Task).filter(Task.owner_user_id == user.id).count()
            print(f"{user.id:<5} {user.username:<20} {user.email:<30} {task_count:<10}")
        
        print("\n" + "=" * 70)
        print("\n📋 Task breakdown by owner:\n")
        
        # Get all tasks grouped by owner
        from sqlalchemy import func
        task_owners = db.query(
            Task.owner_user_id,
            func.count(Task.id).label('count')
        ).group_by(Task.owner_user_id).all()
        
        for owner_id, count in task_owners:
            owner = db.query(User).filter(User.id == owner_id).first()
            owner_name = owner.username if owner else f"User {owner_id} (deleted?)"
            print(f"  {owner_name} (ID: {owner_id}): {count} task(s)")
        
        total_tasks = db.query(Task).count()
        print(f"\n📊 Total tasks: {total_tasks}")
        
    except Exception as e:
        print(f"❌ Error listing users: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    # Initialize database
    init_db()
    
    # List users
    list_users()
