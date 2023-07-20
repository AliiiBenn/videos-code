import os

import discord
import dotenv
from discord.ext import commands


def premier_check(ctx : commands.Context) -> bool:
    return False


def second_check() -> commands.check:
    def predicate(ctx : commands.Context) -> bool:
        return False
    return commands.check(predicate)
    

def check_exemple() -> bool:
    def predicate(ctx : commands.Context) -> bool:
        return False 
    return commands.check(predicate)



class ChecksCog(commands.Cog):
    def __init__(self, bot : commands.Bot) -> None:
        self.bot = bot
        
        
    @commands.command(name="ping")
    @commands.check_any(is_owner(), example_check())
    @commands.check(premier_check)
    @second_check()
    async def ping_command(self, ctx : commands.Context) -> discord.Message:
        return await ctx.send('Pong !')


class Bot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix='!', intents=discord.Intents.all())


    async def setup_hook(self) -> None:
        await self.add_cog(ChecksCog(self))
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