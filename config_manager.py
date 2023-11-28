import os
from dotenv import load_dotenv

class ConfigManager:
    def __init__(self):
        load_dotenv()

    def get(self, key):
        return os.getenv(key)
