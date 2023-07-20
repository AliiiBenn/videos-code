import discord 
from discord.ext import commands

import aiosqlite

from database import add_pocket_money, remove_pocket_money, add_bank_money, \
    remove_bank_money, has_bank_money, has_pocket_money



async def withdraw_money(connection : aiosqlite.Connection,
                         member : discord.Member,
                         money : int) -> None:
    
    if not await has_bank_money(connection, member, money):
        raise commands.BadArgument("Vous n'avez pas assez d'argent en banque !")
    
    await remove_bank_money(connection, member, money)
    await add_pocket_money(connection, member, money)


async def deposit_money(connection : aiosqlite.Connection,
                        member : discord.Member,
                        money : int) -> None:
    
    if not await has_pocket_money(connection, member, money):
        raise commands.BadArgument("Vous n'avez pas assez d'argent dans votre porte-monnaie !")
    
    await remove_pocket_money(connection, member, money)
    await add_bank_money(connection, member, money)
    
    

class WithdrawDepositCog(commands.Cog):
    def __init__(self, bot : commands.Bot, connection : aiosqlite.Connection) -> None:
        self.bot = bot
        self.connection = connection
        
        
    @commands.hybrid_command(name="withdraw")
    async def withdraw(self, ctx : commands.Context[commands.Bot], money : int) -> discord.Message:
        await withdraw_money(self.connection, ctx.author, money)
    
        embed = discord.Embed(
            title="Retrait",
            description=f"Vous avez retiré {money} de votre banque !",
            color=discord.Color.green()
        )
        
        bot_user = self.bot.user
        embed.set_author(name=bot_user.display_name, icon_url=bot_user.display_avatar.url)
        embed.set_footer(text=f"Commande effectuée par {ctx.author.display_name}", 
                         icon_url=ctx.author.display_avatar.url)
        
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        
        

        return await ctx.send(embed=embed)


    @withdraw.error
    async def withdraw_error(self, ctx : commands.Context[commands.Bot], error : commands.CommandError) -> None:
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                title=":x: Vous n'avez pas assez d'argent en banque !",
                color=discord.Color.red(),
            )
            
            await ctx.send(embed=embed)
            
        else:
            raise error
    
    
    @commands.hybrid_command(name="deposit")
    async def deposit(self, ctx : commands.Context[commands.Bot], money : int) -> discord.Message:
        await deposit_money(self.connection, ctx.author, money)
        
        embed = discord.Embed(
            title="Dépôt",
            description=f"Vous avez déposé {money} dans votre banque !",
            color=discord.Color.green()
        )
        
        bot_user = self.bot.user
        embed.set_author(name=bot_user.display_name, icon_url=bot_user.display_avatar.url)
        embed.set_footer(text=f"Commande effectuée par {ctx.author.display_name}",
                         icon_url=ctx.author.display_avatar.url)
        
        embed.set_thumbnail(url=ctx.author.display_avatar.url)

        return await ctx.send(embed=embed)


    @deposit.error
    async def deposit_error(self, ctx : commands.Context[commands.Bot], error : commands.CommandError) -> None:
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                title=":x: Vous n'avez pas assez d'argent en banque !",
                color=discord.Color.red(),
            )
            
            await ctx.send(embed=embed)
            
        else:
            raise error
    
    
    
async def setup(bot : commands.Bot) -> None:
    connection = await aiosqlite.connect("economy.db")
    await bot.add_cog(WithdrawDepositCog(bot, connection))
