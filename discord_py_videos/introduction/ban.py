import discord
from discord.ext import commands

import dotenv, os


bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


@bot.event
async def on_ready():
    print('Je suis en ligne !')
    
    
@bot.command()
async def ban(ctx : commands.Context,
              member : discord.Member,
              *,
              reason : str = "") -> discord.Message:
    
    is_in_private_messages = ctx.guild is None and isinstance(ctx.author, discord.User)
    has_permission = ctx.author.guild_permissions.ban_members
    is_member_bannable = ctx.author.top_role > member.top_role 
    
    
    if is_in_private_messages:
        return await ctx.send('This command cannot be used in private messages')
    
    if not has_permission:
        return await ctx.send('You do not have permission to use this command')

    if not is_member_bannable:
        return await ctx.send('You cannot ban this member')

    if reason == "":
        reason = "No reason provided"

    await member.ban(reason=reason)

    return await ctx.send(f':hammer: Banned {member.name}#{member.discriminator} for {reason}')



def main() -> None:
    dotenv.load_dotenv()

    TOKEN = os.getenv('TOKEN')

    if TOKEN is None:
        raise ValueError('Le token n\'est pas défini !')

    bot.run(TOKEN)


if __name__ == '__main__':
    main()