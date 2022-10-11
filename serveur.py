import Pyro4
import unidecode
from random import choice


# mot = input("Entrer le mot: ")

# remplacement par des underscores

def underscore(mot , L = []):
    r = ''
    for i in mot:
        if i in L:
            r += i + ' '
        else:
            r += '_ '
            
    return r[:-1]
    
    
@Pyro4.expose
class MyServer(object):
    
    Mot = ""
    mot_a_deviner = ""
    affichage = ""
    lettres_deja_proposees = []

    @Pyro4.expose
    @property
    def getLettre(self):
        return self.lettres_deja_proposees

    def word(self):
        f = open('mots.txt', 'r' , encoding = 'utf8')
        contenu = f.readlines()
        return unidecode.unidecode( choice(contenu) ).upper().replace('\n','')
    
    def renitialize (self):
        self.mot_a_deviner = self.word()
        self.affichage = underscore( self.mot_a_deviner )
        self.lettres_deja_proposees = []
        

    @Pyro4.expose
    @property
    def getMot(self):
        return self.mot_a_deviner

    @Pyro4.expose
    @property
    def getAffichage(self):
        return self.affichage
    
    def verifyLetterIn(self, letter, nb_erreurs):        
        if letter not in self.lettres_deja_proposees and letter in self.mot_a_deviner:
            self.lettres_deja_proposees += [ letter ]
            nb_erreurs = 3
        
        elif letter not in self.mot_a_deviner:
            nb_erreurs -= 1
                
        self.affichage = underscore( self.mot_a_deviner , self.lettres_deja_proposees )
        sentence = f'\nMot à deviner : {self.affichage } il vous reste: {nb_erreurs} tentative(s)'
        return sentence, nb_erreurs
        

daemon = Pyro4.Daemon()                
ns = Pyro4.locateNS()                  
uri = daemon.register(MyServer())   
ns.register("jeu.pendu", uri)   

print("Ready.")
print(uri)
daemon.requestLoop()        