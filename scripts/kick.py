import discord 
from discord.ext import commands

import dotenv, os



bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')
    print('------')



@bot.command()
async def kick(ctx : commands.Context, member : discord.Member, reason : str) -> discord.Message:
    is_in_private_messages = ctx.guild is None and isinstance(ctx.author, discord.User)
    if is_in_private_messages:
        return await ctx.send('This command cannot be used in private messages')
    
    has_permission = ctx.author.guild_permissions.kick_members
    if not has_permission:
        return await ctx.send('You do not have permission to use this command')
    
    is_member_kickable = ctx.author.top_role > member.top_role
    if not is_member_kickable:
        return await ctx.send('You cannot kick this member')
    
    if reason == "":
        reason = "No reason provided"
        
    await member.kick(reason=reason)
    
    return await ctx.send(f':boot: Kicked {member.name}#{member.discriminator} for {reason}')


if __name__ == '__main__':
    dotenv.load_dotenv()
    TOKEN = os.getenv('TOKEN')
    
    if TOKEN is None:
        raise ValueError('Token not found')
    
    bot.run(TOKEN)