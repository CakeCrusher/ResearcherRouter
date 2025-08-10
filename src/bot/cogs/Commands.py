import discord
from discord.ext import commands
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.qdrant.qdrant import search_papers, get_participants_from_results

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        allowed_channel=int(os.getenv('ALLOWED_CHANNELS'))
        return ctx.channel.id == allowed_channel
    
    @commands.command()
    async def ping(self, ctx):
        '''Shows Latency'''
        await ctx.send(f"Pong! {self.bot.latency*1000:.2f}ms")
    
    @commands.command()
    async def check_perms(self, ctx):
        '''Checks the bot's permission value for the current channel. (Admin only)'''
        if not ctx.author.guild_permissions.administrator:
            return
        perms = ctx.channel.permissions_for(ctx.guild.get_member(self.bot.user.id))
        await ctx.send(f"My permissions here:\n{perms}")

    @commands.command()
    async def instructions(self, ctx):
        await ctx.send(f"Try mentioning me with a question like: '{self.bot.user.mention} machine learning' or use `!search <topic>`")
        
    @commands.command()
    async def search(self, ctx, *, query):
        """
        Search for people who discussed a specific topic.
        Usage: !search <your question/topic>
        Example: !search machine learning
        """
        try:
            # Search Qdrant for relevant papers
            results = search_papers(query, limit=5)
            
            if not results:
                await ctx.send(f"❌ No discussions found about '{query}'. Try a different search term!")
                return
            
            # Get all participants from the search results
            participant_ids = get_participants_from_results(results)
            
            # Get usernames from Discord
            usernames = []
            for user_id in participant_ids:
                try:
                    user = await self.bot.fetch_user(user_id)
                    usernames.append(user.display_name)
                except:
                    usernames.append(f"User_{user_id}")
            
            # Get paper info for context
            paper_info = []
            for result in results[:5]:  # Show first 5 papers
                payload = result.payload
                title = payload.get('title', 'No title')
                summary = payload.get('summary', '')
                paper_info.append(f"📄 **{title}**")
                if summary:
                    paper_info.append(f"\t-Summary: {summary[:100]}...")
            
            # Create response
            response = f"🔍 **Search results for '{query}':**\n\n"
            response += "**People who discussed this topic:**\n"
            for username in sorted(usernames):
                response += f"👤 {username}\n"
            
            response += f"\n**Found {5 if len(results) > 5 else len(results)} related discussions:**\n"
            for info in paper_info:
                response += f"{info}\n"
            
            await ctx.send(response)
            
        except Exception as e:
            await ctx.send(f"❌ Error searching: {str(e)}")

    @commands.Cog.listener()
    async def on_message(self, message):
        # Test mode: validate channel
        channel = self.bot.get_channel(int(os.getenv('ALLOWED_CHANNELS')))
        if not message.channel == channel:
            return
        # Check if bot is mentioned
        if self.bot.user.mentioned_in(message) and not message.author.bot:
            # Extract the question (remove the @bot mention)
            content = message.content.replace(f'<@{self.bot.user.id}>', '').strip()
            
            if content:
                # Treat it as a search query
                await self.search(message.channel, query=content)
            else:
                await message.channel.send(f"👋 Hi! I can help you find people who discussed specific topics. Try mentioning me with a question like: '{self.bot.user.mention} machine learning' or use `!search <topic>`")

    @commands.command()
    async def listtags(self, ctx):
        """List all available tags in the current channel (for setup)"""
        if hasattr(ctx.channel, 'available_tags'):
            await ctx.send("**Available tags in this channel:**")
            for tag in ctx.channel.available_tags:
                await ctx.send(f"• **{tag.name}**: ID = `{tag.id}`")
        else:
            await ctx.send("❌ This channel doesn't have tags (not a forum channel)")

    @commands.command()
    async def indexall(self, ctx):
        """Index all existing threads in the forum channel (admin only)"""
        # Check if user has admin permissions
        if not ctx.author.guild_permissions.administrator:
            await ctx.send("❌ You need administrator permissions to use this command.")
            return
            
        await ctx.send("🔄 Starting to index all existing threads...")
        
        try:
            import os
            from bot.logic.add_thread import add_thread
            
            channel_ID = int(os.getenv('PAPER_CHANNEL_ID'))
            paper_channel = self.bot.get_channel(channel_ID)
            
            if not paper_channel:
                await ctx.send(f"❌ Could not find channel with ID: {channel_ID}")
                return
                
            indexed_count = 0
            total_threads = len(paper_channel.threads)
            
            for thread in paper_channel.threads:
                try:
                    await add_thread(self.bot, thread)
                    indexed_count += 1
                    await ctx.send(f"✅ Indexed thread: {thread.name}")
                except Exception as e:
                    await ctx.send(f"❌ Failed to index {thread.name}: {str(e)}")
            
            await ctx.send(f"🎉 **Indexing complete!** Indexed {indexed_count}/{total_threads} threads.")
            
        except Exception as e:
            await ctx.send(f"❌ Error during indexing: {str(e)}")

async def setup(bot):
    await bot.add_cog(Commands(bot))