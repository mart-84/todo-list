import sys
import os
import json
import win32api
from categorie import *


# Path of the Json file where data is saved
path = "C:\\Users\\marti\\source\\repos\\Todo_List\\Todo_List\\data.json"
# Path of the repertory where toPrint file is saved
pathPrint = "C:\\Users\\marti\\source\\repos\\Todo_List\\Todo_List\\"

"""Load the content of the Json file specified

:param path: path of the json file to load

:return: the content of the json file
"""
def loadTodos(path: str) -> list:
	with open(path) as jsonFile:
		return json.load(jsonFile)

"""Count the total number of Todo

:param data: list of the Todo

:return: number of Todos in the data
"""
def countTodo(data: list) -> int:
    count = len(data)
    return count

"""Save the data fo the Todos in the Json file

:param todos: data of the Todo to save
:param path: path of the Json file
"""
def saveTodos(todos: list, path: str):
    with open(path, 'w') as jsonFile:
        json.dump(todos, jsonFile, indent=2)
    print("Todo enregistré")

"""List all the existing categories of the Todos
In the list, each category is unique

:param data: the list of the Todo

:return: a list of the categories
"""
def listCategoriesTodo(data: list) -> list:
    categories = []
    for todo in data:
        if not todo["categorie"] in categories:
            categories.append(todo["categorie"])
    return categories

"""Display the selected Todo

:param args: arguments passed after the "todo" command
:param data: list of the Todos
"""
def displayTodo(args: list, data: list):
    if len(args) <= 2:
        print("Todo enregistré(s) :")
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

"""Add a new Todo to the list

:param args: arguments passed after the "todo" command
:param data: list of the Todos
:param index: the number of Todos before adding

:return: the new list of the Todos after adding
"""
def addTodo(args: list, data: list, index: int) -> list:
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

"""Manage the different actions of the "todo category" command

:param args: arguments passed after the "todo" command
:param data: list of the Todos
"""
def categorieTodo(data: list, args: list):
    if len(args) >= 3:
        if args[2].lower() == "help":
            categorieAide()

        elif args[2].lower() == "afficher"  or args[2].lower() == "aff":
            categorieAfficher(listCategoriesTodo(data))

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

"""Delete one or all the Todos of the list

:param args: arguments passed after the "todo" command
:param data: list of the Todos

:return: a blank list
"""
def deleteTodo(args: list, data: list) -> list:
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

"""Print a category or all the Todos of the list

Use the win32api package:
pip install pywin32

:param args: arguments passed after the "todo" command
:param data: list of the Todos
"""
def printTodo(args: list, data: list):
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
            os.remove(pathPrint + filename)

"""Open the JSON file where data is stored

:param file: name of the file where data is stored
"""
def openTodo(file: str):
    print("Ouverture du fichier des Todo")
    print("Fermez le fichier pour continuer")
    os.system("data.json")


"""Redirect the process to the adequate part depending on the arguments

Main function of the program
"""
def main():
    data = loadTodos(path)
    todoNumber = countTodo(data)
    args = sys.argv
    
    print("")
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

        elif args[1].lower() == "print":

            printTodo(args, data)

        elif args[1].lower() == "open":

            openTodo("data.json")

        else:

            print("Commande inconnue\nEssayer 'todo help' pour plus d'infos")
    print("")

#================================================
# Main
#================================================
main()
#__END__
