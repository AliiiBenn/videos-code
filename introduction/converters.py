import discord  
from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


@bot.event
async def on_ready() -> None:
    print("Le bot est en ligne")
    
    
@bot.command()
async def add(ctx : commands.Context, a : float, b : float) -> discord.Message:
    return await ctx.send(str(a + b))


def to_upper(argument : str) -> str:
    return argument.upper()


@bot.command()
async def test(ctx : commands.Context, *, message : to_upper) -> discord.Message:
    return await ctx.send(message)

@bot.command()
async def hey(ctx : commands.Context, *, member : discord.Member) -> discord.Message:
    return await ctx.send(f"Hey {member.name} !")


bot.run('token')