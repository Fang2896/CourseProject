# from config_manager import ConfigManager
from json_config_manager import JsonConfigManager
from gpt_client import GPTClient
from discord_bot import DiscordBot

def main():
  json_config_manager = JsonConfigManager('config.json')
  gpt_client = GPTClient(json_config_manager.get("OPENAI_API_KEY_SYILAB"))
  discord_bot = DiscordBot(json_config_manager.get("DISCORD_BOT_TOKEN"), gpt_client, json_config_manager)
  discord_bot.run()

if __name__ == "__main__":
    main()
