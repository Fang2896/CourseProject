import os
import discord
from dialogue_history import DialogueHistory


class DiscordBot:
    def __init__(self, token, group_id, gpt_client, prompt_config_manager):
        self.client = discord.Client(intents=discord.Intents().all())
        self.gpt_client = gpt_client

        self.token = token
        self.group_id = group_id
        
        self.history = DialogueHistory(prompt_config_manager)
        self.prompt_config_manager = prompt_config_manager

        # 四种模式: Begin, Free, Image, Scene
        self.mode = "Begin"

        @self.client.event
        async def on_ready():
            print(f"Logged in as {self.client.user}. Target channel ID: ", self.group_id)
            channel = self.client.get_channel(int(self.group_id))
            if channel:
                await channel.send(
                    "======================================================\n"
                    "Hello! I'm online. You can use the following commands:\n"
                    "#mode [Free/Image/Scene] - to switch modes.\n"
                    "#setRole [You settings] - to set the bot character/function\n"
                    "#correct - to get conversation correction.\n"
                    "#reset - to reset history conversation.\n"
                    "======================================================\n"
            ) 
            else: 
                print("Channel Connect Failed!")


        @self.client.event
        async def on_message(message):
            if message.author == self.client.user:
                return
            msg = message.content
            
            if msg.startswith('#setRole '):
                await self.handle_set_system(message)

            elif msg.startswith('#mode '):
                await self.handle_mode_change(message)

            elif msg.strip() == '#correct':
                await self.handle_correction_mode(message)
                
            elif msg.strip() == '#reset':
                await self.handle_reset_mode(message)

            else:
                await self.handle_user_input(message)

    '''
    Handle Functions:
        Correct mode
        Reset mode
        Mode change
        Setting change
        User input
    '''
    async def handle_correction_mode(self, message):
        tobe_corrected_input = self.history.get_all_user_history()
        correct_instruction = self.prompt_config_manager.get("CORRECT_INSTRUCTION")
        correct_format_prompt = self.prompt_config_manager.get("CORRECT_FORMAT")
        
        print("Begin Correct")
        await self.send_split_messages(message.channel, 
                                       "===== In Correcting =====")
        
        correct_input = [
            {
                "role": "system", 
                "content": self.prompt_config_manager.get("CORRECT_SYSTEM_CONTENT")
            },
            {
                "role": "user",
                "content": correct_instruction + correct_format_prompt + "\n" + tobe_corrected_input
            }

        ]
        
        response = await self.gpt_client.submit_message(correct_input)
        await self.send_split_messages(message.channel, response["content"])
        self.history.clear_history()
        await self.send_split_messages(message.channel, "===== Conversation has been reset =====")


    async def handle_reset_mode(self, message):
        print("Begin Reset")
        await self.send_split_messages(message.channel, "===== Conversation has been reset =====")
        self.history.clear_history(self.mode)


    async def handle_mode_change(self, message):
        _, mode_name = message.content.split(maxsplit=1)
        allowed_modes = ["Free", "Image", "Scene"]

        mode_guidance = {
            # TODO: 这里可以设定各个模式下更详细的引导信息
            "Free": "You're now in Free mode. You can chat freely.",
            "Image": "You're now in Image mode. Send me a prompt, and I'll generate an image for you.",
            "Scene": "You're now in Scene mode. I will give you a scene in daily life."
        }

        if mode_name in allowed_modes:
            self.mode = mode_name

            new_system = self.prompt_config_manager.get(mode_name + "_SYSTEM_CONTENT")
            self.history.reset_system_prompt(new_system)

            await message.channel.send(f"===== Mode changed to: [{self.mode}] =====")
            if self.mode != "Begin":
                await message.channel.send(mode_guidance[self.mode])
        else:
            await message.channel.send(f"===== Invalid mode. Please choose from [{', '.join(allowed_modes)}]. =====")


    async def handle_set_system(self, message):
        if self.mode == "Begin":
            await self.send_split_messages(message.channel, "===== Please set a mode before setting system! ====")
            return

        _, system_prompt = message.content.split(maxsplit=1)
        await self.send_split_messages(message.channel, "===== Set New System ====")
        self.history.reset_system_prompt(system_prompt)


    # 主要逻辑就在这里实现
    async def handle_user_input(self, message):
        if self.mode == "Image":
            """
            TODO:
            目前的功能只有让用户输入prompt，然后生成对应的image
            后面要改成：
            1. 首先一切换到这个模式的时候，就随机生成一张图片
            2. 然后让用户tell a story
            3. 然后GPT渐渐的引导用户--
            4. 最后用户满意的时候可以调用#correct来获得相应的反馈
            """

            image_path = await self.gpt_client.get_image(message.content)
            print("Image Path: ", image_path)
            if image_path:
                await self.send_image(message.channel, image_path)


        elif self.mode == "Free":
            """
            TODO:
            目前的功能就是单纯聊天，但是需要更好的prompt
            """

            self.history.add_message("user", message.content)
            print("User Input: ", message.content)
            response = await self.gpt_client.submit_message(self.history.get_full_history())
            self.history.add_message("assistant", response["content"])
            await self.send_split_messages(message.channel, response["content"])


        elif self.mode == "Scene":
            """
            TODO:
            首先要设定至少5个scene setting，然后随机选一个
            然后展示给用户其设定，然后开始roleplay
            roleplay后，针对场景来进行纠正反馈，不仅仅是对话
            还有针对相应场景更好的应对方式，以及更好的表达方式等等
            """

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

