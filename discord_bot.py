import discord
from dialogue_history import DialogueHistory

class DiscordBot:
    def __init__(self, token, gpt_client):
        self.client = discord.Client(intents=discord.Intents().all())
        self.gpt_client = gpt_client
        self.token = token
        self.history = DialogueHistory()

        @self.client.event
        async def on_ready():
            print(f"Logged in as {self.client.user}")

        @self.client.event
        async def on_message(message):
            if message.author == self.client.user:
                return

            msg = message.content

            # check stop
            if msg.strip() == '#stop':
                full_history_text = self.format_full_conversation()
                await self.send_split_messages(message.channel, full_history_text)
                self.history.clear_history()
            else:
                self.history.add_message("user", msg)

                # response = self.gpt_client.submit_message(self.history.get_full_history())
                response = await self.gpt_client.submit_message(self.history.get_full_history())

                self.history.add_message("assistant", response["content"])

                # await message.channel.send(response["content"])
                await self.send_split_messages(message.channel, response["content"])

    def format_full_conversation(self):
        full_history = self.history.get_full_history()
        return '\n'.join([f'{msg["role"].title()}: {msg["content"]}' for msg in full_history])

    # async def send_full_conversation(self, channel):
    #         full_history = self.history.get_full_history()
    #         history_text = '\n'.join([f'{msg["role"].title()}: {msg["content"]}' for msg in full_history])
    #         await channel.send(history_text)

    async def send_split_messages(self, channel, message):
        if len(message) <= 2000:
            await channel.send(message)
        else:
            # discord limit the send text size to 2000
            for i in range(0, len(message), 1500):
                await channel.send(message[i:i+1500])

    def run(self):
        self.client.run(self.token)

