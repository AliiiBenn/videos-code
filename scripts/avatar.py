import discord 
from discord.ext import commands

import dotenv, os

from typing import Optional, Union


bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')
    print('------')



@bot.command(name="avatar")
async def send_user_avatar(ctx : commands.Context, user : Optional[Union[discord.User, discord.Member]] = None) -> discord.Message:
    if user is None:
        user = ctx.author
    
    embed = discord.Embed(title=f"{user.name}#{user.discriminator}'s avatar", description=f"[{user.name} avatar link]({user.display_avatar.url})", color=0x2F3136)
    embed.set_image(url=user.display_avatar.url)
    
    return await ctx.send(embed=embed)
    
    


if __name__ == '__main__':
    dotenv.load_dotenv()
    TOKEN = os.getenv('TOKEN')
    
    if TOKEN is None:
        raise ValueError('Token not found')
    
    bot.run(TOKEN)