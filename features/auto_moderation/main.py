import os

import discord
import dotenv
from discord.ext import commands

from abc import ABC, abstractmethod



class AutoModerationStrategy(ABC):
    @abstractmethod
    def check(self, message : discord.Message) -> bool:
        pass 



class MajusculeStrategy(AutoModerationStrategy):
    def get_content(self, message : discord.Message) -> str:
        return message.content
    
    def get_maj_count(self, content : str) -> int:
        return len([character for character in content if character.isupper()])
    
    def get_percentage(self, maj_count : int, content : str) -> float:
        return maj_count / len(content)
    
    def check_percentage(self, percentage : float) -> bool:
        LIMIT = 0.25
        return percentage > LIMIT
    
    
    def check(self, message : discord.Message) -> bool:
        message_content = self.get_content(message)
        message_maj_count = self.get_maj_count(message_content)
        maj_percentage = self.get_percentage(message_maj_count, message_content)
        
        return self.check_percentage(maj_percentage)
        



class DiscordLinkStrategy(AutoModerationStrategy):
    def check(self, message : discord.Message) -> bool:
        return "discord.gg" in message.content or "discordapp.com/invite" in message.content




class Bot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix='!', intents=discord.Intents.all())


    async def setup_hook(self) -> None:
        await self.tree.sync()

    async def on_ready(self) -> None:
        print('Je suis en ligne !')
        
        
    async def on_message(self, message : discord.Message) -> None:
        strategies = [MajusculeStrategy(), DiscordLinkStrategy()]
        
        if message.author.bot or message.guild is None :
            return
        
        for strategy in strategies:
            if strategy.check(message):
                await message.delete()
                await message.channel.send(f"{message.author.name} merci de respecter les règles du serveur !")
                return
            
            
        await self.process_commands(message)



def main() -> None:
    dotenv.load_dotenv()
    bot = Bot()

    TOKEN = os.getenv('TOKEN')

    if TOKEN is None:
        raise ValueError('Le token n\'est pas défini !')

    bot.run(TOKEN)


if __name__ == '__main__':
    main()