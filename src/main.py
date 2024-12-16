from ipd_classes import inpoda
from IPython import display

# affiche un menu
def printMenu(options: list[str]):
    output = '\n'.join(options)
    print(f"MENU :\n{output}\n")

# affiche un message et attend que l'utilisateur appuie sur entrée
def printPause(msg: str):
    print(msg)
    input("Appuyez sur Entrée pour continuer")
 
ipd = inpoda("./tweets.json")
#df = ipd.getDF()
#print(df)
ipd.test_everything()

if __name__ == "__mai__":
    ipd = inpoda("./tweets.json")

    menus = {
        "main": [
            "(0) Quitter",
            "(1) Menu Tops",
            "(2) Menu Extra"
        ],
        "tops": [
            "(0) Menu Principal",
            "(1 [k]) Top k hashtags",
            "(2 [k]) Top k utilisateurs",
            "(3 [k]) Top k utilisateurs mentionnés",
            "(4 [k]) Top K topics",
        ],
        "extra": [
            "(0) Menu Principal",
            "(1 ID) Nombre de publications par utilisateurs",
            "(2 h) Nombre de publications par hashtag",
            "(3 t) Nombre de publications par topic",
            "(4 ID) Ensemble des publications d'un utilisateur",
            "(5 ID) Ensemble des publications mentionnant un utilisateur",
            "(6)",
            "(7)",
        ]
    }

    stop = False

    # boucle principale
    while stop == False:
        printMenu(menus["main"])
        saisie = input("Veuillez saisir votre choix :\n")
        saisie = saisie.strip().split(" ")

        choix = saisie[0]
        if len(saisie) > 1:
            option = saisie[1]
        else:
            option = ""

        match choix:
            case '0':
                stop = True
                break
            case '1':
                ipd.listPosts()
                input("Appuyez sur Entrée pour continuer")
            case '2':
                index = int(option)
                printPause(f"L'auteur du post n°{index} est : {ipd.getAuteur(index)}")
            case '3':
                index = int(option)
                printPause(f"Liste des hashtags du post n°{index} :\n{ipd.getHashtags(index)}")
            case '4':
                index = int(option)
                printPause(f"Liste des utilisateurs mentionnés du post n°{index} :\n{ipd.getMentionned(index)}")
            case '5':
                index = int(option)
                printPause(f"Le post n°{index} est {ipd.getSentiment(index)}")
            case _:
                print("Argument Invalide")
                pass
        print("")
