import discord 
from discord.ext import commands 

import aiosqlite


from database import create_table, create_account, delete_account, account_exists
    
    

class TableSetupCog(commands.Cog):
    def __init__(self, bot : commands.Bot, connection : aiosqlite.Connection) -> None:
        self.bot = bot
        self.connection = connection
        
        
    @commands.Cog.listener("on_member_join")
    async def create_account_for_new_members(self, member : discord.Member) -> None:
        await create_account(self.connection, member)
        print(f"Account created for {member.display_name} !")
    
    
    @commands.Cog.listener("on_member_remove")
    async def delete_account_for_left_members(self, member : discord.Member) -> None:
        await delete_account(self.connection, member)
        print(f"Account deleted for {member.display_name} !")
        
        
    @commands.hybrid_command(name="create_all_missing_accounts")
    async def create_all_missing_accounts(self, ctx : commands.Context) -> None:
        if ctx.guild is None:
            raise commands.NoPrivateMessage("This command can't be used in DMs !")
        
        for member in ctx.guild.members:
            if not await account_exists(self.connection, member) and not member.bot:
                await create_account(self.connection, member)
                
        await ctx.send("All missing accounts have been created !")
        
    
        
        
        
        
async def setup(bot : commands.Bot) -> None:
    connection = await aiosqlite.connect('economy.db')
    
    await create_table(connection)
    await bot.add_cog(TableSetupCog(bot, connection))