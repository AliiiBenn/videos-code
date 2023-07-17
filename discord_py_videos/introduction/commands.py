import discord  
from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


@bot.command()
async def hello(ctx : commands.Context) -> discord.Message:
    return await ctx.send("Hello, World!")


@bot.command()
async def compter(ctx : commands.Context, n : int) -> None:
    for i in range(n):
        await ctx.send(str(i))
        
        
@bot.command()
async def echo(ctx : commands.Context, n : int, *, message : str) -> discord.Message:
    for _ in range(n):
        await ctx.send(message)


bot.run('token')