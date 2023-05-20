import discord
from discord.ext import commands

import os, dotenv





class AutoModerationCog(commands.Cog):
    def __init__(self, BOT : commands.Bot) -> None:
        self.BOT = BOT
        
        
    async def is_maj_spam(self, message : discord.Message) -> bool:
        print(message.content)
        maj_count = sum(1 for cara in message.content if cara.isupper())
        MAXIMUM_PERCENTAGE = 50 
        
        if maj_count == 0 or len(message.content) < 5:
            return False 
        
        return (maj_count / len(message.content)) * 100 > MAXIMUM_PERCENTAGE
    
    
        
    @commands.Cog.listener(name="on_message")
    async def check_for_auto_moderation(self, message : discord.Message) -> None:
        if message.author.BOT:
            return
        
        checkers = [self.is_maj_spam]
        
        for checker in checkers:
            if await checker(message):
                await message.delete()
                await message.channel.send(f"{message.author.mention} don't spam !")
                break


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
        command_prefix='!',
        intents=discord.Intents.all()
        )

    async def setup_hook(self) -> None:
        await self.add_cog(AutoModerationCog(self))
        
        await self.tree.sync()

    async def on_ready(self):
        print('-------------')
        print(f'Logged in as {self.user}')
        print(f'Bot is ready.')



if __name__ == '__main__':
    BOT = MyBot()
    
    
    dotenv.load_dotenv()
    token = os.getenv('token')

    if token is None:
        raise ValueError('Token not found')

    BOT.run(token)