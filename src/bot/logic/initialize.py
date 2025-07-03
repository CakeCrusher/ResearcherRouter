import os
from .add_thread import *

# Redirect storage from Forum to store information to the vector database
# Logs all items in the forum at startup
async def initialize(bot):

    channel_ID = int(os.getenv('PAPER_CHANNEL_ID')) # replace channelID with cool-papers channelID
    sumID = int(os.getenv('SUMMARIZED_TAG'))
    logID = int(os.getenv('LOGGED_TAG'))
    paper_channel = bot.get_channel(channel_ID)

    # For each Thread channel in the Forum (cool-papers)
    for thread in paper_channel.threads:
        
        tags = [tag.id for tag in thread.applied_tags]
        if (sumID in tags) and (logID not in tags):

            await add_thread(bot, thread)
        