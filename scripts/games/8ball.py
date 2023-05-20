import discord 
from discord.ext import commands

import os, dotenv
from typing import Final


import random # needed for random.choice() function to choise a random response

BOT : Final[commands.Bot] = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@BOT.event
async def on_ready():
    print(f'Logged in as {BOT.user.name} - {BOT.user.id}')
    print('------')


@BOT.command(name='8ball')
async def eight_ball_game(ctx : commands.Context, *, question : str) -> discord.Message:
    possible_responses = [
        'That is a resounding no',
        'It is not looking likely',
        'Too hard to tell',
        'It is quite possible',
        'Definitely',
    ]
    
    choice = random.choice(possible_responses)
    final_message = f'Question: {question}\nAnswer: {choice}'
    
    return await ctx.send(final_message)



if __name__ == '__main__':
    dotenv.load_dotenv()
    TOKEN = os.getenv('TOKEN')
    
    if TOKEN is None:
        raise ValueError('Token not found')
    
    BOT.run(TOKEN)