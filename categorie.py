"""Display the existing categories of the Todos

:param listCategorie: a list of the existing categories
"""
def categorieAfficher(listCategorie: list):
    print("Les catégories déjà existantes sont :\n")
    for cat in listCategorie:
        print("->  " + cat, end="\n")

"""Change a Todo of category

:param data: list of the Todos
:param nouvelle: new category for the Todo
:param index: index of the Todo to modify

:return: the modified list of the Todos
"""
def changeCategorie(data: list, nouvelle: str, index: int) -> list:
    print("Catégorie modifiée")
    nData = data
    nData[index - 1]["categorie"] = nouvelle
    return nData

"""Delete a category

Move all the Todos in the category to the "autre" category

:param data: list of the Todos
:param catergorie: category to be deleted

:return: modified list of the Todos
"""
def categorieSupprimer(data: list, categorie: str) -> list:
    nData = data
    for todo in nData:
        if todo["categorie"] == categorie:
            todo["categorie"] = "autre"
    return nData

"""Display a message of help to the user
"""
def categorieAide():
    print("gvvj")