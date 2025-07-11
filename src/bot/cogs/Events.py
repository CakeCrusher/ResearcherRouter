import os
from discord.ext import commands
from bot.logic.initialize import *
from bot.logic.on_message_update import *
from bot.logic.add_thread import *

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.forum_id = int(os.getenv('PAPER_CHANNEL_ID'))
        self.sumID = int(os.getenv('SUMMARIZED_TAG'))

    # initialize() when bot is ready
    # Logs all Forum threads that are available upon startup
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Success! Logged in as {self.bot.user}')
        await initialize(self.bot) # load all Summarized threads

    # getThreadData() when upon creation of a new thread
    # Add the poster's ID, possible attachments or embeds, and messages
    @commands.Cog.listener()
    async def on_thread_create(self, thread):
        # Skip if not cool-papers
        if not thread.parent_id == self.forum_id:
            return
        
        # Check the tags
        tags = [tag.id for tag in thread.applied_tags]
        if self.sumID not in tags:
            return
        
        await add_thread(self.bot, thread)
        return

    # addMember() on event trigger
    # Add new member to the data
    @commands.Cog.listener()
    async def on_thread_member_join(self, member):
        # Skip if not cool-papers forum channel
        if not member.channel.parent_id == self.forum_id:
            return
        
        # Check the tags
        tags = [tag.id for tag in member.channel.applied_tags]
        if self.sumID not in tags:
            return
        
        # Note: addMember function was removed, so we'll skip this for now
        return
    
    # logTag()
    # Logs the channel if 'Sumbitted' tag is added after init thread creation
    @commands.Cog.listener()
    async def on_thread_update(self, before, after):

        before_tags = [tag.id for tag in before.applied_tags]
        after_tags = [tag.id for tag in after.applied_tags]

        # If the forum is cool-papers
        if after.parent.id == self.forum_id:
            if (self.sumID not in before_tags) and (self.sumID in after_tags):
                await add_thread(self.bot, after)
        return
    
    # Listen for new messages in threads
    # Updates thread when new messages are detected
    @commands.Cog.listener()
    async def on_message(self, message):
        # If message author is bot
        if message.author == self.bot.user:
            return
            
        # Only process messages in forum threads
        if not hasattr(message.channel, 'parent_id'):
            return
            
        # If the message is sent in cool-papers forum threads
        if message.channel.parent_id == self.forum_id:
            # Add the information from the message to the thread's data
            await on_message_update(message)
            return

async def setup(bot):
    await bot.add_cog(Events(bot))