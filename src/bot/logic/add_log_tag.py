import os

async def add_log_tag(bot, thread):
    logID = int(os.getenv('LOGGED_TAG'))
    channel_id = int(os.getenv('PAPER_CHANNEL_ID'))
    paper_channel = bot.get_channel(channel_id)
    logged_tag = [tag for tag in paper_channel.available_tags if tag.id == logID]
    thread_tag_ids = [tag.id for tag in thread.applied_tags]

    if thread.archived: # Try to add tag to thread, 
        try:
            await thread.edit(archived=False) 
        except Exception as e:
            print(f"Could not unarchive thread {thread.name}: {e}")
            return
    if logID in thread_tag_ids:
        return
    updated_tags = thread.applied_tags + logged_tag
    await thread.edit(applied_tags=updated_tags) # mark the channel as logged