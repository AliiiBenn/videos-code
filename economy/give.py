import discord 
from discord.ext import commands

import aiosqlite

from database import has_bank_money, add_bank_money, remove_bank_money, account_exists


class GiveCog(commands.Cog):
    def __init__(self, bot : commands.Bot, connection : aiosqlite.Connection) -> None:
        self.bot = bot
        self.connection = connection
        
        
        
    @commands.hybrid_command(name="give")
    async def give_money(self, 
                         ctx : commands.Context[commands.Bot], 
                         member : discord.Member, 
                         quantity : int) -> discord.Message:
        
        if ctx.guild is None:
            raise commands.NoPrivateMessage()
        
        if not await account_exists(self.connection, member) or member.bot:
            embed = discord.Embed(
                title=f"**{member.name}** n'a pas de compte !",
                color=discord.Color.red()
            )
        
        elif not await has_bank_money(self.connection, ctx.author, quantity):
            embed = discord.Embed(
                title="Vous n'avez pas assez d'argent !",
                color=discord.Color.red()
            )
            
        else:   
            await remove_bank_money(self.connection, ctx.author, quantity)
            await add_bank_money(self.connection, member, quantity)
            
            embed = discord.Embed(
                title=f"**{ctx.author.name}** a donné {quantity} money à **{member.name}** !",
                color=discord.Color.green()
            )
            
        return await ctx.send(embed=embed)
    
    
async def setup(bot : commands.Bot) -> None:
    connection = await aiosqlite.connect("economy.db")
    
    await bot.add_cog(GiveCog(bot, connection))