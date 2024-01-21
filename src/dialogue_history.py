import os
import json
from datetime import datetime


class DialogueHistory:
  def __init__(self, json_config_manager):
    self.json_config_manager = json_config_manager
    self.history = [
        {
            "role":"system", 
            "content":json_config_manager.get("DEFAULT_SYSTEM_CONTENT")
        }
    ]
    self.history_folder = "history"  # 文件夹名称
    self._create_history_folder()
    self.filename = os.path.join(self.history_folder, \
                                 f"{datetime.now().strftime('%Y%m%d%H%M%S')}_dialogue_history.json")
    self._init_json_file()


  def _create_history_folder(self):
    if not os.path.exists(self.history_folder):
      os.makedirs(self.history_folder)


  def _init_json_file(self):
    with open(self.filename, 'w') as file:
        json.dump(self.history, file, indent=4)


  def add_message(self, role, content):
    allowed_roles = ["user", "system", "assistant"]
    if role not in allowed_roles:
        raise ValueError("Role must be 'user', 'system', or 'assistant'")
    
    new_message = {"role": role, "content": content}
    self.history.append(new_message)
    with open(self.filename, 'a') as file:
        file.write(',\n' + json.dumps(new_message, indent=4))


  def get_latest_response(self):
    for message in reversed(self.history):
      if message["role"] == "assistant":
        return message["content"]
      
    return None


  def get_full_history(self):
    return self.history
 

  def get_all_user_history(self):
    user_history = []
    for message in self.history:
        if message["role"] == "user":
            user_history.append(f"user: {message['content']}")
    return ', '.join(user_history)


  def get_full_user_assistant_history(self):
    formatted_history = []
    for message in self.history:
        if message["role"] in ["user", "assistant"]:
            role = "user" if message["role"] == "user" else "gpt"
            formatted_history.append(f"{role}: {message['content']}")
    return ', '.join(formatted_history)


  def clear_history(self, system_content = ""):
    if system_content == "":
        system_content = self.json_config_manager.get("DEFAULT_SYSTEM_CONTENT")
    print("==== clean history ====")

    self.history = [{"role": "system", "content": system_content}]
    self.filename = os.path.join(self.history_folder, \
                                 f"{datetime.now().strftime('%Y%m%d%H%M%S')}_dialogue_history.json")
    
    with open(self.filename, 'w') as file:
        json.dump(self.history, file, indent=4)

