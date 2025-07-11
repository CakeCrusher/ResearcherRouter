import os

# NOTE: No need to check if tag is already applied - checks have been performed prior to calling add_log_tag
async def add_log_tag(bot, thread):
    logID = int(os.getenv('LOGGED_TAG'))
    channel_id = int(os.getenv('PAPER_CHANNEL_ID'))
    paper_channel = bot.get_channel(channel_id)

    logged_tag = [tag for tag in paper_channel.available_tags if tag.id == logID]
    updated_tags = thread.applied_tags + logged_tag
    await thread.edit(applied_tags=updated_tags) # mark the channel as logged