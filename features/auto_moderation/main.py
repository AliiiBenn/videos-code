import os

import discord
import dotenv
from discord.ext import commands

import strategies




class Bot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix='!', intents=discord.Intents.all())


    async def setup_hook(self) -> None:
        await self.tree.sync()

    async def on_ready(self) -> None:
        print('Je suis en ligne !')
        
        
    async def on_message(self, message : discord.Message) -> None:
        moderation_strategies = [strategies.MajusculeStrategy(), strategies.DiscordLinkStrategy()]
        
        if message.author.bot or message.guild is None :
            return
        
        for strategy in moderation_strategies:
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