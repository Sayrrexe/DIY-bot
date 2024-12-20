import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = '7810887853:AAGz3C_UXiE-WgwMsFYr_xCeXCS2SQAhI58'
DB_URL = "sqlite://db.sqlite3"

# sqlite
TORTOISE_ORM = {
    "connections": {
        "default": DB_URL,
    },
    "apps": {
        "models": {
            "models": ["app.database.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
