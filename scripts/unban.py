import discord 
from discord.ext import commands

import dotenv, os



bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')
    print('------')


@bot.command()
async def unban(ctx : commands.Context, member : str, *, reason : str = "") -> discord.Message:
    is_in_private_messages = ctx.guild is None and isinstance(ctx.author, discord.User)
    if is_in_private_messages:
        return await ctx.send('This command cannot be used in private messages')
    
    has_permission = ctx.author.guild_permissions.ban_members
    if not has_permission:
        return await ctx.send('You do not have permission to use this command')
    
    banned_users = [ban_entry async for ban_entry in ctx.guild.bans()]
    member_name, member_discriminator = member.split('#')
    
    for ban_entry in banned_users:
        user = ban_entry.user
        
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user, reason=reason)
            return await ctx.send(f':hammer: Unbanned {user.name}#{user.discriminator}')
        
    return await ctx.send(f'Could not find user {member_name}#{member_discriminator}')



if __name__ == '__main__':
    dotenv.load_dotenv()
    TOKEN = os.getenv('TOKEN')
    
    if TOKEN is None:
        raise ValueError('Token not found')
    
    bot.run(TOKEN)