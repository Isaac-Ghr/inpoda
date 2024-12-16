from ipd_classes import inpoda
import re

# affiche un menu
def printMenu(options: list[str]):
    for i, option in enumerate(options):
        print(f"({i}) {option}")

def inputNum() -> str:
    try:
        out = re.sub(r"[^\d]", "", input("Votre choix > "))
    except:
        return '0'
    return out

if __name__ == "__main__":
    ipd = inpoda("./tweets.json")

    menus = [
        "Quitter l'application",
        "Menu des classements",
        "Nombre de publication en fonction de x",
        "Publications par auteur",
        "Publications par utilisateur mentionné",
        "Auteurs par hashtags",
        "Auteurs par utilisateur mentionné"
    ]

    stop = False

    # boucle principale
    while stop == False:
        printMenu(menus)
        choix = inputNum()

        match choix:
            case '0':
                stop = True
                break
            case '1':
                submenu = [
                    "Revenir au menu principal",
                    "Top k des hashtags",
                    "Top k des auteurs",
                    "Top k des utilisateurs mentionnés",
                    "Top k des topics"
                ]
                printMenu(submenu)
                subchoix = inputNum()
                match subchoix:
                    case '1':
                        ipd.topHashtags()
                    case '2':
                        ipd.topUsers()
                    case '3':
                        ipd.topMentionned()
                    case '4':
                        ipd.topTopics()
                    case _:
                        pass
            case '2':
                submenu = [
                    "Revenir au menu principal",
                    "Nombre de publications par auteur",
                    "Nombre de publications par hashtags",
                    "Nombre de publications par topics"
                ]
                printMenu(submenu)
                subchoix = inputNum()
                match subchoix:
                    case '1':
                        ipd.countPostByUser()
                    case '2':
                        ipd.countPostByHashtags()
                    case '3':
                        ipd.countPostByTopics()
                    case _:
                        pass
            case '3':
                ipd.postsByUsers()
                input("Appuyez sur entrée..")
            case '4':
                ipd.postsByMentions()
                input("Appuyez sur entrée..")
            case '5':
                ipd.auteursByHashtags()
                input("Appuyez sur entrée..")
            case '6':
                ipd.mentionnedByUser()
                input("Appuyez sur entrée..")
            case _:
                print("Argument Invalide")
                pass
        print("")
