

"""

Syntaxe : lambda arguments : expression

"""


# Exemple classique de fonction lambda


# On crée une fonction lambda qui prend un argument x et qui retourne x * x
# Le problème est que la fonction est inutilisable car elle n'est pas
# stockée dans une variable
lambda x: x * x 


# On peut la stocker dans une variable pour pouvoir l'appeller
# Le nom de la variable va être le nom de la fonction
fonction = lambda x: x * x


# Ici on appelle la fonction lambda stockée dans la variable fonction
print(fonction(2)) # 4
print(fonction(5)) # 25


# Bien que cela soit possible, il est déconseillé de stocker une fonction
# Lambda selon les règles de PEP8. Il est préférable d'utiliser une fonction
# classique

def fonction(x : int) -> int:
    return x * x



# Les fonctions lambda doivent être utilisées
# directement dans des fonctions quie elles mêmes 
# prennent en paramètre des fonction en argument

liste = [1, 2, 3, 4, 5]

print(list(map(lambda x: x * x, liste))) # [1, 4, 9, 16, 25]

# Ici la fonction map est une fonction qui prend en paramètre une fonction
# Nous allons donc lui passer une fonction lambda qui va suivre la même logique
# Qu'avant
