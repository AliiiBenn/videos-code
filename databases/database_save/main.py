import discord
from discord.ext import commands

import os, dotenv


import aiosqlite
from dataclasses import dataclass 


@dataclass
class User:
    id : int
    username : str


async def create_table(connection : aiosqlite.Connection) -> None:
    await connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY, username TEXT   
        )                 
    """)
    
    await connection.commit()


async def add_user(connection : aiosqlite.Connection, user_id : int, username : str) -> None:
    await connection.execute("""
        INSERT INTO users (id, username) VALUES (?, ?)           
    """, (user_id, username))   
    
    await connection.commit()                      
    


async def update_user(connection : aiosqlite.Connection, user_id : int, username : str) -> None:
    await connection.execute("""
        UPDATE users SET username = ? WHERE id = ?           
    """, (username, user_id))   
    
    await connection.commit()


async def get_user(connection : aiosqlite.Connection, user_id : int) -> User | None:
    cursor = await connection.execute("""
        SELECT * FROM users WHERE id = ?         
    """, (user_id,))
    
    user = await cursor.fetchone()
    
    if user is None:
        return None
    
    return User(*user)


async def get_users(connection : aiosqlite.Connection) -> list[User]:
    users = await connection.execute_fetchall("""SELECT * FROM users""")
    
    return [User(*user) for user in users]


async def delete_user(connection : aiosqlite.Connection, user_id : int) -> None:
    await connection.execute("""
        DELETE FROM users WHERE id = ?         
    """, (user_id,))
    
    await connection.commit()
    
    
    
class UserCog(commands.Cog):
    def __init__(self, bot : commands.Bot, connection : aiosqlite.Connection) -> None:
        self.bot = bot
        self.connection = connection
        
        
    @commands.command(name="add_user")
    async def add_user_command(self, ctx : commands.Context, user_id : int, username : str) -> None:
        await add_user(self.connection, user_id, username)
        await ctx.send(f"User {user_id} ajouté !")
        
    
    @commands.command(name="update_user")
    async def update_user_command(self, ctx : commands.Context, user_id : int, username : str) -> None:
        await update_user(self.connection, user_id, username)
        await ctx.send(f"User {user_id} mis à jour !")
        
        
    @commands.command(name="get_user")
    async def get_user_command(self, ctx : commands.Context, user_id : int) -> None:
        user = await get_user(self.connection, user_id)
        
        if user is None:
            await ctx.send(f"User {user_id} introuvable !")
            return
        
        await ctx.send(f"User {user.id} trouvé !")    
    

    @commands.command(name="get_users")
    async def get_users_command(self, ctx : commands.Context) -> None:
        users = await get_users(self.connection)
        
        await ctx.send(f"Users : {users}")
        
    
    @commands.command(name="delete_user")
    async def delete_user_command(self, ctx : commands.Context, user_id : int) -> None:
        await delete_user(self.connection, user_id)
        await ctx.send(f"User {user_id} supprimé !")



class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
        command_prefix="!",
        intents=discord.Intents.all()
        )

    async def setup_hook(self) -> None:
        await self.tree.sync()
        
        self.connection = await aiosqlite.connect('main.db')
        
        await create_table(self.connection)
        await self.add_cog(UserCog(self, self.connection))
        

    async def on_ready(self):
        print('-------------')
        print(f'Logged in as {self.user}')
        print('Bot is ready.')

bot = MyBot()

if __name__ == '__main__':
    dotenv.load_dotenv()
    token = os.getenv('token')

    if token is None:
        raise ValueError('Token not found')

    bot.run(token)