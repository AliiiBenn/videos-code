import discord
from discord.ext import commands

import os, dotenv
from typing import Final
import json



def get_prefixes(BOT, message):
    if message.guild is None:
        return ['!']
    
    guild_id = str(message.guild.id)
    
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
        
    
    is_guild_defined = guild_id in prefixes
    if not is_guild_defined:
        return ['!']
    
    guild_prefixes = prefixes[guild_id]
    return guild_prefixes




class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
        command_prefix=get_prefixes,
        intents=discord.Intents.all()
        )

    async def setup_hook(self) -> None:
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