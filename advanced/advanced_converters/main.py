import os

import discord
import dotenv
from discord.ext import commands



class ExampleConverter(commands.Converter):
    async def convert(self, ctx : commands.Context, argument : str) -> str:
        return f"Vous avez écrit {argument} !"


class ExampleCog(commands.Cog):
    def __init__(self, bot : commands.Bot) -> None:
        self.bot = bot
        
        
    @commands.hybrid_command(name="example")
    async def example(self, ctx : commands.Context, *, argument : ExampleConverter) -> discord.Message:
        await ctx.send(argument)
        
        
        

        
    


class Bot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix='!', intents=discord.Intents.all())


    async def setup_hook(self) -> None:
        await self.add_cog(ExampleCog(self))
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