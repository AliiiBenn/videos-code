import os

import discord
import dotenv
from discord.ext import commands
from discord.ext import tasks


def create_table(connection : aiosqlite.Connection) -> None:
    await connection.execute('CREATE TABLE IF NOT EXISTS messages (guild_id INTEGER, channel_id INTEGER, message TEXT)')



class RepetitiveMessagesCog(commands.Cog):
    def __init__(self, bot : commands.Bot) -> None:
        self.bot = bot
        
        self.send_message.start()
        
    
    @tasks.loop(seconds=5)
    async def send_message(self) -> None:
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                await channel.send('Je suis un message répétitif !')
    


class Bot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix='!', intents=discord.Intents.all())


    async def setup_hook(self) -> None:
        await self.add_cog(RepetitiveMessagesCog(self))
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