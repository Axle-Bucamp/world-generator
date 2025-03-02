import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Application settings
    APP_NAME = "Asgard World Generator"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))

    # Redis settings
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB = int(os.getenv("REDIS_DB", 0))
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)

    # World generator settings
    DEFAULT_WORLD_SIZE = int(os.getenv("DEFAULT_WORLD_SIZE", 20))
    MAX_WORLD_SIZE = int(os.getenv("MAX_WORLD_SIZE", 100))

    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Create a config object
config = Config()