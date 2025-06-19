import re
from .addTag import add_log_tag
# If the channel updates its tag

# Add channel to the database
async def addThread(bot, thread):
    
    url_pattern = r'https?:\/\/[^\s]+'

    # content
    thread_ID = thread.id       # int
    poster_ID = thread.owner_id # int
    commenter_IDs = []          # [int]
    urls = []                   # [str]
    messages = []               # [str]
    embeds = []                 # [Embed]
    attachments = []            # [Attachment]

    thread_members = await thread.fetch_members()
    for commenter in thread_members:
            if commenter.id not in commenter_IDs and commenter.id != poster_ID:
                commenter_IDs.append(commenter.id)

    async for message in thread.history(limit=None, oldest_first=True):
        messages.append(message.content)
        embeds.extend(message.embeds)
        attachments.extend(message.attachments) 
        urls.extend(re.findall(url_pattern, message.content))


    print(messages)
    print(thread_ID)

    '''
    Qdrant API here
    '''

    # Refer to API documentation to get Embed and Attachment information
    # Log if successful
    await add_log_tag(bot, thread)