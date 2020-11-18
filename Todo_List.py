import sys
import os
import json
import win32api
from categorie import *

path = "C:\\Users\\marti\\source\\repos\\Todo_List\\Todo_List\\data.json"
pathPrint = "C:\\Users\\marti\\source\\repos\\Todo_List\\Todo_List\\"

def loadTodos(path):
	with open(path) as jsonFile:
		return json.load(jsonFile)

def countTodo(data):
    count = len(data)
    return count

def saveTodos(todos, path):
    with open(path, 'w') as jsonFile:
        json.dump(todos, jsonFile, indent=2)
    print("Todo enregistré")

def listCategoriesTodo(data):
    categories = []
    for todo in data:
        if not todo["categorie"] in categories:
            categories.append(todo["categorie"])
    return categories

def displayTodo(args, data):
    if len(args) <= 2:
        print("Todo enregistré(s) :\n")
        for cat in listCategoriesTodo(data):
            print("\n  --- " + cat.capitalize() + " ---  ")
            for dat in data:
                if cat == dat["categorie"]:
                    print("N°" + str(dat["number"]) + "\t" + dat["content"])
    else:
        try:
            index = int(args[2])
        except:
            index = args[2]

        if type(index) is int:
            index = int(args[2])
            if index < len(data):
                todo = data[index-1]
                print("Todo N°" + str(todo["number"]) + " :\t" + todo["content"])
            else:
                print("Ce Todo n'existe pas !")

        else:
            categorie = args[2]
            if categorie in listCategoriesTodo(data):
                print("Todo dans la catégorie : " + categorie + "\n")
                for dat in data:
                    if dat["categorie"] == categorie:
                        print("N°" + str(dat["number"]) + "\t" + dat["content"])
            else:
                print("Cette catégorie n'existe pas.")

def addTodo(args, data, index):
    if len(args) >= 3:
        content = ""
        for i in range(2, len(args)):
            content += args[i] + " "
    else:
        print("Saississez un Todo à rajouter :")
        content = input("? ")
        print("")

    print("Nouveau Todo ajouté avec le numéro " + str(index + 1) + " :\n" + content)
    newTodo = dict()
    newTodo["number"] = index + 1
    newTodo["categorie"] = "autre"
    newTodo["content"] = content

    data.append(newTodo)
    return data

def categorieTodo(data, args):
    if len(args) >= 3:
        if args[2].lower() == "help":
            categorieAide()

        elif args[2].lower() == "afficher"  or args[2].lower() == "aff":
            categorieAfficher(listCategories)

        elif args[2].lower() == "ajouter" or args[2].lower() == "aj":
            if len(args) < 5:
                index = input("Entrez le Todo à modifier : ")
            else:
                index = ""
                for i in range(4, len(args)):
                    index += args[i] + ","

            if len(args) < 4:
                categorie = input("Entrez la catégorie choisie : ")
            else:
                categorie = args[3]
            
            index = index.split(",")
            index.pop()
            nData = data
            for i in index:
                nData = changeCategorie(nData, categorie, int(i))
            saveTodos(nData, path)

        elif args[2].lower() == "retirer" or args[2].lower() == "ret":
            if len(args) < 4:
                index = int(input("Entrez le Todo à modifier : "))
            else:
                index = int(args[3])

            nData = changeCategorie(data, "autre", index)
            saveTodos(nData, path)

        elif args[2].lower() == "supprimer" or args[2].lower() == "sup":
            if len(args) < 4:
                categorie = input("Entrez la catégorie à supprimer : ")
            else:
                categorie = args[3]

            if categorie in listCategoriesTodo(data):
                nData = categorieSupprimer(data, categorie)
                saveTodos(nData, path)
            else:
                print("Cette catégorie n'existe pas.")

        else:
            print("Commande inconnue\n")
            categorieAide()
    else:
        print("Essayer 'todo categorie help' pour plus d'information sur la commande")

def deleteTodo(args, data):
    if len(args) >= 3:
        index = args[2]
    else:
        print("Saississez un Todo à supprimer :")
        index = input("? ")
        print("")
    
    if index == "tout":
        confirmation = input("Etes vous sur de vouloir supprimer tous les Todo ? o/n ")
        if confirmation.lower() == "o":
            print("Tous les Todos supprimés")
            return []
        else:
            return None

    index = int(index)
    if index <= len(data):
        print("Suppression du Todo N°" + str(index))
        data.pop(index-1)
        i = 1
        for todo in data:
            todo["number"] = i
            i += 1
        return data
    else:
        print("Ce Todo n'existe pas !")
        return None

def printTodo(args, data):
    ok = True
    if len(args) >= 3:
        categorie = args[2]
        if not categorie in listCategoriesTodo(data):
            print("Cette catégorie n'existe pas.")
            ok = False
        else:
            toPrint = "Liste des " + categorie + "\n"
            for todo in data:
                if todo["categorie"] == categorie:
                    toPrint += "\nN° " + str(todo["number"]) + "\t" + todo["content"]
    else:
        toPrint = "Liste des Todo\n"
        for todo in data:
            toPrint += "\nN° " + str(todo["number"]) + "\t" + todo["content"]

    print(toPrint)

    if ok:
        sur = input("Etes vous sur de vouloir imprimer les Todo ? o/n ")
        if sur == "o":
            print("Impression des Todo")
            filename = "toPrint.txt"
            with open(pathPrint + filename, "w") as printFile:
                printFile.write(toPrint)

            dir = pathPrint
            win32api.ShellExecute( 0,  "print",  filename, None, ".", 0)

def main():
    data = loadTodos(path)
    todoNumber = countTodo(data)

    args = sys.argv
    if len(args) == 1:

        displayTodo(args, data)

    elif len(args) >= 2:

        if args[1].lower() == 'afficher' or args[1].lower() == 'aff':

            displayTodo(args, data)

        elif args[1].lower() == 'ajouter' or args[1].lower() == 'aj':

            newData = addTodo(args, data, todoNumber)
            saveTodos(newData, path)

        elif args[1].lower() == 'categorie' or args[1].lower() == 'cat':
            
            categorieTodo(data, args)

        elif args[1].lower() == 'supprimer' or args[1].lower() == 'sup':

            newData = deleteTodo(args, data)

            if newData != None:
                saveTodos(newData, path)

        elif args[1].lower() == 'help' or args[1] == '?':

            print("""				Todo List :
----------------------------------------------------------------------
Todo list est une application de gestion de mémos (des Todo).
Vous pouvez les gérer grâce aux différentes commandes suivantes :

    todo [aff/aj/sup]


 aff/afficher___________: afficher l'ensemble des Todo enregistrés
			  par l'utilisateur
 aff/afficher [num]_____: spécifie un Todo à afficher


 aj/ajouter_____________: ajouter un nouveau Todo à la liste
			  l'utilisateur doit ensuite saisir le contenu du Todo
 aj/ajouter [contenu]___: ajouter un nouveau Todo à la liste dont le
			  contenu est spécifié


 sup/supprimer__________: supprimer un Todo de la liste (opération définitive)
			  l'utilisateur doit ensuite saisir le numéro
			  du Todo spécifié
 sup/supprimer [num]____: supprimer le Todo de la liste dont le numéro
			  est spécifié
 sup/supprimer tout_____: supprimer l'ensemble des Todo de la liste


 help___________________: affiche ce message""")

        elif args[1].lower() =="print":

            printTodo(args, data)

        else:

            print("Commande inconnue\nEssayer 'todo help' pour plus d'infos")

#================================================
# Main
#================================================
print("")
main()
print("")
#__END__
