import re
from .add_log_tag import add_log_tag
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.qdrant.qdrant import process_new_thread
from pydantic_configure import *
import json

# Add channel to the database
async def add_thread(bot, thread):
    
    url_pattern = r'https?:\/\/[^\s]+'
 
    comment_obj = []
    async for message in thread.history(limit=None, oldest_first=True):
        # check if the message contains attachments first
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
        comment_obj.append(
            CommentSerialized(
                author_id = message.author.id,
                comment = message.content,
                url = re.findall(url_pattern, message.content),
                attachments = attach_obj
            )
        ) 
    
    # content
    thread_obj = ThreadSerialized(
        thread_id = thread.id,
        owner_id = thread.owner_id,
        topic = thread.name,
        comments = comment_obj
    )
    '''
    get content in 
    python dict format: thread_obj.model_dump()
    json format: thread_obj.model_dump_json(indent=2)
    '''

    # uncomment, but arguments should be changed    
    # await process_new_thread(bot, thread, messages, urls, embeds, attachments)

    '''
    NOTE: need to verify whether the database insertion was successful,
    then add_log_tag
    '''
    # await add_log_tag(bot, thread)