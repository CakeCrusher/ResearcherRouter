import os
from .add_thread import *
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.qdrant.qdrant import create_collection
# Redirect storage from Forum to store information to the vector database
# Logs all items in the forum at startup
async def initialize(bot):

    # Create the Qdrant collection on startup
    create_collection()
    channel_ID = int(os.getenv('PAPER_CHANNEL_ID')) # replace channelID with cool-papers channelID
    sumID = int(os.getenv('SUMMARIZED_TAG'))
    logID = int(os.getenv('LOGGED_TAG'))
    paper_channel = bot.get_channel(channel_ID)

    # Command line statements
    print(f"Initializing forum channel: {paper_channel.name}")
    print(f"Found {len(paper_channel.threads)} threads")

    # For each Thread channel in the Forum (cool-papers)
    for thread in paper_channel.threads:
        
        # We only need threads with the Summarized tag
        # Checks if the thread is Summarized but not Logged
        tags = [tag.id for tag in thread.applied_tags]
        if (sumID in tags) and (logID not in tags):
            await add_thread(bot, thread)
    
    print("Initialization complete!")
        