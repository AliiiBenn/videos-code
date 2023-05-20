import discord
from discord.ext import commands
from discord import app_commands

import os, dotenv
from typing import Final

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
        command_prefix='!',
        intents=discord.Intents.all()
        )

    async def setup_hook(self) -> None:
        await self.tree.sync()

    async def on_ready(self):
        print('-------------')
        print(f'Logged in as {self.user}')
        print(f'Bot is ready.')

BOT = MyBot()


@BOT.tree.command(name="test")
async def test_command(interaction : discord.Interaction, message : str):
    return await interaction.response.send_message(message, ephemeral=True)


@BOT.tree.context_menu()
async def react(interaction: discord.Interaction, message: discord.Message):
    await interaction.response.send_message('Very cool message!', ephemeral=True)

@BOT.tree.context_menu()
async def ban(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.send_message(f'Should I actually ban {user}...', ephemeral=True)


@app_commands.command(name="test_app_command")
async def test(interaction : discord.Interaction, message : str):
    return await interaction.response.send_message(message, ephemeral=True)


if __name__ == '__main__':
    dotenv.load_dotenv()
    token = os.getenv('token')

    if token is None:
        raise ValueError('Token not found')

    BOT.run(token)