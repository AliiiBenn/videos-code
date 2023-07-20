

# Dans le cas où le fichier est importé dans un autre fichier
# La variable __name__ ne sera pas égale à __main__
# donc le code qui se trouve dans le if ne sera pas exécuté

import fichier1

# Comme le fichier est importé, le code dans le if ne sera pas exécuté

print("Le fichier est importé")