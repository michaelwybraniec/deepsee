"""Script to seed the database with 50 sample tasks."""

import sys
import json
import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

# Add parent directory to path
sys.path.insert(0, '.')

from infrastructure.database import SessionLocal, init_db
from domain.models.user import User
from domain.models.task import Task


# Sample data for generating tasks
TASK_TITLES = [
    "Complete project documentation",
    "Review code changes",
    "Update API documentation",
    "Fix bug in authentication",
    "Implement new feature",
    "Write unit tests",
    "Refactor legacy code",
    "Optimize database queries",
    "Design new UI component",
    "Setup CI/CD pipeline",
    "Deploy to staging",
    "Review pull requests",
    "Update dependencies",
    "Fix security vulnerabilities",
    "Improve error handling",
    "Add logging and monitoring",
    "Create user guide",
    "Setup development environment",
    "Configure production server",
    "Implement caching strategy",
    "Optimize frontend performance",
    "Add integration tests",
    "Update documentation",
    "Fix memory leaks",
    "Improve code coverage",
    "Setup backup strategy",
    "Configure load balancer",
    "Implement rate limiting",
    "Add API versioning",
    "Create admin dashboard",
    "Setup monitoring alerts",
    "Implement search functionality",
    "Add file upload feature",
    "Create data migration script",
    "Setup database replication",
    "Implement authentication",
    "Add password reset flow",
    "Create email templates",
    "Setup email service",
    "Implement notifications",
    "Add task filtering",
    "Create export functionality",
    "Implement pagination",
    "Add sorting options",
    "Create user profiles",
    "Implement permissions",
    "Add audit logging",
    "Create reports",
    "Setup analytics",
    "Implement search indexing",
]

TASK_DESCRIPTIONS = [
    "This task requires careful attention to detail and thorough testing.",
    "Make sure to follow best practices and coding standards.",
    "Review existing implementation before making changes.",
    "Consider edge cases and error scenarios.",
    "Ensure backward compatibility is maintained.",
    "Test thoroughly in development environment first.",
    "Document any breaking changes clearly.",
    "Coordinate with team members before implementation.",
    "Check for existing similar implementations.",
    "Verify requirements with stakeholders.",
    "Consider performance implications.",
    "Ensure security best practices are followed.",
    "Review related documentation.",
    "Test with various data scenarios.",
    "Consider scalability requirements.",
]

STATUSES = ["todo", "in_progress", "done"]
PRIORITIES = ["low", "medium", "high"]
TAG_OPTIONS = [
    ["frontend", "ui"],
    ["backend", "api"],
    ["database", "sql"],
    ["testing", "qa"],
    ["documentation", "docs"],
    ["security", "auth"],
    ["performance", "optimization"],
    ["bugfix", "hotfix"],
    ["feature", "enhancement"],
    ["refactor", "cleanup"],
    ["deployment", "devops"],
    ["monitoring", "logging"],
]


def get_or_create_seed_user(db: Session) -> User:
    """Get or create a seed user for tasks."""
    # Try to find existing seed user
    user = db.query(User).filter(User.username == "seed_user").first()
    
    if not user:
        # Create seed user
        import bcrypt
        hashed_password = bcrypt.hashpw(b"seed_password", bcrypt.gensalt()).decode('utf-8')
        user = User(
            username="seed_user",
            email="seed@example.com",
            hashed_password=hashed_password
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"✅ Created seed user: {user.username} (ID: {user.id})")
    else:
        print(f"✅ Using existing seed user: {user.username} (ID: {user.id})")
    
    return user


def generate_task_data(index: int, user_id: int) -> dict:
    """Generate task data for a single task."""
    # Random title
    title = random.choice(TASK_TITLES)
    if index > 0:
        title = f"{title} #{index + 1}"
    
    # Random description (70% chance)
    description = None
    if random.random() < 0.7:
        description = random.choice(TASK_DESCRIPTIONS)
    
    # Random status
    status = random.choice(STATUSES)
    
    # Random priority
    priority = random.choice(PRIORITIES)
    
    # Random due date (within next 30 days, or past for some tasks)
    days_offset = random.randint(-10, 30)
    due_date = datetime.now() + timedelta(days=days_offset)
    
    # Random tags (60% chance, 1-3 tags)
    tags = None
    if random.random() < 0.6:
        num_tags = random.randint(1, 3)
        selected_tags = random.sample(TAG_OPTIONS, num_tags)
        tags_list = [tag for tag_group in selected_tags for tag in tag_group[:1]]  # Take first tag from each group
        tags = json.dumps(tags_list)
    
    # Random created_at (within last 60 days)
    created_days_ago = random.randint(0, 60)
    created_at = datetime.now() - timedelta(days=created_days_ago)
    
    # Updated_at is same as created_at or slightly later
    updated_at = created_at
    if random.random() < 0.3:  # 30% chance task was updated
        updated_days_ago = random.randint(0, created_days_ago)
        updated_at = datetime.now() - timedelta(days=updated_days_ago)
    
    return {
        "title": title,
        "description": description,
        "status": status,
        "priority": priority,
        "due_date": due_date,
        "tags": tags,
        "owner_user_id": user_id,
        "created_at": created_at,
        "updated_at": updated_at,
    }


def seed_tasks(count: int = 50, user_id: int = None):
    """
    Seed the database with sample tasks.
    
    Args:
        count: Number of tasks to create (default: 50)
        user_id: User ID to assign tasks to (if None, creates/uses seed_user)
    """
    db: Session = SessionLocal()
    
    try:
        # Get or create user
        if user_id:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                print(f"❌ User with ID {user_id} not found!")
                return
        else:
            user = get_or_create_seed_user(db)
        
        # Check existing tasks count
        existing_count = db.query(Task).filter(Task.owner_user_id == user.id).count()
        print(f"📊 Existing tasks for user '{user.username}': {existing_count}")
        
        # Generate and create tasks
        created = 0
        for i in range(count):
            task_data = generate_task_data(i, user.id)
            task = Task(**task_data)
            db.add(task)
            created += 1
        
        db.commit()
        
        # Verify creation
        total_count = db.query(Task).filter(Task.owner_user_id == user.id).count()
        print(f"✅ Successfully created {created} tasks!")
        print(f"📊 Total tasks for user '{user.username}': {total_count}")
        
        # Print summary
        status_counts = db.query(Task.status, db.func.count(Task.id)).filter(
            Task.owner_user_id == user.id
        ).group_by(Task.status).all()
        
        print("\n📈 Task status breakdown:")
        for status, count in status_counts:
            print(f"   {status or 'None'}: {count}")
        
        priority_counts = db.query(Task.priority, db.func.count(Task.id)).filter(
            Task.owner_user_id == user.id
        ).group_by(Task.priority).all()
        
        print("\n📈 Task priority breakdown:")
        for priority, count in priority_counts:
            print(f"   {priority or 'None'}: {count}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding tasks: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Seed the database with sample tasks')
    parser.add_argument(
        '--count',
        type=int,
        default=50,
        help='Number of tasks to create (default: 50)'
    )
    parser.add_argument(
        '--user-id',
        type=int,
        default=None,
        help='User ID to assign tasks to (default: creates/uses seed_user)'
    )
    
    args = parser.parse_args()
    
    # Initialize database
    init_db()
    
    # Seed tasks
    seed_tasks(count=args.count, user_id=args.user_id)
