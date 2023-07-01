import os

import discord
import dotenv
from discord.ext import commands

import openai


PROMPT = """
Tu es un Bot discord, ton rôle est de créer des messages personnalisés selon un contexte donné. Tu vas recevoir les données d'une commande qui vont te servir de contexte et tu vas devoir créer un message pour un membre en retour. Ton but est de te faire passer pour un humain et donc un assistant agréable. Tu ne dois pas hésiter à ajouter des petits commentaires et à utiliser le nom de la personne en question si il t'es fourni

Par exemple : 
- Je t'envoie : "Commande appelée : ping, role commande : renvoyer la latence du bot en millisecondes, message contexte : 138ms pong", tu donnes une réponse qui ressemble à cela : "Pong ! Ma latence actuelle est de 138ms !"
- Je t'envoie : "Commande appelée : time, role commande : Renvoyer l'heure actuelle, message contexte : 16h30", tu donnes une réponse qui ressemble à cela : "Il est actuellement 16h30, c'est l'heure du gouter !"
- Je t'envoie : "Commande appelée : time, role commande : Renvoyer l'heure actuelle, message contexte : 22h30", tu donnes une réponse qui ressemble à cela : "Il est actuellement 16h30, c'est l'heure de dormir!"
- Je t'envoie : "Commande appelée : warn, role commande : Avertit un membre pour un mauvais comportement, contexte : Aliben avertit pour insultes", tu donnes une réponse qui ressemble à cela : "Bah alors AliBen, pourquoi tu insultes les gens ? Tu sais que cela est interdit sur notre serveur, ne recommences plus s'il te plaît sous peine de sanctions plus strictes"

Tu ne dois que renvoyer ta réponse et absolument rien d'autre. Tu ne dois pas mettre de "Voici votre réponse" ou autre qui y ressemble car cela n'est pas ton rôle, tu ne dois pas non plus me demander si cela me convient. Ton unique rôle est de générer des messages et pas de demander quelque chose. Tu ne dois pas non plus me demander si je veux autre chose, tu  ne dois t'occuper que d'une seule commande à la fois. Tu ne dois pas demander aux gens si ils veulent de l'aide supplémentaire. 
"""


class MyContext(commands.Context):
    async def send_custom(self, content : str, **kwargs) -> discord.Message:
        await self.defer()
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=[
                {"role": "user", "content": PROMPT},
                {"role" : "user", "content" : content}
            ],
            temperature=0.9
        )
        
        text = response["choices"][0]["message"]["content"]
        
        
        return await self.send(text, **kwargs)
    

class ExampleCog(commands.Cog):
    def __init__(self, bot : commands.Bot) -> None:
        self.bot = bot
        
        
    @commands.command(name="ping")
    async def ping_command(self, ctx : MyContext) -> discord.Message:
        return await ctx.send_custom('Commande appelée : ping, Role : Renvoyer pong pour montrer que le bot est en ligne')


class Bot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix='!', intents=discord.Intents.all())
        
        
    async def get_context(self, message : discord.Message, *, cls=MyContext) -> MyContext:
        return await super().get_context(message, cls=cls)


    async def setup_hook(self) -> None:
        await self.add_cog(ExampleCog(self))
        await self.tree.sync()

    async def on_ready(self) -> None:
        print('Je suis en ligne !')



def main() -> None:
    dotenv.load_dotenv()
    bot = Bot()

    TOKEN = os.getenv('TOKEN')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    if OPENAI_API_KEY is None:
        raise ValueError('Le token OpenAI n\'est pas défini !')

    if TOKEN is None:
        raise ValueError('Le token n\'est pas défini !')


    openai.api_key = OPENAI_API_KEY
    bot.run(TOKEN)


if __name__ == '__main__':
    main()
    
    
    
