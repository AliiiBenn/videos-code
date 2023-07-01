import os

import discord
import dotenv
from discord.ext import commands

import openai

class ImageVariation(commands.Cog):
    def __init__(self, bot : commands.Bot) -> None:
        self.bot = bot
        
        
    @commands.hybrid_command(name="avatar_variation")
    async def avatar_variation(self, ctx : commands.Context, member : discord.Member) -> discord.Message:
        response = openai.Image.create_variation(
            image=member.display_avatar.url,
            n=1,
            size="256x256"
        )
        
        return await ctx.send(response["data"][0]["url"])


class Bot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix='!', intents=discord.Intents.all())


    async def setup_hook(self) -> None:
        await self.add_cog(ImageVariation(self))
        await self.tree.sync()

    async def on_ready(self) -> None:
        print('Je suis en ligne !')



def main() -> None:
    dotenv.load_dotenv()
    bot = Bot()

    TOKEN = os.getenv('TOKEN')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

    if TOKEN is None:
        raise ValueError('Le token n\'est pas défini !')
    
    if OPENAI_API_KEY is None:
        raise ValueError('Le token OpenAI n\'est pas défini !')
    
    openai.api_key = OPENAI_API_KEY

    bot.run(TOKEN)


if __name__ == '__main__':
    main()