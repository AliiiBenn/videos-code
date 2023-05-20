import discord
from discord.ext import commands

import os, dotenv
from typing import Final

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
        command_prefix='!',
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