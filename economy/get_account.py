import discord 
from discord.ext import commands

import aiosqlite 

from database import get_bank_money, get_pocket_money


class MoneyGetterCog(commands.Cog):
    def __init__(self, bot : commands.Bot, connection : aiosqlite.Connection) -> None:
        self.bot = bot
        self.connection = connection
        
        
    async def create_embed(self, member : discord.Member) -> discord.Embed:
        embed = discord.Embed(
            title=f"Compte de {member.display_name}",
            description=f"Voici le compte de {member.mention}",
            color=discord.Color.blurple()
        )
        
        embed.add_field(
            name="Argent en banque",
            value=str(await get_bank_money(self.connection, member))
        )
        
        embed.add_field(
            name="Argent de poche",
            value=str(await get_pocket_money(self.connection, member))
        )
        
        bot_user = self.bot.user
        
        if bot_user is None:
            raise commands.UserNotFound("Bot user not found !")
        
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=f"ID: {member.id}")
        embed.set_author(
            name=bot_user.display_name, icon_url=bot_user.display_avatar.url
        )
        
        
        return embed
        
        
        
    @commands.hybrid_command(name="get_account")
    async def get_account(self,
                          ctx : commands.Context[commands.Bot],
                          member : discord.Member = commands.Author) -> discord.Message:
        
        if ctx.guild is None:
            raise commands.NoPrivateMessage("This command can't be used in DMs !")
        
        if member.bot:
            bot_embed = discord.Embed(
                    title=":x: Les Bots ne peuvent pas avoir de compte !", 
                    color=discord.Color.red()  
                )
            
            return await ctx.send(
                embed=bot_embed
            )
        
        embed = await self.create_embed(member)
        
        
        return await ctx.send(embed=embed)
    
    
async def setup(bot : commands.Bot) -> None:
    connection = await aiosqlite.connect("economy.db")
    await bot.add_cog(MoneyGetterCog(bot, connection))
        