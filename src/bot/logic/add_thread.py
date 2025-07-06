import re
from .add_log_tag import add_log_tag
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.qdrant.qdrant import process_new_thread
from bot.pydantic_configure.pydantic_conf import *
import json

# Add channel to the database
async def add_thread(bot, thread):
    
    url_pattern = r'https?:\/\/[^\s]+'
 
    # Collect all messages and data
    messages = []
    urls = []
    embeds = []
    attachments = []
    
    async for message in thread.history(limit=None, oldest_first=True):
        messages.append(message.content)
        urls.extend(re.findall(url_pattern, message.content))
        embeds.extend(message.embeds)
        attachments.extend(message.attachments)
    
    # Add to Qdrant collection
    await process_new_thread(bot, thread, messages, urls, embeds, attachments)
    
    # Log if successful
    await add_log_tag(bot, thread)