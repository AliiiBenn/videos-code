import discord
from discord.ext import commands

import aiosqlite

from database import get_member_guild_messages, increment_member_channel_messages


class GetGuildMessagesCog(commands.Cog):
    def __init__(self, bot : commands.Bot, connection : aiosqlite.Connection) -> None:
        self.bot = bot
        self.connection = connection
        
        
    def set_embed(self, member : discord.Member, messages : int) -> discord.Embed:
        embed = discord.Embed(
            title=f"Messages de {member.name}",
            description=f"{member.name} a envoyé {messages} messages sur ce serveur!",
            color=member.color
        )
        
        embed.set_thumbnail(url=member.display_avatar.url)
        
        bot_user = self.bot.user 
        
        embed.set_author(
            name=bot_user.name,
            icon_url=bot_user.display_avatar.url
        )
        
        return embed
        
        
    @commands.hybrid_command(name="get_guild_messages")
    async def get_guild_messages(self,
                                 ctx : commands.Context[commands.Bot],
                                 member : discord.Member = commands.Author) -> discord.Message:
        
        if ctx.guild is None:
            raise commands.NoPrivateMessage()
        
        messages = await get_member_guild_messages(self.connection,
                                                   member,
                                                   ctx.guild.id)
        
        embed = self.set_embed(member, messages)
        
        
        return await ctx.send(embed=embed)
    
    
    @commands.Cog.listener("on_message")
    async def increment_guild_messages(self, message : discord.Message) -> None:
        if message.author.bot or isinstance(message.author, discord.User):
            return
        
        await increment_member_channel_messages(self.connection,
                                                message.author,
                                                message.channel.id)
    
        



async def setup(bot : commands.Bot) -> None:
    connection = await aiosqlite.connect("messages.db")
    await bot.add_cog(GetGuildMessagesCog(bot, connection))