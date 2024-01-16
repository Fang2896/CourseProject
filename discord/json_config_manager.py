import json

class JsonConfigManager:
    def __init__(self, filepath):
        self.config_data = self._load_config(filepath)

    def _load_config(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)

    def get(self, key):
        # 获取指定键的值（一个字符串数组），然后将其连接成一个完整的字符串
        value = self.config_data.get(key)
        if isinstance(value, list):
            return "\n".join(value)
        return value

config_manager = JsonConfigManager('config.json')
print(config_manager.get('DEFAULT_SYSTEM_CONTENT'))
