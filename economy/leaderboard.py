import discord 
from discord.ext import commands

import aiosqlite

from database import get_most_money_members



class LeaderboardCog(commands.Cog):
    def __init__(self, bot : commands.Bot, connection : aiosqlite.Connection) -> None:
        self.bot = bot
        self.connection = connection
        
        
    @commands.hybrid_command(name="leaderboard")
    async def leaderboard(self, ctx : commands.Context[commands.Bot]) -> discord.Message:
        members = await get_most_money_members(self.connection, ctx.guild.id)
        
        embed = discord.Embed(
            title="Classement",
            description="Voici le classement des membres les plus riches du serveur !",
            color=discord.Color.green()
        )
        
        embed.set_thumbnail(url=ctx.guild.icon.url)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)
        
        for i, member in enumerate(members):
            embed.add_field(name=f"{i + 1}. {member['name']}",
                            value=f"{member['money']} money",
                            inline=False
                )
        
        
        await ctx.send(embed=embed)
        
        
        
async def setup(bot : commands.Bot) -> None:
    connection = await aiosqlite.connect("economy.db")
    
    await bot.add_cog(LeaderboardCog(bot, connection)) 