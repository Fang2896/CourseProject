import os
from dotenv import load_dotenv

class TokenConfigManager:
    def __init__(self):
        load_dotenv()

    def get(self, key):
        return os.getenv(key)
