import os


TORTOISE_ORM = {
    "connections": {"default": os.environ.get("DATABASE_URL", "sqlite://./db.sqlite3")},
    "apps": {
        "models": {
            "models": [
                "src.database.models", "aerich.models"
            ],
            "default_connection": "default"
        }
    }
}
