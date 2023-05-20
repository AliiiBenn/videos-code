import discord 
from discord.ext import commands

import os, dotenv
from typing import Final



BOT : Final[commands.Bot] = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@BOT.event
async def on_ready():
    print(f'Logged in as {BOT.user.name} - {BOT.user.id}')
    print('------')


@BOT.command(name="serverinfo")
async def server_info(ctx : commands.Context) -> discord.Message:
    is_in_private_messages = ctx.guild is None and isinstance(ctx.author, discord.User)
    if is_in_private_messages:
        return await ctx.send('This command cannot be used in private messages')
    
    embed = discord.Embed(title=f'{ctx.guild.name}\'s info', color=discord.Color.blue())
    embed.set_thumbnail(url=ctx.guild.icon.url)
    embed.add_field(name='Owner', value=f'{ctx.guild.owner.name}#{ctx.guild.owner.discriminator}')
    embed.add_field(name='Members', value=ctx.guild.member_count)
    embed.add_field(name='Channels', value=len(ctx.guild.channels))
    embed.add_field(name='Roles', value=len(ctx.guild.roles))
    embed.add_field(name='Created at', value=ctx.guild.created_at.strftime('%d/%m/%Y %H:%M:%S'))
    
    return await ctx.send(embed=embed)


if __name__ == '__main__':
    dotenv.load_dotenv()
    TOKEN = os.getenv('TOKEN')
    
    if TOKEN is None:
        raise ValueError('Token not found')
    
    BOT.run(TOKEN)