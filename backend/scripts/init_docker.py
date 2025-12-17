"""Initialize Docker environment: create test user and seed database."""

import sys
import time
import os

# Force unbuffered output for Docker
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

sys.path.insert(0, '.')

from infrastructure.database import SessionLocal, init_db
from domain.models.user import User
from scripts.create_user import create_user
from scripts.seed_tasks import seed_tasks
from sqlalchemy import text


def wait_for_db(max_retries=30, delay=2):
    """Wait for database to be ready."""
    print("⏳ Waiting for database to be ready...")
    for i in range(max_retries):
        try:
            db = SessionLocal()
            db.execute(text("SELECT 1"))
            db.close()
            print("✅ Database is ready!")
            return True
        except Exception as e:
            if i < max_retries - 1:
                print(f"   Attempt {i+1}/{max_retries}...")
                time.sleep(delay)
            else:
                print(f"❌ Database not ready after {max_retries} attempts: {e}")
                return False
    return False


def init_docker():
    """Initialize Docker environment."""
    print("\n🚀 Initializing Docker environment...\n")
    
    # Wait for database
    if not wait_for_db():
        print("❌ Failed to connect to database")
        return False
    
    # Initialize database schema
    print("📦 Initializing database schema...")
    init_db()
    print("✅ Database schema initialized\n")
    
    # Create test user
    test_username = os.getenv("TEST_USERNAME", "testuser")
    test_email = os.getenv("TEST_EMAIL", "test@example.com")
    test_password = os.getenv("TEST_PASSWORD", "testpassword")
    
    print(f"👤 Creating test user: {test_username}")
    user = create_user(test_username, test_email, test_password)
    
    if not user:
        print("⚠️  Test user may already exist, continuing...")
        # Get existing user
        db = SessionLocal()
        user = db.query(User).filter(User.username == test_username).first()
        db.close()
    
    if user:
        print("\n" + "="*60)
        print("✅ DOCKER INITIALIZATION COMPLETE!")
        print("="*60)
        print("\n📝 TEST USER CREDENTIALS:")
        print(f"   Username: {test_username}")
        print(f"   Email: {test_email}")
        print(f"   Password: {test_password}")
        print("\n" + "="*60)
        print("You can now login at http://localhost:5173")
        print("="*60 + "\n")
    
    # Seed tasks
    if user:
        task_count = int(os.getenv("SEED_TASK_COUNT", "50"))
        print(f"🌱 Seeding {task_count} sample tasks...")
        seed_tasks(count=task_count, user_id=user.id)
        print("✅ Database seeded successfully!\n")
    else:
        print("⚠️  Skipping task seeding (no user available)\n")
    
    return True


if __name__ == "__main__":
    success = init_docker()
    sys.exit(0 if success else 1)
