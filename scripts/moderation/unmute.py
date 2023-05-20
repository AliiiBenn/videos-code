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
async def unmute(ctx : commands.Context, member : discord.Member, *, reason : str = "") -> discord.Message:
    is_in_private_messages = ctx.guild is None and isinstance(ctx.author, discord.User)
    if is_in_private_messages:
        return await ctx.send('This command cannot be used in private messages')
    
    has_permission = ctx.author.guild_permissions.manage_channels
    if not has_permission:
        return await ctx.send('You do not have permission to use this command')
    
    is_member_kickable = ctx.author.top_role > member.top_role
    if not is_member_kickable:
        return await ctx.send('You cannot unmute this member')
    
    is_in_voice_channel = member.voice is not None and member.voice.channel is not None
    if not is_in_voice_channel:
        return await ctx.send('This member is not in a voice channel')
    
    if reason == "":
        reason = "No reason provided"
        
    await member.edit(mute=False,reason=reason)
    
    return await ctx.send(f'unmuted {member.name}#{member.discriminator} for {reason}')


if __name__ == '__main__':
    dotenv.load_dotenv()
    TOKEN = os.getenv('TOKEN')
    
    if TOKEN is None:
        raise ValueError('Token not found')
    
    BOT.run(TOKEN)