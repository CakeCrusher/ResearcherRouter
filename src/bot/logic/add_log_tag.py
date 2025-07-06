import os

async def add_log_tag(bot, thread):
    logID = int(os.getenv('LOGGED_TAG'))
    channel_id = int(os.getenv('PAPER_CHANNEL_ID'))
    paper_channel = bot.get_channel(channel_id)

    logged_tag = [tag for tag in paper_channel.available_tags if tag.id == logID] # The forum's 'Logged' tag
    
    # Check if the Logged tag is already applied
    current_tag_ids = [tag.id for tag in thread.applied_tags]
    if logID not in current_tag_ids:
        updated_tags = thread.applied_tags + logged_tag
        await thread.edit(applied_tags=updated_tags) # mark the channel as logged
    else:
        print(f"Thread {thread.name} already has Logged tag")