import os
import discord
from dialogue_history import DialogueHistory


class DiscordBot:
    def __init__(self, token, gpt_client, json_config_manager):
        self.client = discord.Client(intents=discord.Intents().all())
        self.gpt_client = gpt_client
        self.token = token
        self.history = DialogueHistory(json_config_manager)
        self.json_config_manager = json_config_manager

        # 三种模式: Free, Image, Scene
        self.mode = "Free"

        @self.client.event
        async def on_ready():
            print(f"Logged in as {self.client.user}")

        @self.client.event
        async def on_message(message):
            if message.author == self.client.user:
                return
            msg = message.content

            if msg.strip() == '#correct':
                await self.handle_correction_mode(message)
                
            elif msg.strip() == '#reset':
                await self.handle_reset_mode(message)

            elif msg.startswith('#mode '):
                await self.handle_mode_change(message)
                await self.handle_reset_mode(message)

            else:
                await self.handle_user_input(message)

    '''
    Handle Functions:
        Correct mode
        Reset mode
        Mode change
        User input
    '''
    async def handle_correction_mode(self, message):
        tobe_corrected_input = self.history.get_all_user_history()
        correct_instruction = self.json_config_manager.get("CORRECT_INSTRUCTION")
        correct_format_prompt = self.json_config_manager.get("CORRECT_FORMAT")
        print("Begin Correct")

        await self.send_split_messages(message.channel, "===== In Correcting =====")
        self.history.add_message(
            "user", 
                correct_instruction + correct_format_prompt + "\n" + tobe_corrected_input)

        response = await self.gpt_client.submit_message(self.history.get_full_history())
        await self.send_split_messages(message.channel, response["content"])
        self.history.clear_history()
        await self.send_split_messages(message.channel, "===== Conversation has been reset =====")


    async def handle_reset_mode(self, message):
        print("Begin Reset")
        await self.send_split_messages(message.channel, "===== Conversation has been reset =====")
        self.history.clear_history()


    async def handle_mode_change(self, message):
        _, mode_name = message.content.split(maxsplit = 1)
        allowed_modes = ["Free", "Image", "Scene"]
        
        if mode_name in allowed_modes:
            self.mode = mode_name
            await message.channel.send(f"===== Mode changed to: [{self.mode}] =====")
        else:
            await message.channel.send(f"===== Invalid mode. Please choose from [{', '.join(allowed_modes)}]. =====")


    async def handle_user_input(self, message):
        if self.mode == "Image":
            image_path = await self.gpt_client.get_image(message.content)
            print("Image Path: ", image_path)
            if image_path:
                await self.send_image(message.channel, image_path)

            image_path = await self.gpt_client.get_image(message.content)
            print("Image Path: ", image_path)
        else:
            self.history.add_message("user", message.content)
            print("User Input: ", message.content)
            response = await self.gpt_client.submit_message(self.history.get_full_history())
            self.history.add_message("assistant", response["content"])
            await self.send_split_messages(message.channel, response["content"])


    '''
    Send Functions:
        Send text message
        Send image
        Send voice files
    '''
    async def send_split_messages(self, channel, message):
        if len(message) <= 2000:
            await channel.send(message)
        else:
            # discord limit the send text size to 2000
            for i in range(0, len(message), 1500):
                await channel.send(message[i:i+1500])


    async def send_image(self, channel, image_path):
        if not os.path.exists(image_path):
            await channel.send("Image not found.")
            return

        file = discord.File(image_path)
        await channel.send(file=file)


    def format_full_conversation(self):
        full_history = self.history.get_full_history()
        return '\n'.join([f'{msg["role"].title()}: {msg["content"]}' for msg in full_history])
    

    def run(self):
        self.client.run(self.token)

