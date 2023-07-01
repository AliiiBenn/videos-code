from typing import Optional
import discord
from discord.ext import commands

import os, dotenv


class NotInVoiceChannel(commands.CommandError):
    def __init__(self, message : Optional[str] = None) -> None:
        self.message = message
        super().__init__(message)


class MoveMeCog(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot


    @commands.hybrid_command(name="moveme")
    @commands.guild_only()
    async def move_me_command(self,
                              ctx : commands.Context,
                              channel : Optional[discord.VoiceChannel] = None
                              ) -> discord.Message:
        
        member = ctx.author 
        
        if not member.voice:
            raise NotInVoiceChannel(message="Vous n'êtes pas dans un salon vocal.") 
        
        
        # Si channel est None on quitte le salon actuel
        await member.move_to(channel=channel, reason=f"Commande moveme appelée par {member.name}.")
        
        return await ctx.send(f"{member.name} déplacé")
        
    @move_me_command.error
    async def move_me_error_command(self, ctx : commands.Context, error : commands.CommandError) -> discord.Message:
        if isinstance(error, NotInVoiceChannel):
            error_message = error.message
            if error_message is None:
                error_message = ":x: Une erreur est survenue."
            
            return await ctx.send(
                embed=discord.Embed(title=error_message, color=discord.Color.red())
            )
        
        raise error


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
        command_prefix='!',
        intents=discord.Intents.all()
        )

    async def setup_hook(self) -> None:
        await self.add_cog(MoveMeCog(self))
        await self.tree.sync()

    async def on_ready(self):
        print('-------------')
        print(f'Logged in as {self.user}')
        print(f'Bot is ready.')

bot = MyBot()

if __name__ == '__main__':
    dotenv.load_dotenv()
    token = os.getenv('token')

    if token is None:
        raise ValueError('Token not found')

    bot.run(token)