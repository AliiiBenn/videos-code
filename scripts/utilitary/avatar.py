import discord 
from discord.ext import commands

import os, dotenv
from typing import Final

from typing import Optional, Union, Final


BOT : Final[commands.Bot] = commands.Bot(command_prefix='!', intents=discord.Intents.all())


@BOT.event
async def on_ready():
    print(f'Logged in as {BOT.user.name} - {BOT.user.id}')
    print('------')


@BOT.command(name="avatar")
async def send_user_avatar(ctx : commands.Context, user : Optional[Union[discord.User, discord.Member]] = None) -> discord.Message:
    
    is_user_not_defined = user is None
    if is_user_not_defined:
        user = ctx.author
    
    embed = discord.Embed(
        title=f"{user.name}#{user.discriminator}'s avatar",
        description=f"[{user.name} avatar link]({user.display_avatar.url})",
        color=0x2F3136
    )
    
    user_avatar_url = user.display_avatar.url
    embed.set_image(url=user_avatar_url)
    
    return await ctx.send(embed=embed)
    
    


if __name__ == '__main__':
    dotenv.load_dotenv()
    TOKEN = os.getenv('TOKEN')
    
    if TOKEN is None:
        raise ValueError('Token not found')
    
    BOT.run(TOKEN)