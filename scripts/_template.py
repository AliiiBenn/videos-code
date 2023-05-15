import discord 
from discord.ext import commands

import dotenv, os



bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')
    print('------')



if __name__ == '__main__':
    dotenv.load_dotenv()
    TOKEN = os.getenv('TOKEN')
    
    if TOKEN is None:
        raise ValueError('Token not found')
    
    bot.run(TOKEN)