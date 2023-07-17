import discord
from discord.ext import commands

from discord import app_commands

import aiosqlite
from dataclasses import dataclass


@dataclass
class Response:
    trigger : str 
    response : str


    
async def add_response(connection : aiosqlite.Connection, guild_id: int, trigger : str, response : str) -> None:
    await connection.execute('INSERT INTO responses VALUES (?, ?, ?)', (guild_id, trigger, response))
    
    await connection.commit()
    
    
async def get_responses(connection : aiosqlite.Connection, guild_id : int) -> list[Response]:
    responses = await connection.execute_fetchall(
        'SELECT trigger, response FROM responses WHERE guild_id = ?',
        (guild_id,)
    )
    
    return [Response(trigger, response) for trigger, response in responses]



class AutoResponseCog(commands.Cog):
    def __init__(self, bot : commands.Bot, connection : aiosqlite.Connection) -> None:
        self.bot = bot
        self.connection = connection
        
        
        
    def get_final_responses(self, message : discord.Message, responses : list[Response]) -> list[str]:
        variables = {
            'user' : message.author.mention,
            'user_name' : message.author.name   
        }
        
        final_responses : list[str] = []
        for response in responses:
            if response.trigger in message.content:
                for variable, value in variables.items():
                    response.response = response.response.replace(f'[{variable}]', value)
                    
                final_responses.append(response.response)
        
    
    @commands.Cog.listener("on_message")
    async def check_for_response(self, message : discord.Message) -> None:
        responses = await get_responses(self.connection, message.guild.id)
        final_responses = self.get_final_responses(message, responses)
        
        
        for response in final_responses:
            if response in message.content:
                await message.channel.send(response)
                
                
        print(final_responses)
        
    
    
    @app_commands.command(name="add_response")
    async def add_response(self, interaction : discord.Interaction, trigger : str, response : str) -> None:
        await add_response(self.connection, interaction.guild.id, trigger, response)
        
        embed = discord.Embed(
            title="Réponse ajoutée !",
            description=f"Le trigger `{trigger}` a été ajouté !",
            color=discord.Color.green()   
        )
        
        return await interaction.response.send_message(embed=embed)
    
    
    @app_commands.command(name="get_responses")
    async def get_responses(self, interaction : discord.Interaction) -> None:
        responses = await get_responses(self.connection, interaction.guild.id)
        
        embed = discord.Embed(
            title="Réponses",
            description="\n".join([f"**{response.trigger}** : {response.response}" for response in responses]),
            color=discord.Color.green()   
        )
        
        return await interaction.response.send_message(embed=embed) 
    