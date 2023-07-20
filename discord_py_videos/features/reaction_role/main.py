import os

import discord
import dotenv
from discord.ext import commands


class RoleButton(discord.ui.Button['ReactionRoleView']):
    def __init__(self, role : discord.Role) -> None:
        super().__init__(
            label=role.name,
            custom_id=f'button_{role.name}',
            style=discord.ButtonStyle.blurple
        )
        
        self.role = role
        
    async def callback(self, interaction : discord.Interaction) -> None:
        author = interaction.user 
        
        if isinstance(author, discord.User):
            return 
        
        if self.role in author.roles:
            await author.remove_roles(self.role)
            
            return await interaction.response.send_message(
                f"Vous avez perdu le rôle {self.role.name} !",
                ephemeral=True
            )
        
        await author.add_roles(self.role)
            
        return await interaction.response.send_message(
            f"Vous avez obtenu le rôle {self.role.name} !",
            ephemeral=True
        )
            
            
    async def on_error(self, interaction : discord.Interaction) -> None:
        return await interaction.response.send_message(
            "Vous ne pouvez pas obtenir ce rôle !",
            ephemeral=True
        )
    



class ReactionRoleSelectMenu(discord.ui.RoleSelect["ReactionRoleView"]):
    def __init__(self) -> None:
        super().__init__(placeholder='Choisissez les rôles !', max_values=25)

    
    async def callback(self, interaction : discord.Interaction) -> None:
        new_view = ReactionRoleView()
        for role in self.values:
            new_view.add_item(RoleButton(role))
            
            
        embed = discord.Embed(
                title="Veuillez choisir vos rôles !",
                description="Cliquez sur les boutons pour obtenir les rôles !",
                color=discord.Color.random()
            )
        
        embed.set_thumbnail(url=interaction.guild.icon.url)
        
        await interaction.response.edit_message(
            embed=embed,
            view=new_view
        )
        
        if self.view is not None:
            self.view.stop()
        

class ReactionRoleView(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)
        
  
        
class ReactionRoleCog(commands.Cog):
    def __init__(self, bot : commands.Bot) -> None:
        self.bot = bot
        

    @commands.hybrid_command(name="reaction_role")
    async def reaction_role(self, ctx : commands.Context[commands.Bot]) -> discord.Message:
        if ctx.guild is None:
            raise commands.NoPrivateMessage()
        
        view = ReactionRoleView().add_item(ReactionRoleSelectMenu())
        
        
        embed = discord.Embed(
            title="Veuillez choisir les rôles à ajouter !",
            description="Cliquez sur les boutons pour selectionner un rôle !",
            color=discord.Color.random()
        )
        
        embed.set_author(icon_url=self.bot.user.display_avatar.url, name=self.bot.user.name)
        embed.set_thumbnail(url=ctx.guild.icon.url)
        
        return await ctx.send(embed=embed, view=view)


class Bot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix='!', intents=discord.Intents.all())


    async def setup_hook(self) -> None:
        await self.add_cog(ReactionRoleCog(self))
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