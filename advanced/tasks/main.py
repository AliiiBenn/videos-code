import os

import discord
import dotenv
from discord.ext import commands
from discord.ext import tasks       # Module des tâches

import datetime

times = [
    datetime.time(hour=12, minute=30, second=0),        # 12h30 tous les jours
    datetime.time(hour=18, minute=30, second=0),        # 18h30 tous les jours 
    datetime.time(hour=20, minute=45, second=0),        # 20h45 tous les jours 
]


class TaskCog(commands.Cog):
    def __init__(self, bot : commands.Bot) -> None:
        self.bot = bot 
        self.loop.start()           # Commence la première tâche 
        self.loop2.start()          # Comment la seconde tâche
        
    
    @tasks.loop(seconds=3, minutes=0, hours=0, count=3)    # Appelée toutes les 3 secondes pour 3 fois
    async def loop(self) -> None:
        print('Loop !')
        
        
    @loop.before_loop
    async def before_loop(self) -> None:
        print('Before loop !')
        await self.bot.wait_until_ready()       # Attendre la fin de on_ready
        
        
    @tasks.loop(time=times)
    async def loop2(self) -> None:
        print('Loop 2 !')
        
    
    


class Bot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix='!', intents=discord.Intents.all())


    async def setup_hook(self) -> None:
        await self.add_cog(TaskCog(self))
        await self.tree.sync()

    async def on_ready(self) -> None:
        print('Je suis en ligne !')



def main() -> None:
    dotenv.load_dotenv()
    bot = Bot()

    TOKEN = os.getenv('TOKEN')

    if TOKEN is None:
        raise ValueError('Le token n\'est pas défini !')

    bot.run(TOKEN)


if __name__ == '__main__':
    main()