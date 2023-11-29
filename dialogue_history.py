class DialogueHistory:
  def __init__(self, json_config_manager):
    self.json_config_manager = json_config_manager
    self.history = [{"role":"system", "content":json_config_manager.get("DEFAULT_SYSTEM_CONTENT")}]

  def add_message(self, role, content):
    allowed_roles = ["user", "system", "assistant"]
    if role not in allowed_roles:
        raise ValueError("Role must be 'user', 'system', or 'assistant'")
    
    self.history.append({"role":role, "content":content})

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
    if(system_content == ""):
       system_content = self.json_config_manager.get("DEFAULT_SYSTEM_CONTENT")

    print("==== clean history ====")
    self.history = [{"role":"system", "content":system_content}]

