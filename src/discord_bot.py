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
        self.history.clear_history(self.mode)
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
            "Free": "You're now in Free mode.",
            "Image": "You're now in Image mode.",
            "Scene": "You're now in Scene mode.",
        }

        if mode_name in allowed_modes:
            self.mode = mode_name

            await message.channel.send(f"===== Mode changed to: [{self.mode}] =====")
            if self.mode != "Begin":
                await message.channel.send(mode_guidance[self.mode])

            if mode_name == "Image":
                await self.handle_begin_Image_Mode(message)
                
            elif mode_name == "Free":
                await self.handle_begin_Free_Mode(message)

            elif mode_name == "Scene":
                await self.handle_begin_Scene_Mode(message)


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
            self.history.add_message("user", message.content)
            print("User Input: ", message.content)
            response = await self.gpt_client.submit_message(self.history.get_full_history())
            self.history.add_message("assistant", response["content"])
            await self.send_split_messages(message.channel, response["content"])
            

        elif self.mode == "Free":
            self.history.add_message("user", message.content)
            print("User Input: ", message.content)
            response = await self.gpt_client.submit_message(self.history.get_full_history())
            self.history.add_message("assistant", response["content"])
            await self.send_split_messages(message.channel, response["content"])


        elif self.mode == "Scene":
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


    """
    Begining Handles:
    处理3个模式，刚开始切换后要执行的操作
    """

    async def handle_begin_Image_Mode(self, message):
        # 首先获取图片发送给用户
        generation_prompt = self.prompt_config_manager.get("Image_GENERATE_CONTENT")
        image_path, image_url = await self.gpt_client.get_image(generation_prompt)
        print("Image generation prompt:", generation_prompt, "\n")
        print("Image Path: ", image_path)
        print("Image Path: ", image_url)
        if image_path:
            await self.send_image(message.channel, image_path)
        await self.send_split_messages(message.channel, self.prompt_config_manager.get("Image_Describe_GUIDE_CONTENT"))

        # 然后需要让gpt-vision理解, 传入url就行
        image_description = await self.gpt_client.see_image(image_url, self.prompt_config_manager.get("Image_VIEW_CONTENT"))
        image_description_content = image_description["content"]
        print("GPT see this image: \n", image_description_content)
        
        # 更新历史管理
        new_system = self.prompt_config_manager.get("Image" + "_SYSTEM_CONTENT")
        new_system += image_description_content
        self.history.reset_system_prompt(new_system)
        self.history.add_message("assistant", self.prompt_config_manager.get("Image_Describe_GUIDE_CONTENT"))
        return image_description_content

    async def handle_begin_Free_Mode(self, message):
        # 
        generate_prompt_free = [
            {
                "role":"system",
                "content":"You are a good friend of mine, and you will always try to lead the trend of the conversation."
            },
            {
                "role":"user",
                "content":self.prompt_config_manager.get("Free_GENERATE_CONTENT")
            }
        ]
        generated_topics = await self.gpt_client.submit_message(generate_prompt_free)
        print("Free Mode: Generate Topics: \n" ,generated_topics)
        generated_topics_content = generated_topics["content"]

        await self.send_split_messages(message.channel ,"========Here is today's topic, Let's talk!=======")
        await self.send_split_messages(message.channel ,generate_topics_content)

        new_system_free = self.prompt_config_manager.get("Free" + "_SYSTEM_CONTENT")
        new_system_free += generate_topics_content
        self.history.reset_system_prompt(new_system_free)

    async def handle_begin_Scene_Mode(self, message):
        generate_prompt = [
            {
                "role":"system",
                "content":"You are a great script writer"
            },
            {
                "role":"user",
                "content":self.prompt_config_manager.get("Scene_SETTING_GENERATE_CONTENT")
            }
        ]
        generate_settings = await self.gpt_client.submit_message(generate_prompt)
        generate_settings_content = generate_settings["content"]

        await self.send_split_messages(message.channel ,"========The following are the settings=======")
        await self.send_split_messages(message.channel ,generate_settings_content)
        await self.send_split_messages(message.channel ,"========Start RolePlay=======")

        new_system = self.prompt_config_manager.get("Scene" + "_SYSTEM_CONTENT") + generate_settings_content
        self.history.reset_system_prompt(new_system)

    
    def format_full_conversation(self):
        full_history = self.history.get_full_history()
        return '\n'.join([f'{msg["role"].title()}: {msg["content"]}' for msg in full_history])
    

    def run(self):
        self.client.run(self.token)

