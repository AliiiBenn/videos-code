import os

import discord
import dotenv
from discord.ext import commands



class Bot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix='!', intents=discord.Intents.all())


    async def setup_hook(self) -> None:
        await self.load_extension("setup")
        await self.load_extension("get_account")
        await self.load_extension("beg")
        await self.load_extension("withdraw_deposit")
        await self.load_extension("leaderboard")
        await self.load_extension("give")
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