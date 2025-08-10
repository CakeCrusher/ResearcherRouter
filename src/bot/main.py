import discord
import os
import asyncio
import logging
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

# Set up discord.log 
# Logs events and interactions with the bot
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s')
handler.setFormatter(formatter)
discord.utils.setup_logging(level=logging.INFO, handler=handler)

# Set up intent permissions
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Load cogs (bot commands & events)
async def load():
    # Get the directory where this file is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    cogs_dir = os.path.join(current_dir, 'cogs')
    
    for filename in os.listdir(cogs_dir):
        if filename.endswith('.py'):
            await bot.load_extension(f'bot.cogs.{filename[:-3]}')

async def main():
    await load()
    await bot.start(token)

asyncio.run(main())