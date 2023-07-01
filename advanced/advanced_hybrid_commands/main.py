import os

import discord
import dotenv
from discord.ext import commands
from discord import app_commands



class CommandFlags(commands.FlagConverter):
    member : discord.Member
    count : int 
    
    
class ExampleCog(commands.Cog):
    def __init__(self, bot : commands.Bot) -> None:
        self.bot = bot
        
        
    @commands.hybrid_command(name="example")
    @app_commands.describe(
        member = "La personne à mentionner",
        count = "Le nombre à mettre"
    )
    async def example(self,
                      ctx : commands.Context[commands.Bot],
                      *,
                      argument : CommandFlags) -> discord.Message:
        
        return await ctx.send(
            f"Vous avez mentionné {argument.member.mention} et vous avez mis {argument.count} !"
        )




class Bot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix='!', intents=discord.Intents.all())


    async def setup_hook(self) -> None:
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