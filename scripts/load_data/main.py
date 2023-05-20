import discord
from discord.ext import commands

import os, dotenv
from typing import Final, json



class MessagesLoaderSystem(commands.Cog):
    def __init__(self, BOT : commands.Bot) -> None:
        self.BOT = BOT
        
        
    @commands.Cog.listener("on_message")
    async def load_message(self, message : discord.Message) -> None:
        if message.author.BOT or not message.guild:
            return
        
        guild_id = str(message.guild.id)
        
        with open('data.json', 'r') as f:
            messages = json.load(f)
            
        if guild_id not in messages:
            messages[guild_id] = []
        
        messages[guild_id].append(f"{discord.utils.utcnow()} | {message.content} | {message.author}")

        with open('data.json', 'w') as f:
            json.dump(messages, f, indent=4)
            
            
    @commands.hybrid_command(name="get_messages")
    async def get_messages(self, ctx : commands.Context, limit : int = 10) -> None:
        guild_id = str(ctx.guild.id)
        
        with open('data.json', 'r') as f:
            messages = json.load(f)
            
        if guild_id not in messages:
            messages[guild_id] = []
            
        messages = messages[guild_id]
        
        await ctx.send("\n".join(messages[-limit:]))
        

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
        command_prefix='!',
        intents=discord.Intents.all()
        )

    async def setup_hook(self) -> None:
        await self.add_cog(MessagesLoaderSystem(self))
        
        await self.tree.sync()

    async def on_ready(self):
        print('-------------')
        print(f'Logged in as {self.user}')
        print(f'Bot is ready.')

BOT = MyBot()

if __name__ == '__main__':
    dotenv.load_dotenv()
    token = os.getenv('token')

    if token is None:
        raise ValueError('Token not found')

    BOT.run(token)