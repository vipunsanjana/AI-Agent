import logging
import os

# === Ensure logs folder exists ===
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# === Configure the root logger ===
LOG_FILE_PATH = os.path.join(LOG_DIR, "app.log")

logging.basicConfig(
    filename=LOG_FILE_PATH,
    filemode="a",  # append mode
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    level=logging.INFO
)

# === Create module-level logger ===
logger = logging.getLogger("app_logger")

def get_logger(name: str = None) -> logging.Logger:
    """Return a named logger for module-specific context."""
    return logging.getLogger(name or "app_logger")
