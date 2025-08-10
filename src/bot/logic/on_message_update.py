import re
import sys
import os
import discord
from bot.pydantic_configure import *
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.qdrant.qdrant import process_thread_update
from .thread_summary import thread_summary

'''
Called whenever a thread is updated 
Thread in cool-papers receives a new message
'''
async def on_message_update(message, payload=None, channel=None):

    url_pattern = r'https?:\/\/[^\s]+'
    summary = None
    if payload:
        summary = await thread_summary(message, payload, channel)

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

    message_obj = CommentSerialized(
        author_id = message.author.id,
        comment = message.content,
        url = re.findall(url_pattern, message.content),
        attachments = attach_obj,
        reactions = [reaction.emoji for reaction in message.reactions],
        created_at = message.created_at
    )

    '''testing statement'''
    print(message_obj.model_dump_json(indent=2))

    # Update the paper in Qdrant collection
    await process_thread_update(message.channel.id, message_obj, summary)