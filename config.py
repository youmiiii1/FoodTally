import os

# TG 'FoodTelly1.0' API
TOKEN_BOT = os.getenv("TOKEN_BOT")

# Make.com webhook
WEB_HOOK_URL = os.getenv("WEB_HOOK_URL")

# database_config
host = os.getenv("DB_HOST", "localhost")
db_name = os.getenv("DB_NAME", "food_tally_db")
db_password = os.getenv("DB_PASSWORD", "")
db_user = os.getenv("DB_USER", "postgres")
port = int(os.getenv("DB_PORT", 5432))

