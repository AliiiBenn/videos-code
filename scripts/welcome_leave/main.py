import discord
from discord.ext import commands

import os, dotenv
from typing import Final, json


class WelcomeLeaveMessageCog(commands.Cog):
    def __init__(self, BOT):
        self.BOT = BOT


    def get_channel(self, guild : discord.Guild) -> discord.TextChannel | None:
        channel = guild.system_channel
        if channel is not None:
            return channel
        
        with open('data.json', 'r') as f:
            welcome_channels = json.load(f)
            
        guild_id = str(guild.id)
        channel_id = welcome_channels[guild_id]
        
        new_channel = guild.get_channel(channel_id)
        
        if not isinstance(new_channel, discord.TextChannel):
            return None
        
        return new_channel

    @commands.Cog.listener("on_member_join")
    async def welcome_message(self, member : discord.Member):
        guild = member.guild
        channel = self.get_channel(guild)
        
        if channel is None:
            return
        
        return await channel.send(f'Welcome {member.mention} to {guild.name}!')
        
        
    @commands.Cog.listener("on_member_remove")
    async def leave_message(self, member : discord.Member):
        guild = member.guild
        channel = self.get_channel(guild)
        
        if channel is None:
            return

        await channel.send(f'{member.mention} has left {guild.name}!')
        
        
    @commands.hybrid_command(name="set_welcome_channel")
    @commands.guild_only()
    async def set_welcome_channel(self, ctx : commands.Context, channel : discord.TextChannel) -> discord.Message:
        guild_id = str(ctx.guild.id)
        
        with open('data.json', 'r') as f:
            welcome_channels = json.load(f)
            
        welcome_channels[guild_id] = channel.id
        
        with open('data.json', 'w') as f:
            json.dump(welcome_channels, f, indent=4)
            
        return await ctx.send(f'Welcome channel has been set to {channel.mention}!')


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
        command_prefix='!',
        intents=discord.Intents.all()
        )

    async def setup_hook(self) -> None:
        await self.add_cog(WelcomeLeaveMessageCog(self))
         
        await self.tree.sync()

    async def on_ready(self):
        print('-------------')
        print(f'Logged in as {self.user}')
        print(f'Bot is ready.')

BOT = MyBot()

if __name__ == '__main__':
    dotenv.load_dotenv()
    token = os.getenv('token')

    if token is None:
        raise ValueError('Token not found')

    BOT.run(token)