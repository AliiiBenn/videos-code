import discord
from discord.ext import commands

import aiosqlite

from database import get_member_channels_messages, increment_member_channel_messages


class ChannelMessagesCountCog(commands.Cog):
    def __init__(self, bot : commands.Bot, connection : aiosqlite.Connection) -> None:
        self.bot = bot
        self.connection = connection
        
        
    def set_channel_name(self, channel : discord.abc.GuildChannel) -> str:
        name = channel.name
        
        if channel.category is not None:
            name = f"{channel.category.name.upper()}/{channel.name}"
            
        return name
        
    def set_channels_fields(self,
                            embed : discord.Embed,
                            guild : discord.Guild,
                            channels : list[tuple[int, int]]) -> None:
        
        for channel in channels:
            guild_channel = guild.get_channel(channel[0])
            
            if guild_channel is None:
                raise commands.ChannelNotFound(channel[0])
            
            count = channel[1]
        
            name = self.set_channel_name(guild_channel)
            
            embed.add_field(name=name, value=f"{count} messages envoyés")
        
        
    def create_messages_embed(self,
                              member : discord.Member,
                              guild : discord.Guild,
                              channels : list[tuple[int, int]]) -> discord.Embed:
        
        embed = discord.Embed(
            title=f"Messages de {member.name}",
            description="Liste des messages par channel",
            color=member.color
        )
        
        embed.set_thumbnail(url=member.display_avatar.url)
        
        bot_user = self.bot.user
        embed.set_author(
            name=bot_user.name,
            icon_url=bot_user.display_avatar.url
        )
        
        self.set_channels_fields(embed, guild, channels)
            
        return embed
    
        
    @commands.hybrid_command(name="get_channel_messages")
    async def get_channel_messages(self,
                                   ctx : commands.Context[commands.Bot],
                                   member : discord.Member = commands.Author) -> discord.Message:
        
        if ctx.guild is None:
            raise commands.NoPrivateMessage()
        
        channels = await get_member_channels_messages(self.connection, member)
        
                
        embed = self.create_messages_embed(member, ctx.guild, channels)
        
        return await ctx.send(embed=embed)
        
        
    @commands.Cog.listener("on_message")
    async def increment_channel_messages(self, message : discord.Message) -> None:
        if message.author.bot or isinstance(message.author, discord.User):
            return
        
        await increment_member_channel_messages(self.connection,
                                                message.author, 
                                                message.channel.id)
        
        
        


async def setup(bot : commands.Bot) -> None:
    connection = await aiosqlite.connect("messages.db")
    await bot.add_cog(ChannelMessagesCountCog(bot, connection))