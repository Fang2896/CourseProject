from config_manager import ConfigManager
from gpt_client import GPTClient
from discord_bot import DiscordBot

def main():
  config = ConfigManager()
  gpt_client = GPTClient(config.get("OPENAI_API_KEY_SYILAB"))
  discord_bot = DiscordBot(config.get("DISCORD_BOT_TOKEN"), gpt_client)
  discord_bot.run()

if __name__ == "__main__":
    main()
