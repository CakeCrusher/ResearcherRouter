import re
import sys
import os
from bot.pydantic_configure import *
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.qdrant.qdrant import process_thread_update

'''
Called whenever a thread is updated 
Thread in cool-papers receives a new message
'''
async def on_message_update(message):

    url_pattern = r'https?:\/\/[^\s]+'

    attach_obj = [
        AttachmentSerialized(
            filename = attached.filename,
            attachment_id = attached.id,
            url = attached.url,
            byte_size = attached.size,
            media_type = attached.content_type
        )
        for attached in message.attachments
    ]

    # msg content
    message_obj = CommentSerialized(
        author_id = message.author.id,
        comment = message.content,
        url = re.findall(url_pattern, message.content),
        attachments = attach_obj,
        created_at = message.created_at
    )

    # testing print(message_obj)

    # Update the paper in Qdrant collection
    await process_thread_update(message.channel.id, message_obj)