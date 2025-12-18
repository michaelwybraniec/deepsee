"""Worker entry point - starts the scheduler and keeps the process running."""

import signal
import sys
import time
from infrastructure.logging.config import get_logger
from worker.scheduler import start_scheduler, stop_scheduler

logger = get_logger(__name__)


def signal_handler(sig, frame):
    """Handle shutdown signals gracefully."""
    logger.info("worker_shutdown_signal_received", signal=sig, message="Received shutdown signal, stopping scheduler")
    stop_scheduler()
    sys.exit(0)


def main():
    """Main entry point for the worker service."""
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Start the scheduler
        start_scheduler()
        logger.info("worker_service_started", message="Worker service started successfully")
        
        # Keep the process alive
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("worker_keyboard_interrupt", message="Received keyboard interrupt, shutting down")
        stop_scheduler()
    except Exception as e:
        logger.error("worker_fatal_error", error=str(e), exc_info=True, message="Fatal error in worker service")
        stop_scheduler()
        sys.exit(1)


if __name__ == "__main__":
    main()
