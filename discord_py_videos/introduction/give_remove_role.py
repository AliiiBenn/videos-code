import os

import discord
import dotenv
from discord.ext import commands



class RoleCog(commands.Cog):
    def __init__(self, bot : commands.Bot) -> None:
        self.bot = bot
        
        
    @commands.hybrid_command(name='give_role')
    @commands.has_permissions(manage_roles=True)
    @commands.guild_only()
    async def give_role_command(self, 
                        ctx : commands.Context,
                        role : discord.Role, 
                        member : discord.Member) -> discord.Message:
        
        
        await member.add_roles(role)
        
        return await ctx.send(
            f'Gave {role.name} to {member.name}#{member.discriminator}'
        )
        
        
    @commands.hybrid_command(name='remove_role')
    @commands.has_permissions(manage_roles=True)
    @commands.guild_only()
    async def remove_role_command(self, 
                        ctx : commands.Context,
                        role : discord.Role, 
                        member : discord.Member) -> discord.Message:
        
        
        await member.remove_roles(role)
        
        return await ctx.send(
            f'Removed {role.name} to {member.name}#{member.discriminator}'
        )
        


class Bot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix='!', intents=discord.Intents.all())


    async def setup_hook(self) -> None:
        await self.tree.sync()

    async def on_ready(self) -> None:
        print('Je suis en ligne !')



def main() -> None:
    dotenv.load_dotenv()
    bot = Bot()

    TOKEN = os.getenv('TOKEN')

    if TOKEN is None:
        raise ValueError('Le token n\'est pas défini !')

    bot.run(TOKEN)


if __name__ == '__main__':
    main()