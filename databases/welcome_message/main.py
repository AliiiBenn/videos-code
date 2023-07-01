import discord
from discord.ext import commands

import os, dotenv


class WelcomeMessageCog(commands.Cog):
    def __init__(self, bot : commands.Cog) -> None:
        self.bot = bot
        
        
    @commands.Cog.listener("on_member_join")
    async def send_welcome_message(self, member : discord.Member) -> discord.Message:
        pass 
    
    
    @commands.hybrid_command(name="test")
    async def test(self, ctx : commands.Context) -> None:
        print(ctx.guild.system_channel)





class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
        command_prefix='!',
        intents=discord.Intents.all()
        )

    async def setup_hook(self) -> None:
        await self.add_cog(WelcomeMessageCog(self))
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