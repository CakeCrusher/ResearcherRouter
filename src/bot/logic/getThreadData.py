import re
from .add_log_tag import add_log_tag
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.qdrant.qdrant import process_new_thread

# Get data from newly created forum threads
async def getThreadData(bot, thread):

    # fetch starter message
    url_pattern = r'https?:\/\/[^\s]+'
    starter_msg = await thread.fetch_message(thread.id)

    # content
    message = starter_msg.content
    poster_ID = thread.owner_id
    embeds = starter_msg.embeds
    attachments = starter_msg.attachments
    urls = re.findall(url_pattern, message)

    # Collect all messages in the thread
    messages = [message]
    all_urls = urls.copy()
    all_embeds = embeds.copy()
    all_attachments = attachments.copy()
    
    # Get all messages in the thread
    async for msg in thread.history(limit=None, oldest_first=True):
        if msg.id != thread.id:  # Skip the starter message as we already have it
            messages.append(msg.content)
            all_urls.extend(re.findall(url_pattern, msg.content))
            all_embeds.extend(msg.embeds)
            all_attachments.extend(msg.attachments)

    # Add to Qdrant collection
    await process_new_thread(bot, thread, messages, all_urls, all_embeds, all_attachments)

    # Log if successful
    await add_log_tag(bot, thread) 