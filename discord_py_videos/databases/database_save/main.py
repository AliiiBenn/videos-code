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


    
class UserCog(commands.Cog):
    def __init__(self, bot : commands.Bot, connection : aiosqlite.Connection) -> None:
        self.bot = bot
        self.connection = connection
        
        
    @commands.command(name="add_user")
    async def add_user_command(self, ctx : commands.Context, user_id : int, username : str) -> discord.Message:
        await self.connection.execute("""
        INSERT INTO users (id, username) VALUES (?, ?)           
        """, (user_id, username)
        )   
    
        await self.connection.commit()    
        
         
        return await ctx.send(f"User {user_id} ajouté !")
        
    
    @commands.command(name="update_user")
    async def update_user_command(self, ctx : commands.Context, user_id : int, username : str) -> discord.Message:
        await self.connection.execute("""
        UPDATE users SET username = ? WHERE id = ?           
        """, (username, user_id)
        )   
    
        await self.connection.commit()
        
        return await ctx.send(f"User {user_id} mis à jour !")
        
        
    @commands.command(name="get_user")
    async def get_user_command(self, ctx : commands.Context, user_id : int) -> discord.Message:
        cursor = await self.connection.execute("""
        SELECT * FROM users WHERE id = ?         
        """, (user_id,)
        )
    
        user = await cursor.fetchone()

        if user is None:
            return await ctx.send(f"User {user_id} introuvable !")


        final_user = User(*user)
        
        return await ctx.send(f"User {final_user.id} trouvé !")    
    

    @commands.command(name="get_users")
    async def get_users_command(self, ctx : commands.Context) -> discord.Message:
        users = await self.connection.execute_fetchall("""SELECT * FROM users""")
    
        final_users = [User(*user) for user in users]
        
        return await ctx.send(f"Users : {', '.join(user.username for user in final_users)}")
        
    
    @commands.command(name="delete_user")
    async def delete_user_command(self, ctx : commands.Context, user_id : int) -> None:
        await self.connection.execute("""
        DELETE FROM users WHERE id = ?         
        """, (user_id,))
    
        await self.connection.commit()
    
        
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