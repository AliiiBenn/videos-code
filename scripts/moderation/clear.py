import discord 
from discord.ext import commands

import os, dotenv
from typing import Final



BOT : Final[commands.Bot] = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@BOT.event
async def on_ready():
    print(f'Logged in as {BOT.user.name} - {BOT.user.id}')
    print('------')



@BOT.command()
async def clear(ctx : commands.Context, amount : int = 5) -> discord.Message:
    
    is_in_private_messages = ctx.guild is None and isinstance(ctx.author, discord.User)
    if is_in_private_messages:
        return await ctx.send('This command cannot be used in private messages')
    
    
    has_permission = ctx.author.guild_permissions.manage_messages
    if not has_permission:
        return await ctx.send('You do not have permission to use this command')
    
    is_text_channel = isinstance(ctx.channel, discord.TextChannel)
    if not is_text_channel:
        return await ctx.send('This command cannot be used in private messages')
    
    is_limit_reached = amount > 100
    if is_limit_reached:
        return await ctx.send('You cannot delete more than 100 messages at once')
    
    await ctx.channel.purge(limit=amount + 1) 
    
    return await ctx.send(f':wastebasket: Cleared {amount} messages', delete_after=10)


if __name__ == '__main__':
    dotenv.load_dotenv()
    TOKEN = os.getenv('TOKEN')
    
    if TOKEN is None:
        raise ValueError('Token not found')
    
    BOT.run(TOKEN)