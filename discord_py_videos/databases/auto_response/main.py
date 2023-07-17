import os

import discord
import dotenv
from discord.ext import commands


import aiosqlite


import response


async def create_table(connection : aiosqlite.Connection) -> None:
    await connection.execute('CREATE TABLE IF NOT EXISTS responses (guild_id INTEGER, trigger TEXT, response TEXT)')
    
    await connection.commit()



class Bot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix='!', intents=discord.Intents.all())


    async def setup_hook(self) -> None:
        self.connection = await aiosqlite.connect('auto_response.db')
        await create_table(self.connection)
        
        await self.add_cog(response.AutoResponseCog(self, self.connection))
        
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