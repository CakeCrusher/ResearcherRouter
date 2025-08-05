import re
from .add_log_tag import add_log_tag
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.qdrant.qdrant import process_new_thread, upload_success
from bot.pydantic_configure import *

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
                media_type = attached.content_type,
            )
            for attached in message.attachments
        ]
        comment_obj.append(
            CommentSerialized(
                author_id = message.author.id,
                comment = message.content,
                url = re.findall(url_pattern, message.content),
                attachments = attach_obj,
                created_at = message.created_at
            )
        ) 
    
    # content
    thread_obj = ThreadSerialized(
        id = thread.id,
        owner_id = thread.owner_id,
        topic = thread.name,
        tags = [tag.name for tag in thread.applied_tags],
        comments = comment_obj,
        created_at = thread.created_at
    )

    '''
    get content in 
    python dict format: thread_obj.model_dump()
    json format: thread_obj.model_dump_json(indent=2)
    '''
    print(thread_obj.model_dump_json(indent=2))
  
    await process_new_thread(thread_obj)
    success = await upload_success(thread)

    # need to verify whether the database insertion was successful, then add_log_tag
    ''' Remove comment when testing is complete '''
    # if success:
    #     await add_log_tag(bot, thread)