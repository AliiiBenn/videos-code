import discord 
from discord.ext import commands


import json


class AddPrefixOnJoinCog(commands.Cog):
    def __init__(self, BOT : commands.Bot) -> None:
        self.BOT = BOT
        
        
    @commands.Cog.listener("on_guild_join")
    async def add_prefix_on_guild_join(self, guild : discord.Guild) -> None:
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
            
        guild_id = str(guild.id)
        prefixes[guild_id] = ['!']
        
        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)
            
        
    @commands.Cog.listener("on_guild_remove")
    async def remove_prefix_on_guild_remove(self, guild : discord.Guild) -> None:
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
            
        guild_id = str(guild.id)
        prefixes.pop(guild_id)
        
        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)
            
            
            
            
async def setup(BOT : commands.Bot) -> None:
    await BOT.add_cog(AddPrefixOnJoinCog(BOT))
    