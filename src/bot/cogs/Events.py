import os
from discord.ext import commands
from logic.initialize import *
from logic.on_message_update import *
from logic.add_thread import *

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

    # add_thread() upon creation of a new thread
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
    
    # add_thread() and logs the channel if 'Sumbitted' tag is added after init thread creation
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
    # Listen for user @BOT mentions
    # Updates thread when new messages are detected
    @commands.Cog.listener()
    async def on_message(self, message):

        # If message author is bot, return
        if message.author == self.bot.user:
            return
            
        # When bot is mentioned
        for user in message.mentions:
            
            if user == self.bot.user:
                # Extract the question (remove the @bot mention)
                content = message.content.replace(f'<@{self.bot.user.id}>', '').strip()
                if content:
                    # Treat it as a search query
                    await self.search(message.channel, query=content)
                else:
                    await message.channel.send("👋 Hi! I can help you find people who discussed specific topics. Try mentioning me with a question like: '@bot machine learning' or use `!search <topic>`")
            
        # If the message is sent in cool-papers
        if message.channel.parent.id == self.forum_id:
            # Add the information from the message to the thread's data
            await on_message_update(message)
            return

async def setup(bot):
    await bot.add_cog(Events(bot))