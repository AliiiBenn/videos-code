import discord
from discord.ext import commands

import aiosqlite

from database import create_member_guild_messages, create_member_channel_messages, \
    create_guild_messages_table, create_channel_messages_table, \
        remove_member_channel_messages, remove_member_guild_messages
        


class SetupMessagesCog(commands.Cog):
    def __init__(self, bot : commands.Bot, connection : aiosqlite.Connection) -> None:
        self.bot = bot
        self.connection = connection
        
        
    @commands.hybrid_command(name="setup_guild_messages")
    async def setup_guild_messages(self,
                                   ctx : commands.Context[commands.Bot]) -> discord.Message:
        if ctx.guild is None:
            raise commands.NoPrivateMessage()
        
        for member in ctx.guild.members:
            if not member.bot:
                await create_member_guild_messages(self.connection, member, ctx.guild.id)
            
            
        return await ctx.send("Setup complete!")
    
    
    @commands.hybrid_command(name="setup_channel_messages")
    async def setup_channel_messages(self,
                                     ctx : commands.Context[commands.Bot]) -> discord.Message:
        if ctx.guild is None:
            raise commands.NoPrivateMessage()
        
        for channel in ctx.guild.text_channels:
            for member in ctx.guild.members:
                if not member.bot:
                    await create_member_channel_messages(self.connection, member, channel.id)
                
                
        return await ctx.send("Setup complete!")
    
    
    @commands.Cog.listener("on_member_join")
    async def on_member_join(self, member : discord.Member) -> None:
        await create_member_guild_messages(self.connection, member, member.guild.id)
        
    
    @commands.Cog.listener("on_guild_channel_create")
    async def on_guild_channel_create(self, channel : discord.abc.GuildChannel) -> None:
        for member in channel.guild.members:
            if not member.bot:
                await create_member_channel_messages(self.connection, member, channel.id)
                
    
    @commands.Cog.listener("on_member_remove")
    async def on_member_remove(self, member : discord.Member) -> None:
        await remove_member_guild_messages(self.connection, member, member.guild.id)
        
        
    @commands.Cog.listener("on_guild_channel_delete")
    async def on_guild_channel_delete(self, channel : discord.abc.GuildChannel) -> None:
        for member in channel.guild.members:
            if not member.bot:
                await remove_member_channel_messages(self.connection, member, channel.id)
        
        


async def setup(bot : commands.Bot) -> None:
    connection = await aiosqlite.connect("messages.db")
    
    await create_guild_messages_table(connection)
    await create_channel_messages_table(connection)
    
    await bot.add_cog(SetupMessagesCog(bot, connection))