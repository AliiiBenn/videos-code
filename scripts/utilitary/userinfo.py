import discord 
from discord.ext import commands

import os, dotenv
from typing import Final



BOT : Final[commands.Bot] = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@BOT.event
async def on_ready():
    print(f'Logged in as {BOT.user.name} - {BOT.user.id}')
    print('------')


@BOT.command(name="userinfo")
async def user_info(ctx : commands.Context, user : discord.User | discord.Member | None = None) -> discord.Message:
    if user is None:
        user = ctx.author
    
    embed = discord.Embed(title=f"{user.name}#{user.discriminator}'s info", description=f"ID: {user.id}", color=0x2F3136)
    embed.set_thumbnail(url=user.display_avatar.url)
    embed.add_field(name="Created at", value=user.created_at.strftime("%d/%m/%Y %H:%M:%S"), inline=False)
    
    
    if isinstance(user, discord.Member):
        embed.add_field(name="Joined at", value=user.joined_at.strftime("%d/%m/%Y %H:%M:%S"), inline=False)
        embed.add_field(name="Top role", value=user.top_role.mention, inline=False)
        embed.add_field(name="Bot", value=user.BOT, inline=False)
        embed.add_field(name="Nickname", value=user.nick, inline=False)
        embed.add_field(name="Status", value=user.status, inline=False)
        embed.add_field(name="Activity", value=user.activity, inline=False)
        embed.add_field(name="Mobile", value=user.is_on_mobile(), inline=False)
        
    return await ctx.send(embed=embed)


if __name__ == '__main__':
    dotenv.load_dotenv()
    TOKEN = os.getenv('TOKEN')
    
    if TOKEN is None:
        raise ValueError('Token not found')
    
    BOT.run(TOKEN)