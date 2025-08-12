import os
from discord.ext import commands
from bot.logic.initialize import *
from bot.logic.on_message_update import *
from bot.logic.add_thread import *
from bot.logic.thread_summary import *
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.qdrant.qdrant import delete_thread

'''Updates thread when message events are triggered'''
async def update_message_data(bot, message):
        sum_id = int(os.getenv('SUMMARIZED_TAG'))
    # If message author is bot
        if message.author == bot.user:
            return
        # Only process messages in forum threads
        if not hasattr(message.channel, 'parent_id'):
            return
        tags = [tag.id for tag in message.channel.applied_tags]
        # Starter message: skip
        if message == message.channel.starter_message:
            return
        # Not Summarized channel: skip
        if sum_id not in tags:
            return
        
        # Add the information from the message to the thread's data
        await on_message_update(message)
        return


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.forum_id = int(os.getenv('PAPER_CHANNEL_ID'))
        self.sum_id = int(os.getenv('SUMMARIZED_TAG'))

    # Logs all Forum threads that are available upon startup
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Success! Logged in as {self.bot.user}')
        await initialize(self.bot) # load all Summarized threads

    # Add the poster's ID, possible attachments or embeds, and messages
    @commands.Cog.listener()
    async def on_thread_create(self, thread):
        # Skip if not cool-papers
        if not thread.parent_id == self.forum_id:
            return
        
        # Check the tags
        tags = [tag.id for tag in thread.applied_tags]
        if self.sum_id not in tags:
            return
        
        await add_thread(self.bot, thread)
        return
    
    @commands.Cog.listener()
    async def on_thread_delete(self, thread):

        if not thread.parent_id == self.forum_id:
            return
        
        tags = [tag.id for tag in thread.applied_tags]
        if self.sum_id not in tags:
            return
        
        await delete_thread(thread)
        return

    # Logs the channel if 'Sumbitted' tag is added after init thread creation
    @commands.Cog.listener()
    async def on_thread_update(self, before, after):

        before_tags = [tag.id for tag in before.applied_tags]
        after_tags = [tag.id for tag in after.applied_tags]

        if (self.sum_id not in before_tags) and (self.sum_id in after_tags):
            await add_thread(self.bot, after)
        return
    
    # Listen for new messages in threads
    
    @commands.Cog.listener()
    async def on_message(self, message):
        await update_message_data(self.bot, message)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        await update_message_data(self.bot, message)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        await update_message_data(self.bot, after)    
        
        
    # Update metadata: add reactions to messages
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        if not hasattr(channel, 'parent_id'):
            return
        if not channel.parent_id == self.forum_id:
            return
        
        tags = [tag.id for tag in channel.applied_tags]
        if self.sum_id not in tags:
            return

        await on_message_update(message, payload, channel)
        return
    
    # Update metadata: remove reactions to messages
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):

        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        if not hasattr(channel, 'parent_id'):
            return
        if not channel.parent_id == self.forum_id:
            return
        
        tags = [tag.id for tag in channel.applied_tags]
        if self.sum_id not in tags:
            return

        await on_message_update(message, payload, channel)
        return


    # @commands.Cog.listener()
    # async def on_command_error(self, ctx, error):
    #     '''Listens to command errors and responds'''
    #     if isinstance(error, commands.CheckFailure):
    #         await ctx.send("Commands not active in this channel.")

async def setup(bot):
    await bot.add_cog(Events(bot))