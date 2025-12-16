"""Script to list all tasks with their owners."""

import sys
import json

# Add parent directory to path
sys.path.insert(0, '.')

from infrastructure.database import SessionLocal, init_db
from domain.models.task import Task
from domain.models.user import User

def list_tasks(limit=20):
    """List tasks with their owner information."""
    db = SessionLocal()
    
    try:
        tasks = db.query(Task).order_by(Task.id.desc()).limit(limit).all()
        
        if not tasks:
            print("❌ No tasks found in database.")
            return
        
        print(f"\n📋 Showing {len(tasks)} most recent task(s):\n")
        print(f"{'ID':<5} {'Title':<40} {'Owner':<20} {'Owner ID':<10} {'Status':<15}")
        print("-" * 100)
        
        for task in tasks:
            owner = db.query(User).filter(User.id == task.owner_user_id).first()
            owner_name = owner.username if owner else f"User {task.owner_user_id} (not found)"
            title = task.title[:37] + "..." if len(task.title) > 40 else task.title
            status = task.status or "None"
            
            print(f"{task.id:<5} {title:<40} {owner_name:<20} {task.owner_user_id:<10} {status:<15}")
        
        print("\n" + "=" * 100)
        
        # Summary
        total_tasks = db.query(Task).count()
        print(f"\n📊 Total tasks in database: {total_tasks}")
        
    except Exception as e:
        print(f"❌ Error listing tasks: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='List tasks with owner information')
    parser.add_argument(
        '--limit',
        type=int,
        default=20,
        help='Number of tasks to show (default: 20)'
    )
    
    args = parser.parse_args()
    
    # Initialize database
    init_db()
    
    # List tasks
    list_tasks(limit=args.limit)
