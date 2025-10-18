import logging
import os
from datetime import datetime

# Create a directory for logs if it doesn't exist
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Create log file path with current date
LOG_FILE = os.path.join(LOG_DIR, f"log_{datetime.now().strftime('%Y-%m-%d')}.log")

# Configure logging settings
logging.basicConfig(
    filename=LOG_FILE,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    level=logging.INFO
)

def get_logger(name):
    """Returns a logger instance with the given name."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger
