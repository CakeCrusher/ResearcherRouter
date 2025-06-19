import re
# Import neccessary qdrant_client packages


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

    '''
    Qdrant API here
    '''