import discord 
from discord.ext import commands

import aiosqlite
import random


from database import add_pocket_money, remove_pocket_money, get_pocket_money




class BegCog(commands.Cog):
    def __init__(self, bot : commands.Bot, connection : aiosqlite.Connection) -> None:
        self.bot = bot
        self.connection = connection
        
        
    @commands.hybrid_command(name="beg")
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def beg_money(self, ctx : commands.Context[commands.Bot]) -> discord.Message:
        if ctx.guild is None:
            raise commands.NoPrivateMessage()
        
        
        QUANTITY = random.randint(1, 15)
        
        await add_pocket_money(self.connection, ctx.author, QUANTITY)
        
        embed = discord.Embed(
            title="Beg",
            description=f"Vous avez reçu {QUANTITY} pièces !",
            color=discord.Color.blurple()
        )
        
        bot_user = self.bot.user
        embed.set_author(name=bot_user.display_name, icon_url=bot_user.display_avatar.url)
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        
        return await ctx.send(embed=embed)
        
        
    @beg_money.error
    async def beg_money_error(self, ctx : commands.Context[commands.Bot], error : commands.CommandError) -> None:
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send(
                embed = discord.Embed(
                    title=":x: Cette commande ne peut pas être utilisée en DMs !",
                    color = discord.Color.red()
                    )
                )
            
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                embed = discord.Embed(
                    title=f":x: Cette commande est en cooldown ! Réessayez dans {error.retry_after:.2f}s",
                    color = discord.Color.red()
                    )
                )
            
        else:
            raise error
        

class RobCog(commands.Cog):
    def __init__(self, bot : commands.Bot, connection : aiosqlite.Connection) -> None:
        self.bot = bot
        self.connection = connection
        
    
    async def create_failed_embed(self, member : discord.Member, amount : int) -> discord.Embed:
        embed = discord.Embed(
            title=f"Vous avez échoué à voler {member.name} !",
            description=f"Vous avez perdu {amount} pièces !",
            color=discord.Color.red()
        )
        
        return embed
    
    async def create_success_embed(self, member : discord.Member, amount : int) -> discord.Embed:
        embed = discord.Embed(
            title=f"Vous avez volé {member.name} !",
            description=f"Vous avez reçu {amount} pièces !",
            color=discord.Color.green()
        )
        
        return embed
    
    
    async def set_failed_money(self, author : discord.Member, member : discord.Member) -> int:
        MAX_AMOUNT = await get_pocket_money(self.connection, member)

        if MAX_AMOUNT == 0:
            return 0

        AMOUNT_TO_REMOVE = random.randint(1, MAX_AMOUNT)
        
        await remove_pocket_money(self.connection, author, AMOUNT_TO_REMOVE)
        await add_pocket_money(self.connection, member, AMOUNT_TO_REMOVE)
        
        return AMOUNT_TO_REMOVE
        
        
    async def set_success_money(self, author : discord.Member, member : discord.Member) -> int:
        MAX_AMOUNT = await get_pocket_money(self.connection, member)

        if MAX_AMOUNT == 0:
            return 0

        AMOUNT_TO_ADD = random.randint(1, MAX_AMOUNT)
        
        await add_pocket_money(self.connection, author, AMOUNT_TO_ADD)
        await remove_pocket_money(self.connection, member, AMOUNT_TO_ADD)
        
        return AMOUNT_TO_ADD
    
    
    @commands.hybrid_command(name="rob")
    @commands.cooldown(1, 21600, commands.BucketType.user)
    async def rob_member_money(self, ctx : commands.Context[commands.Bot], member : discord.Member) -> discord.Message:
        if ctx.guild is None:
            raise commands.NoPrivateMessage()
        
        FAILED = random.choice([True, False])
        
        if FAILED:
            amount = await self.set_failed_money(ctx.author, member)
            embed = await self.create_failed_embed(member, amount)
        else:
            amount = await self.set_success_money(ctx.author, member)
            embed = await self.create_success_embed(member, amount)
            
        bot_user = self.bot.user
        embed.set_author(name=bot_user.display_name, icon_url=bot_user.display_avatar.url)
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        
        return await ctx.send(embed=embed)            
        
        
    @rob_member_money.error
    async def rob_member_money_error(self, ctx : commands.Context[commands.Bot], error : commands.CommandError) -> None:
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send(
                embed = discord.Embed(
                    title=":x: Cette commande ne peut pas être utilisée en DMs !",
                    color = discord.Color.red()
                    )
                )
            
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                embed = discord.Embed(
                    title=f":x: Cette commande est en cooldown ! Réessayez dans {error.retry_after:.2f}s",
                    color = discord.Color.red()
                    )
                )
            
        elif isinstance(error, commands.BadArgument):
            await ctx.send(
                embed = discord.Embed(
                    title="Membre invalide !",
                    color = discord.Color.red()
                    )
                )
            
        else:
            raise error
        
        
async def setup(bot : commands.Bot) -> None:
    connection = await aiosqlite.connect("economy.db")
    await bot.add_cog(BegCog(bot, connection))
    await bot.add_cog(RobCog(bot, connection))