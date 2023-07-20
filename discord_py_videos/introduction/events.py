import discord  
from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


@bot.event 
async def on_ready() -> None:
    print("Le bot est en ligne") 
    
    
@bot.event
async def on_message(message : discord.Message) -> None:
    if message.author.bot:
        return
    
    if "bonjour" in message.content.lower():
        await message.channel.send("Bonjour !")


bot.run('token')