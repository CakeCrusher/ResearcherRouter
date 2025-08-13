import os
from .add_thread import *
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.qdrant.qdrant import create_collection, delete_thread_id
# Redirect storage from Forum to store information to the vector database
# Logs all items in the forum at startup
async def initialize(bot):

    # Create the Qdrant collection on startup
    create_collection()
    channel_ID = int(os.getenv('PAPER_CHANNEL_ID')) # replace channelID with cool-papers channelID
    channel_threads = 0
    sumID = int(os.getenv('SUMMARIZED_TAG'))
    logID = int(os.getenv('LOGGED_TAG'))
    paper_channel = bot.get_channel(channel_ID)

    # Command line statements
    print(f"Initializing forum channel: {paper_channel.name}")

    '''Checks each active summarized thread in the forum'''
    for thread in paper_channel.threads:
        thread = await bot.fetch_channel(thread.id)
        tags = [tag.id for tag in thread.applied_tags]
        if (sumID in tags) and (logID not in tags):
            await add_thread(bot, thread)
            channel_threads += 1
    
    '''Checks each archived summarized thread in the forum (old posts 30> days)'''
    async for thread in paper_channel.archived_threads(limit=None):
        thread = await bot.fetch_channel(thread.id)
        tags = [tag.id for tag in thread.applied_tags]
        if (sumID in tags) and (logID not in tags):
            await add_thread(bot, thread)
            channel_threads += 1
    print(f"Found {channel_threads} threads")
    print("Initialization complete!")
        