import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_IDS = [int(i) for i in os.environ.get("ADMIN_IDS", "").split(",") if i.strip().isdigit()]
