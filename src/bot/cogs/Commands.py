# NOTE : Might not need this file

import discord
from discord.ext import commands
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.qdrant.qdrant import search_papers, get_participants_from_results

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("pong!")
    
    @commands.command()
    async def check_perms(self, ctx):
        perms = ctx.channel.permissions_for(ctx.guild.get_member(self.bot.user.id))
        await ctx.send(f"My permissions here:\n{perms}")

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
            for result in results[:3]:  # Show first 3 papers
                payload = result.payload
                title = payload.get('title', 'No title')
                summary = payload.get('summary', '')
                paper_info.append(f"📄 **{title}**")
                if summary:
                    paper_info.append(f"   Summary: {summary[:100]}...")
            
            # Create response
            response = f"🔍 **Search results for '{query}':**\n\n"
            response += "**People who discussed this topic:**\n"
            for username in sorted(usernames):
                response += f"👤 {username}\n"
            
            response += f"\n**Found {len(results)} related discussions:**\n"
            for info in paper_info:
                response += f"{info}\n"
            
            await ctx.send(response)
            
        except Exception as e:
            await ctx.send(f"❌ Error searching: {str(e)}")

    @commands.Cog.listener()
    async def on_message(self, message):
        # Check if bot is mentioned
        if self.bot.user.mentioned_in(message) and not message.author.bot:
            # Extract the question (remove the @bot mention)
            content = message.content.replace(f'<@{self.bot.user.id}>', '').strip()
            
            if content:
                # Treat it as a search query
                await self.search(message.channel, query=content)
            else:
                await message.channel.send("👋 Hi! I can help you find people who discussed specific topics. Try mentioning me with a question like: '@bot machine learning' or use `!search <topic>`")

async def setup(bot):
    await bot.add_cog(Commands(bot))