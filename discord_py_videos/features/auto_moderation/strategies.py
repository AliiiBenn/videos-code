import discord

from abc import ABC, abstractmethod



class AutoModerationStrategy(ABC):
    @abstractmethod
    def check(self, message : discord.Message) -> bool:
        pass 



class MajusculeStrategy(AutoModerationStrategy):
    def get_content(self, message : discord.Message) -> str:
        return message.content
    
    def get_maj_count(self, content : str) -> int:
        return len([character for character in content if character.isupper()])
    
    def get_percentage(self, maj_count : int, content : str) -> float:
        return maj_count / len(content)
    
    def check_percentage(self, percentage : float) -> bool:
        LIMIT = 0.25
        return percentage > LIMIT
    
    
    def check(self, message : discord.Message) -> bool:
        message_content = self.get_content(message)
        message_maj_count = self.get_maj_count(message_content)
        maj_percentage = self.get_percentage(message_maj_count, message_content)
        
        return self.check_percentage(maj_percentage)
        


class DiscordLinkStrategy(AutoModerationStrategy):
    def check(self, message : discord.Message) -> bool:
        return "discord.gg" in message.content or "discordapp.com/invite" in message.content