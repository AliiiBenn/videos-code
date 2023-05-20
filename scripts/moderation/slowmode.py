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
async def slowmode(ctx : commands.Context, seconds: int, channel : discord.TextChannel = None) -> discord.Message:
    is_in_private_messages = ctx.guild is None and isinstance(ctx.author, discord.User)
    if is_in_private_messages:
        return await ctx.send('This command cannot be used in private messages')
    
    has_permission = ctx.author.guild_permissions.manage_channels
    if not has_permission:
        return await ctx.send('You do not have permission to use this command')
    
    is_time_invalid = seconds < 0 or seconds > 21600
    if is_time_invalid:
        return await ctx.send('Time must be between 0 and 21600 seconds')
    
    if channel is None:
        channel = ctx.channel
    
    if seconds==0:
        await channel.edit(slowmode_delay=0)
        return await ctx.send(f':white_check_mark: Slowmode disabled')
    
    await channel.edit(slowmode_delay=seconds)
    return await ctx.send(f':white_check_mark: Set slowmode to {seconds} seconds')


if __name__ == '__main__':
    dotenv.load_dotenv()
    TOKEN = os.getenv('TOKEN')
    
    if TOKEN is None:
        raise ValueError('Token not found')
    
    BOT.run(TOKEN)