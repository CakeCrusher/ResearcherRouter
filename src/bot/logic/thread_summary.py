import discord
import os
'''
Check whether the payload Emoji is the correct one.
False: Summary = None
True: Summary = message.content

NOTE: ENABLE MANAGE MESSAGES FOR BOT IN FORUM
'''
def can_manage_thread(payload, thread):
    allowed_role_ids = [int(id) for id in os.getenv('ALLOWED_ROLE_IDS', '').split(',')]
    member_roles = [role.id for role in payload.member.roles]
    has_role = False
    for role in allowed_role_ids:
        if role in member_roles:
            has_role = True
 
    return (payload.member == thread.owner
        or has_role
        or payload.member.guild_permissions.administrator
    )

async def thread_summary(message, payload, thread):

    emoji = '📌'
    emoji_count = 0
    pin_reaction = discord.utils.get(message.reactions, emoji=emoji)
    messages = [message async for message in thread.history(limit=None)]
    this_reaction = payload.emoji

    permission = can_manage_thread(payload, thread)     

    '''Removes extra 📌 emojis'''
    for msg in messages:
        for reaction in msg.reactions:
            if reaction.emoji == emoji:
                if not permission:
                    await message.remove_reaction(this_reaction, payload.member)
                    print('Reaction not allowed: not message author or admin.')
                emoji_count += 1
            if (emoji_count > 1) and (this_reaction.name == emoji):  
                print('This channel already contains a summary!')
                await message.remove_reaction(this_reaction, payload.member)
                return

    if not payload.emoji.name == emoji:    # If the reaction != emoji
        print('Invalid reaction: no action.')
        return
    if not pin_reaction or pin_reaction.count > 1: # If reactions > 1 or reaction DNE
        return
    
    summary = message.content
    return summary