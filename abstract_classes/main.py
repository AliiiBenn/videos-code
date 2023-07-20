from abc import ABC, abstractmethod



# Pour créer une nouvelle classe abstraite, il faut hériter de la classe ABC
class Animal(ABC):
    # Quand on crée un constructeur dans une classe abstraite
    # Ce constructeur lui sera concret et non pas abstrait
    def __init__(self, name : str, age : int) -> None:
        self.name = name 
        self.age = age 
        
        
    # Pour créer une méthode abstraite, il faut utiliser le décorateur @abstractmethod
    # Une méthode abstraite est une méthode qui n'a pas de corps
    # Elle ne fait rien, elle est juste déclarée
    # Elle doit être redéfinie dans les classes filles
    @abstractmethod
    def parler(self) -> None:
        pass
    
    
    @abstractmethod
    def manger(self) -> None:
        pass
    
    
    
# On ne peut pas instancier une classe abstraite
# animal = Animal("Bob", 5) # TypeError: Can't instantiate abstract class Animal with abstract methods manger, parler
# mais on peut instancier une classe fille

class Chien(Animal):
    def __init__(self, name : str, age : int) -> None:
        super().__init__(name, age)
        
        
    def parler(self) -> None:
        print("Wouaf wouaf")
        
        
    def manger(self) -> None:
        print("Je mange de la viande")
        
    
    
class Chat(Animal):
    def __init__(self, name : str, age : int) -> None:
        super().__init__(name, age)
        
        
    def parler(self) -> None:
        print("Miaou miaou")
        
        
    def manger(self) -> None:
        print("Je mange du poisson")
        
        
        
# Les classes abstraites sont utiles pour faire comprendre 
# quels sont les types que nous allons utiliser 
# des fois il est plus simple de créer une classe abstraite
# pour éviter des liens concrets dans le code 

def faire_parler(animal : Animal) -> None:
    animal.parler()
    
    
# est bien meilleur que 

def faire_parler(animal : Chien | Chat) -> None:
    animal.parler()
    
    
# car si on a 10 classes qui héritent de Animal
# on va devoir mettre les 10 classes dans le type hinting
# alors qu'avec une classe abstraite, on ne met que la classe abstraite


if __name__ == "__main__":
    chien = Chien("Bob", 5)
    chat = Chat("Rex", 10)
    
    faire_parler(chien) # Wouaf wouaf
    faire_parler(chat) # Miaou miaou