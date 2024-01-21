import json

class PromptConfigManager:
    def __init__(self, filepath):
        self.config_data = self._load_config(filepath)

    def _load_config(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)

    def get(self, key):
        value = self.config_data.get(key)
        if isinstance(value, list):
            return "\n".join(value)
        return value

