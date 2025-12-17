"""Script to drop and optionally recreate database tables."""

import sys
import os
from sqlalchemy import text

# Add parent directory to path
sys.path.insert(0, '.')

from infrastructure.database import engine, Base, init_db
from domain.models import User, Task, Attachment, AuditEvent


def drop_all_tables():
    """Drop all database tables."""
    print("🗑️  Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("✅ All tables dropped successfully!")


def recreate_tables():
    """Recreate all database tables."""
    print("🔨 Recreating all tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ All tables recreated successfully!")


def reset_database(recreate: bool = True):
    """
    Drop all tables and optionally recreate them.
    
    Args:
        recreate: If True, recreate tables after dropping (default: True)
    """
    print("=" * 60)
    print("⚠️  DATABASE RESET")
    print("=" * 60)
    print()
    
    # Show current table counts
    try:
        with engine.connect() as conn:
            # Try to get table counts (will fail if tables don't exist)
            try:
                user_count = conn.execute(text("SELECT COUNT(*) FROM users")).scalar()
                task_count = conn.execute(text("SELECT COUNT(*) FROM tasks")).scalar()
                print(f"📊 Current data:")
                print(f"   Users: {user_count}")
                print(f"   Tasks: {task_count}")
                print()
            except Exception:
                print("📊 No existing tables found.")
                print()
    except Exception as e:
        print(f"⚠️  Could not check current data: {e}")
        print()
    
    # Drop all tables
    drop_all_tables()
    print()
    
    # Recreate if requested
    if recreate:
        recreate_tables()
        print()
        print("✅ Database reset complete! All tables are empty and ready for use.")
    else:
        print("✅ Database reset complete! All tables have been dropped.")
        print("   Run with --recreate flag or use init_db() to recreate tables.")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Drop and optionally recreate all database tables',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Drop and recreate all tables
  python scripts/reset_database.py
  
  # Drop all tables without recreating
  python scripts/reset_database.py --no-recreate
  
  # Using Docker Compose
  docker exec task-tracker-api python scripts/reset_database.py
        """
    )
    parser.add_argument(
        '--no-recreate',
        action='store_true',
        help='Drop tables without recreating them'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Skip confirmation prompt (use with caution!)'
    )
    
    args = parser.parse_args()
    
    # Safety confirmation
    if not args.force:
        # Check if running in interactive mode (TTY)
        is_interactive = sys.stdin.isatty()
        
        if is_interactive:
            print("⚠️  WARNING: This will DELETE ALL DATA in the database!")
            print("   All users, tasks, attachments, and audit events will be lost.")
            print()
            response = input("Are you sure you want to continue? (yes/no): ")
            if response.lower() not in ['yes', 'y']:
                print("❌ Operation cancelled.")
                sys.exit(0)
            print()
        else:
            # Non-interactive mode (e.g., docker exec)
            print("⚠️  WARNING: This will DELETE ALL DATA in the database!")
            print("   All users, tasks, attachments, and audit events will be lost.")
            print()
            print("❌ Running in non-interactive mode. Use --force flag to proceed.")
            print("   Example: docker exec task-tracker-api python scripts/reset_database.py --force")
            sys.exit(1)
    
    # Reset database
    recreate = not args.no_recreate
    reset_database(recreate=recreate)
