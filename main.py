import discord
from discord.ext import commands, tasks
from discord.flags import Intents
from dotenv import load_dotenv
import os
import asyncio

from Bll import load_profanity_words, profanity_warn

intents = discord.Intents.all()
intents.messages = True

client = discord.Client(intents=intents)

load_dotenv()

profanity_words = set()

load_profanity_words()

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Your Messages 👀"))
    print(f"{client.user} is ready to respond.")

@client.event
async def on_guild_join(guild):
    channel = guild.system_channel
    if channel:
        await channel.send(f"https://tenor.com/view/entrance-confident-im-here-woody-toy-story-gif-11881136")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    content = message.content.strip().lower()
    detected_words = [word for word in profanity_words if word in content]
    asyncio.create_task(profanity_warn(message, content, detected_words))

client.run(os.getenv("TOKEN"))

