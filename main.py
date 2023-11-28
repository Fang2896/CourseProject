import os
import discord
import requests
import json
import random

from openai import OpenAI

discord_intents = discord.Intents().all()
discord_client = discord.Client(intents=discord_intents)


def get_description_dir(role, content):
  allowed_roles = ["user", "system", "assistant"]
  if role not in allowed_roles:
        raise ValueError("Role must be 'user', 'system', or 'assistant'")

  return {
    "role":role, 
    "content":content
  }


def submit_gpt_message(message_text, memory_text):
  memory_text.append(get_description_dir("user", message_text))

  gpt_completion = gpt_client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=memory_text
  )

  memory_text.append(gpt_completion.choices[0].message)


def get_latest_response(memory_text):
  for message in reversed(memory_text):
     if message.role == "assistant":
        return message.content
    
  return None


memory_text=[
  get_description_dir("system", "You are a helpful friend and assistant.")
]
gpt_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY_SYILAB"))


# =========discord=========
@discord_client.event
async def on_ready():
  print("successful login as {0.user}".format(discord_client))

# respond func
@discord_client.event
async def on_message(message):
  if message.author == discord_client.user:
    return
  msg = message.content

  # msg process logic
  submit_gpt_message(msg, memory_text)
  await message.channel.send(get_latest_response(memory_text))


#getting the secret token
discord_client.run('MTE3ODkzMjYwNDM5Nzk1NzE5MQ.Ghbt4F.rsoVPkkOpJqAZhzUN_vxgF7BBIABQdFr-frep8')
