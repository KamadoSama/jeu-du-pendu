import Pyro4


def controleSaisie ():
    lettre = input('Entrez une lettre : ')
    while (len( lettre ) > 1 ):
        input('Entrez une lettre : ')
    return lettre.upper()

nameserver = Pyro4.locateNS()
server = Pyro4.Proxy("PYRONAME:jeu.pendu")    

game_start=input(f"Voulez vous faire une partie ? si oui entrez o sinon entrez n : ").upper()

while game_start=="O":
    server.renitialize()
    print(server.getMot)
    print(f'\nMot à deviner : {server.getAffichage}')

    nb_erreurs = 3

    while '_' in server.getAffichage and nb_erreurs >0:
        lettre = controleSaisie()
            
        # Appeler la fonction du serveur verifyIci
        sentence, nb_erreurs = server.verifyLetterIn(lettre, nb_erreurs)
        print(sentence)
    
    if ("_" in server.getAffichage) :
        print("\nPerdu ! Vous avez perdu \nLe mot etait: " + server.getMot)
    else:
        print("Felicitations !")

    game_start=input(f"Voulez vous faire une nouvelle partie ? si oui entrez: o sinon entrez: n").upper()

print(f"Merci d'avoir participer")