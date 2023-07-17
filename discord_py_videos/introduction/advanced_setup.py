import discord 
from discord.ext import commands

import os, dotenv

class Bot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix="!",
            intents=discord.Intents.all(),
        )
        
        
    async def setup_hook(self) -> None:
        await self.tree.sync()
        
        
    async def on_ready(self) -> None:
        print("Bot is ready!")
        
        
        
def main() -> None:
    dotenv.load_dotenv()
    
    TOKEN = os.getenv("TOKEN")
    
    if TOKEN is None:
        raise ValueError("TOKEN is not set in .env")
    
    
    bot = Bot()
    bot.run(TOKEN)
    
    
if __name__ == "__main__":
    main()