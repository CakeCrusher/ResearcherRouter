import discord

'''
Check whether the payload Emoji is the correct one.
False: Summary = None
True: Summary = message.content

NOTE: ENABLE MANAGE MESSAGES FOR BOT IN FORUM
'''
async def thread_summary(message, payload, channel):

    emoji = '📌'
    emoji_count = 0
    pin_reaction = discord.utils.get(message.reactions, emoji=emoji)
    messages = [message async for message in channel.history(limit=None)]
    this_reaction = payload.emoji


    '''Removes extra 📌 emojis'''
    for msg in messages:
        for reaction in msg.reactions:
            if reaction.emoji == emoji:
                emoji_count += 1
            if (emoji_count > 1) and (this_reaction.name == emoji):  
                print('This channel already contains a summary!')
                await message.remove_reaction(this_reaction, message.author)
                return

    if not payload.emoji.name == emoji:    # If the reaction != emoji
        print('Invalid reaction: no action.')
        return
    if not pin_reaction or pin_reaction.count > 1: # If reactions > 1 or reaction DNE
        return
    
    summary = message.content
    return summary