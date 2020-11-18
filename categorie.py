def categorieAfficher(listCategorie):
    print("Les catégories déjà existantes sont :\n")
    for cat in listCategorie:
        print("->  " + cat, end="\n")

def changeCategorie(data, nouvelle, index):
    print("Catégorie modifiée")
    nData = data
    nData[index - 1]["categorie"] = nouvelle
    return nData

def categorieSupprimer(data, categorie):
    nData = data

    for todo in nData:
        if todo["categorie"] == categorie:
            todo["categorie"] = "autre"

    return nData

def categorieAide():
    print("gvvj")