# -*- coding: utf-8 -*-
"""
Script unique : Rassemblement des contextes textuels et génération du WordCloud
Pour lancer le programme :
1) Ouvrir un terminal et activer l'environnement : source chemin/environnement/bin/activate
2) Installer les dépendances si nécessaire : pip install wordcloud matplotlib nltk
"""

import os
import unicodedata
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords

# ==========================================
# 1. CONFIGURATION ET ENTRÉES UTILISATEUR
# ==========================================
chemin_dossier = input("Entrez le chemin du dossier contenant tous les fichiers .txt (ex: ../contextes) : ").strip()
fichier_rassembler = "../nuage/corpus/tous_contextes_fra.txt"
mot_cible = "âme"

# Vérification de l'existence du dossier source
if not os.path.isdir(chemin_dossier):
    raise FileNotFoundError(f"Le dossier '{chemin_dossier}' n'existe pas.")

# Récupération de la liste des fichiers .txt
fichiers_txt = [f for f in os.listdir(chemin_dossier) if f.endswith(".txt")]
if not fichiers_txt:
    raise FileNotFoundError(f"Aucun fichier .txt trouvé dans '{chemin_dossier}'.")

# Assurer la création des dossiers de sortie
os.makedirs(os.path.dirname(fichier_rassembler), exist_ok=True)
os.makedirs("../nuage/images", exist_ok=True)

# ==========================================
# 2. FUSION ET NORMALISATION DES TEXTES
# ==========================================
print("\n[1/3] Rassemblement et normalisation des fichiers textuels...")
with open(fichier_rassembler, "w", encoding="utf-8") as out_file:
    for nom_fichier in fichiers_txt:
        chemin_fichier = os.path.join(chemin_dossier, nom_fichier)
        try:
            with open(chemin_fichier, "r", encoding="utf-8") as f:
                texte = f.read()
        except UnicodeDecodeError:
            with open(chemin_fichier, "r", encoding="latin-1") as f:
                texte = f.read()
        
        # Préservation stricte des diacritiques (accents) en normalisation NFC
        texte = unicodedata.normalize("NFC", texte)
        out_file.write(texte + "\n")
        print(f"  -> Ajouté et normalisé : {nom_fichier}")

print(f"✓ Tous les fichiers ont été concaténés dans : '{fichier_rassembler}'")

# ==========================================
# 3. EXTRACTION DU CONTEXTE (MOTS VOISINS)
# ==========================================
print(f"\n[2/3] Extraction des mots gravitant autour de '{mot_cible}'...")
with open(fichier_rassembler, "r", encoding="utf-8") as f:
    texte_global = f.read().lower()

texte_global = unicodedata.normalize("NFC", texte_global)
tous_les_mots = texte_global.split()
mots_autour_target = []

# Récupération des voisins de gauche (i-1) et de droite (i+1)
for i, mot in enumerate(tous_les_mots):
    if mot == mot_cible:
        if i > 0:
            mots_autour_target.append(tous_les_mots[i-1])
        if i < len(tous_les_mots) - 1:
            mots_autour_target.append(tous_les_mots[i+1])

# ==========================================
# 4. NETTOYAGE LINGUISTIQUE (STOPWORDS)
# ==========================================
try:
    stopwords_fr = set(stopwords.words('french'))
except LookupError:
    print("  ..Téléchargement du dictionnaire de stopwords NLTK..")
    nltk.download('stopwords', quiet=True)
    stopwords_fr = set(stopwords.words('french'))

# Ajout de votre liste personnalisée de mots à ignorer
mots_ignorer = {
    'un', 'une', 'd', 'l', 'quelques', 'fichier', 'cette', 'ces', 'tout', 'tous',
    'afin', 'mot', 'peut', 'autant', 'comporte', 'décallée', 'doit', 'apparu',
    'voir', 'auprès', 'dite', 'deuxième', 'quelle', 'première', 'chaque', 'toute',
    'vaut', '.', 'bonne', 'autre', 'non', 'fournit', 'sipi', 'plus', 'selon',
    'utilisé', 'courant', 'comme', 'comment', 'troisième', 'très', 'existe',
    'detectors', 'désignait', 'oppose', 'prévue', 'correspond', 'fermer',
    'véritablement', 'également', 'devient', 'sous', 'aussi', 'parfaitement',
    'compréhension', 'complètement', 'appelle'
}
stopwords_fr.update(mots_ignorer)

# Filtrage strict : garde uniquement les chaînes alphabétiques signifiantes
mots_propres = [
    mot for mot in mots_autour_target 
    if mot.isalpha() and len(mot) > 2 and mot not in stopwords_fr
]

# Visualisation des métadonnées dans le terminal
print(f"  -> Aperçu brut des voisins : {mots_autour_target[:15]}")
print(f"  -> Aperçu après filtrage   : {mots_propres[:15]}")
print(f"  -> Volume total extrait    : {len(mots_propres)} mots.")

# ==========================================
# 5. GÉNÉRATION ET SAUVEGARDE DU WORDCLOUD
# ==========================================
print("\n[3/3] Génération du Nuage de mots...")
if mots_propres:
    nuage = WordCloud(
        width=800, 
        height=400, 
        background_color="white",
        max_words=100
    ).generate(" ".join(mots_propres))
    
    # Configuration de l'affichage Matplotlib
    plt.figure(figsize=(10, 5))
    plt.imshow(nuage, interpolation='bilinear')
    plt.axis("off")
    plt.title(f"Mots gravitant autour de '{mot_cible}' en français", fontsize=14, pad=15)

    # Sauvegarde de l'image
    chemin_image = "../nuage/images/fr.png"
    plt.savefig(chemin_image, dpi=300, bbox_inches='tight')
    print(f"✓ Nuage de mots sauvegardé avec succès dans : {chemin_image}")
    
    # Affichage à l'écran
    plt.show()
else:
    print(f"Aucun mot exploitable trouvé autour du lemme '{mot_cible}'. Le WordCloud n'a pas pu être instancié.")