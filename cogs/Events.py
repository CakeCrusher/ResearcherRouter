import os
from discord.ext import commands
from logic.initialize import *
from logic.updateThreadData import *
from logic.getThreadData import *
from logic.addMember import *
from logic.addThread import *
# Modify if needed

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
        
        await getThreadData(self.bot, thread)
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
        
        await addMember(member)
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
                await addThread(self.bot, after)
        return
    
    # Listen for new messages in threads
    # Listen for user @BOT mentions
    # Updates thread when new messages are detected
    @commands.Cog.listener()
    async def on_message(self, message):
        # If message author is bot
        if message.author == self.bot.user:
            return
            
        # When bot is mentioned
        for user in message.mentions:
            if user == self.bot.user:
                return
            
        # If the message is sent in cool-papers
        if message.channel.parent.id == self.forum_id:
            # Add the information from the message to the thread's data
            await updateThreadData(message)
            return
    
        # await message.channel.send(message.content)
        # await self.bot.process_commands(message)

async def setup(bot):
    await bot.add_cog(Events(bot))