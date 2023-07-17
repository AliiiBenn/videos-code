import os

import discord
import dotenv
from discord.ext import commands

import aiosqlite


async def create_table(connection : aiosqlite.Connection) -> None:
    await connection.execute('CREATE TABLE IF NOT EXISTS prefixes (guild_id INTEGER, prefix TEXT)')
    
    await connection.commit()


async def add_prefix(connection : aiosqlite.Connection, guild_id: int, prefix: str) -> None:
    await connection.execute('INSERT INTO prefixes VALUES (?, ?)', (guild_id, prefix))
    
    await connection.commit()
    

async def remove_prefix(connection : aiosqlite.Connection, guild_id: int, prefix : str) -> None:
    await connection.execute('DELETE FROM prefixes WHERE guild_id = ? AND prefix = ?', (guild_id, prefix))
    
    await connection.commit()
    
    
async def get_prefixes(bot : commands.Bot, message : discord.Message) -> list[str]:
    connection = await aiosqlite.connect('prefix.db')
    
    prefixes = await connection.execute_fetchall('SELECT prefix FROM prefixes WHERE guild_id = ?', (message.guild.id,))
    
    if not prefixes:
        return ["!"]
    
    return [prefix[0] for prefix in prefixes]


class PrefixCog(commands.Cog):
    def __init__(self, bot : commands.Bot, connection : aiosqlite.Connection) -> None:
        self.bot = bot
        self.connection = connection
        
        
    @commands.command(name="add_prefix")
    async def add_prefix(self, ctx : commands.Context, *, prefix : str) -> discord.Message:
        if ctx.guild is None:
            raise commands.NoPrivateMessage()
        
        await add_prefix(self.connection, ctx.guild.id, prefix)
        
        return await ctx.send(f"Le préfixe `{prefix}` a été ajouté !")
    
    
    @commands.command(name="remove_prefix")
    async def remove_prefix(self, ctx : commands.Context, *, prefix : str) -> discord.Message:
        if ctx.guild is None:
            raise commands.NoPrivateMessage()
        
        await remove_prefix(self.connection, ctx.guild.id, prefix)
        
        return await ctx.send(f"Le préfixe `{prefix}` a été supprimé !")



class Bot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix=get_prefixes, intents=discord.Intents.all())


    async def setup_hook(self) -> None:
        self.connection = await aiosqlite.connect('prefix.db')
        await create_table(self.connection)
        
        await self.add_cog(PrefixCog(self, self.connection))
        
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