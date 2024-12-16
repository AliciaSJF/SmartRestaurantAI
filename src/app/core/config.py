import os

def load_config():
    config = {}
    config["host"] = os.getenv("HOST")
    config["database"] = os.getenv("DATABASE_URL")
    config["api_key"] = os.getenv("OPENAI_API_KEY")
    return config

