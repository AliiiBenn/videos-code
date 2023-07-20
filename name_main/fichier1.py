


# Chaque fichier python possède un nom 
# Ce nom est stocké dans la variable __name__
print(__name__) # __main__

# Néanmoins, si le fichier est importé dans un autre fichier
# Le nom de la variable __name__ sera le nom du fichier
# et non plus __main__



# C'est ici que l'on va pouvoir utiliser la variable __name__
# Pour pouvoir exécuter du code uniquement si le fichier est exécuté
# directement et non pas importé dans un autre fichier

if __name__ == "__main__":
    print("Le fichier est exécuté directement")