#!/usr/bin/env python3
"""Script to query audit events from the database.

Usage:
    # Activate virtual environment first:
    cd backend
    source .venv/bin/activate  # On macOS/Linux
    # OR
    .venv\Scripts\activate  # On Windows
    
    # Then run:
    python3 scripts/query_audit_events.py [options]
"""

import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)

# Check if we're in a virtual environment or if dependencies are available
try:
    import sqlalchemy
except ImportError:
    venv_python = os.path.join(backend_dir, '.venv', 'bin', 'python3')
    if os.path.exists(venv_python):
        print("ERROR: Virtual environment not activated!")
        print(f"\nPlease activate the virtual environment first:")
        print(f"  cd {backend_dir}")
        print(f"  source .venv/bin/activate  # On macOS/Linux")
        print(f"  # OR")
        print(f"  .venv\\Scripts\\activate  # On Windows")
        print(f"\nThen run this script again.")
        print(f"\nAlternatively, run directly with venv Python:")
        print(f"  {venv_python} scripts/query_audit_events.py")
        sys.exit(1)
    else:
        print("ERROR: SQLAlchemy not found and virtual environment not found!")
        print(f"\nPlease install dependencies:")
        print(f"  cd {backend_dir}")
        print(f"  python3 -m venv .venv")
        print(f"  source .venv/bin/activate")
        print(f"  pip install -r requirements.txt")
        sys.exit(1)

from sqlalchemy.orm import Session
from infrastructure.database import SessionLocal
from infrastructure.persistence.models.audit_event import AuditEvent
from infrastructure.persistence.repositories.audit_repository import SQLAlchemyAuditRepository
from domain.audit.audit_event import AuditActionType


def print_event(event: AuditEvent):
    """Print a formatted audit event."""
    user_info = f"user {event.user_id}" if event.user_id else "system"
    print(f"\n[{event.timestamp}] {event.action_type}")
    print(f"  Performed by: {user_info}")
    print(f"  Resource: {event.resource_type}:{event.resource_id}")
    if event.event_metadata:
        print(f"  Metadata: {event.event_metadata}")


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Query audit events")
    parser.add_argument("--action-type", help="Filter by action type (e.g., task_created)")
    parser.add_argument("--user-id", type=int, help="Filter by user ID")
    parser.add_argument("--resource-type", help="Filter by resource type (e.g., task)")
    parser.add_argument("--resource-id", help="Filter by resource ID")
    parser.add_argument("--limit", type=int, default=20, help="Limit number of results (default: 20)")
    parser.add_argument("--days", type=int, help="Get events from last N days")
    parser.add_argument("--all", action="store_true", help="Show all events (no limit)")
    
    args = parser.parse_args()
    
    db: Session = SessionLocal()
    
    try:
        # Build query
        query = db.query(AuditEvent)
        
        # Apply filters
        if args.action_type:
            query = query.filter(AuditEvent.action_type == args.action_type)
        
        if args.user_id:
            query = query.filter(AuditEvent.user_id == args.user_id)
        
        if args.resource_type:
            query = query.filter(AuditEvent.resource_type == args.resource_type)
        
        if args.resource_id:
            query = query.filter(AuditEvent.resource_id == str(args.resource_id))
        
        if args.days:
            cutoff = datetime.utcnow() - timedelta(days=args.days)
            query = query.filter(AuditEvent.timestamp >= cutoff)
        
        # Order by timestamp (most recent first)
        query = query.order_by(AuditEvent.timestamp.desc())
        
        # Apply limit
        if not args.all:
            query = query.limit(args.limit)
        
        # Execute query
        events = query.all()
        
        # Print results
        print(f"\nFound {len(events)} audit event(s):\n")
        print("=" * 80)
        
        for event in events:
            print_event(event)
        
        print("\n" + "=" * 80)
        
    finally:
        db.close()


if __name__ == "__main__":
    main()
