import discord
from discord.ext import commands

import os, dotenv

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

bot = MyBot()

@bot.command()
async def test(ctx : commands.Context):
    embed1 = discord.Embed(
        title="test1",
    )
    
    embed1.add_field(name="test", value="test description", inline=True)
    embed1.add_field(name="test", value="test description", inline=True)
    
    embed2 = discord.Embed(
        title="test2",
    )
    
    embed2.add_field(name="test", value="test description", inline=False)
    embed2.add_field(name="test", value="test description", inline=False)
    
    await ctx.send(embed=embed1)
    await ctx.send(embed=embed2)

if __name__ == '__main__':
    dotenv.load_dotenv()
    token = os.getenv('token')

    if token is None:
        raise ValueError('Token not found')

    bot.run(token)