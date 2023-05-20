from typing import Final
import discord
from discord.ext import commands

import os, dotenv
from abc import ABC, abstractmethod
from enum import Enum, auto

""" 

This is the type of implementation that I do in my courses, it is more complex, readable, and maintainable than the YouTube version.
It use the Strategy Design Pattern, and the Factory Design Pattern with Abstraction. 

"""

class AutoModerationCheckerStrategy(ABC):
    @abstractmethod
    async def check(self, message : discord.Message) -> bool:
        pass


class MajSpamCheckerStrategy(AutoModerationCheckerStrategy):
    async def check(self, message : discord.Message):
        maj_count = sum(1 for caracter in message.content if caracter.isupper())
        MAXIMUM_PERCENTAGE = 50 
        
        if maj_count == 0 or len(message.content) < 5:
            return False 
        
        return (maj_count / len(message.content)) * 100 > MAXIMUM_PERCENTAGE
    
    
    
class AutoModerationStrategy(Enum):
    MAJ_SPAM = auto()
    

class AutoModerationCheckerFactory:
    STRATEGIES : Final[dict[AutoModerationStrategy, AutoModerationCheckerStrategy]] = {
        AutoModerationStrategy.MAJ_SPAM : MajSpamCheckerStrategy()
    }
    
    @classmethod
    def create(cls, strategy : AutoModerationStrategy) -> AutoModerationCheckerStrategy:
        if not strategy in cls.STRATEGIES:
            raise ValueError("Invalid Strategy")
        
        return cls.STRATEGIES[strategy]



class AutoModerationCog(commands.Cog):
    def __init__(self, BOT : commands.Bot) -> None:
        self.BOT = BOT
        
        
    def create_all_strategies(self) -> list[AutoModerationCheckerStrategy]:
        return [AutoModerationCheckerFactory.create(strategy) for strategy in AutoModerationStrategy]
    
    
        
    @commands.Cog.listener(name="on_message")
    async def check_for_auto_moderation(self, message : discord.Message) -> None:
        if message.author.BOT:
            return
        
        checkers = self.create_all_strategies()
        
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