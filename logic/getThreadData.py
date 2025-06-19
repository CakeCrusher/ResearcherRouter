import re
from .addTag import add_log_tag

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

    '''
    Qdrant API here
    '''

    # Log if successful
    await add_log_tag(bot, thread)