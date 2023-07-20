import os

import discord
import dotenv
from discord.ext import commands
from discord.ext import tasks       # Module des tâches - 1

import datetime # - 13

times = [ # - 14
    datetime.time(hour=12, minute=30, second=0),        # 12h30 tous les jours - 15
    datetime.time(hour=18, minute=30, second=0),        # 18h30 tous les jours - 16  
    datetime.time(hour=20, minute=45, second=0),        # 20h45 tous les jours - 17  
]


class TaskCog(commands.Cog): # - 2
    def __init__(self, bot : commands.Bot) -> None:  # - 3
        self.bot = bot # - 4
        self.loop.start()           # Commence la première tâche - 7 - lancer le code
        self.loop2.start()          # Comment la seconde tâche - 21 - lancer le code
        
    
    @tasks.loop(seconds=3, minutes=0, hours=0, count=3)    # Appelée toutes les 3 secondes pour 3 fois - 4
    async def loop(self) -> None: # - 5
        print('Loop !') # - 6
        
        
    @loop.before_loop # - 9
    async def before_loop(self) -> None: # - 10
        print('Before loop !') # - 11
        await self.bot.wait_until_ready()       # Attendre la fin de on_ready - 12 - lancer le code 
        
        
    @tasks.loop(time=times) # - 18
    async def loop2(self) -> None: # - 19
        print('Loop 2 !') # - 20
        
    
    


class Bot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix='!', intents=discord.Intents.all())


    async def setup_hook(self) -> None:
        await self.add_cog(TaskCog(self)) # - 8
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