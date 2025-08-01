# Config/app_config.py
from Config.database_config import DatabaseConfig
# === App Info ===
APP_NAME = "Long Chau Pharmacy"
APP_VERSION = "1.0.0"

# === Database ===
DATABASE_FILE = 'Data/pharmacy.db'
DATABASE_CONFIG = DatabaseConfig(DATABASE_FILE)

# === Display Settings ===
DISPLAY_WIDTH = 60
DEFAULT_CURRENCY = "VND"

# === Thresholds ===
LOW_STOCK_THRESHOLD = 10

# === Staff Roles ===
ROLE_PHARMACIST = "Pharmacist"
ROLE_MANAGER = "BranchManager"

# === Date Format ===
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# === System Messages ===
WELCOME_MESSAGE = f"Welcome to {APP_NAME}!"
