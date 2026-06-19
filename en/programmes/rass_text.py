#Script qui permet de rassembler tous les contextes (textes) en anglais en un seul fichier txt

import os

# 1) Demander les chemins à l'utilisateur
chemin_dossier = input("Entrez le chemin du dossier contenant les fichiers à rassembler : ").strip() #Donner le dossier "contextes"
fichier_destination = input("Entrez le chemin et le nom du fichier final (ex: tous_contexte_en.txt) : ").strip()

# 2) Vérifier si le dossier existe
if not os.path.isdir(chemin_dossier):
    raise FileNotFoundError(f"Le dossier '{chemin_dossier}' n'existe pas.")

# 3) Récupérer la liste de tous les fichiers .txt
fichiers_txt = [f for f in os.listdir(chemin_dossier) if f.endswith(".txt")]

if not fichiers_txt:
    print(f"⚠ Aucun fichier .txt trouvé dans '{chemin_dossier}'.")
else:
    # 4) Ouvrir le fichier final en mode écriture ('w')
    with open(fichier_destination, "w", encoding="utf-8") as out_file:
        for nom_fichier in fichiers_txt:
            chemin_complet = os.path.join(chemin_dossier, nom_fichier)
            
            # Gestion des encodages pour lire le contenu
            try:
                with open(chemin_complet, "r", encoding="utf-8") as f:
                    contenu = f.read()
            except UnicodeDecodeError:
                with open(chemin_complet, "r", encoding="latin-1") as f:
                    contenu = f.read()
            
            # Écrire le contenu dans le fichier final avec un saut de ligne
            out_file.write(contenu + "\n")
            print(f"Ajouté : {nom_fichier}")

    print(f"\n✓ Terminé ! Tous les fichiers ont été rassemblés dans '{fichier_destination}'.")



"""commade : python3 rass_text.py
-> commande pour le dossier contextes : ../contextes
-> commande pour le fichier de sortie (où il doit appraître et donner son nom de fichier.txt) : ./contextes/tous_contextes_en.txt
"""