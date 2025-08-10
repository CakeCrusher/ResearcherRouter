import re
from .add_log_tag import add_log_tag
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.qdrant.qdrant import process_new_thread, thread_exists
from bot.pydantic_configure import *

# Add channel to the database
async def add_thread(bot, thread):
    
    url_pattern = r'https?:\/\/[^\s]+'
 
    comment_obj = []
    thread_urls = []
    participants = set()
    emoji = '📌'
    summary = None
    async for message in thread.history(limit=None, oldest_first=True):
        link = re.findall(url_pattern, message.content)
        thread_urls.extend(link)
        participants.add(message.author.id)

        '''Check if the message contains attachments first'''
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
        comment = CommentSerialized(
                author_id = message.author.id,
                comment = message.content,
                url = link,
                attachments = attach_obj,
                reactions = [reaction.emoji for reaction in message.reactions],
                created_at = message.created_at
            )
        
        '''Check for reactions: find summary'''
        for reaction in message.reactions:
            if reaction.emoji == emoji:
                summary = message.content
        comment_obj.append(comment) 
    
    # content
    thread_obj = ThreadSerialized(
        id = thread.id,
        owner_id = thread.owner_id,
        participants = [id for id in participants],
        topic = thread.name,
        tags = [tag.name for tag in thread.applied_tags],
        urls = thread_urls,
        summary = summary,
        comments = comment_obj,
        created_at = thread.created_at
    )

    '''
    get content in 
    python dict format: thread_obj.model_dump()
    json format: thread_obj.model_dump_json(indent=2)
    '''

    await process_new_thread(thread_obj)
    success = await thread_exists(thread)

    # need to verify whether the database insertion was successful, then add_log_tag
    ''' NOTE: Remove comment when testing is complete '''
    # if success:
    #     await add_log_tag(bot, thread)