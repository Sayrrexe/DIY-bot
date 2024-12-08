import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
DB_URL = os.getenv("DB_URL")

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
