import re
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.qdrant.qdrant import process_thread_update

# Update the database in real time whenver a new thread is posted
# Call when an on_thread_update event occurs
# Check for new ForumChannel events and update the database
async def updateThreadData(message):

    url_pattern = r'https?:\/\/[^\s]+'
    
    # content
    thread_id = message.channel.id
    content = message.content
    urls = re.findall(url_pattern, content)
    embeds = message.embeds
    attachments = message.attachments
    commenter_id = message.author.id  # Track who posted this message

    # Update the paper in Qdrant collection
    await process_thread_update(thread_id, content, urls, embeds, attachments, commenter_id)