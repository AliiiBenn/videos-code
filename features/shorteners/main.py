import discord
from discord.ext import commands

import os, dotenv

import pyshorteners



class UrlShorternerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.shortener = pyshorteners.Shortener()


    @commands.hybrid_command(name="short")
    async def short_url_command(self, ctx : commands.Context, *, url : str) -> discord.Message:
        await ctx.defer()
        
        return await ctx.send(self.shortener.tinyurl.short(url))
    
    
    

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
        command_prefix='!',
        intents=discord.Intents.all()
        )

    async def setup_hook(self) -> None:
        await self.add_cog(UrlShorternerCog(self))
        await self.tree.sync()

    async def on_ready(self):
        print('-------------')
        print(f'Logged in as {self.user}')
        print(f'Bot is ready.')

bot = MyBot()

if __name__ == '__main__':
    dotenv.load_dotenv()
    token = os.getenv('token')

    if token is None:
        raise ValueError('Token not found')

    bot.run(token)