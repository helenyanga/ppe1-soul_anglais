import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import nltk

# ---------------------------
# STOPWORDS EN ANGLAIS
# ---------------------------
try:
    stopwords_en = set(stopwords.words('english'))
except:
    nltk.download('stopwords')
    stopwords_en = set(stopwords.words('english'))

# Ajout de stopwords personnalisés (anglais)
mots_ignorer = {
    "the", "and", "for", "with", "from", "that", "this", "these", "those",
    "a", "an", "to", "of", "in", "on", "at", "by", "is", "are", "was", "were",
    "be", "been", "being", "it", "its", "as", "or", "but"
}

stopwords_en.update(mots_ignorer)

# ---------------------------
# FICHIER CONTEXTES
# ---------------------------
fichier = "../contextes/tous_contextes_en.txt"

with open(fichier, 'r', encoding='utf-8') as f:
    texte = f.read().lower()

# ---------------------------
# TOKENISATION
# ---------------------------
tous_les_mots = texte.split()
mots_autour_soul = []

# ---------------------------
# EXTRACTION CONTEXTE
# ---------------------------
for i, mot in enumerate(tous_les_mots):
    if mot == "soul":
        if i > 0:
            mots_autour_soul.append(tous_les_mots[i - 1])
        if i < len(tous_les_mots) - 1:
            mots_autour_soul.append(tous_les_mots[i + 1])

# ---------------------------
# NETTOYAGE
# ---------------------------
mots_propres = []

for mot in mots_autour_soul:
    mot = mot.lower()
    if mot not in stopwords_en and len(mot) > 2 and mot.isalpha():
        mots_propres.append(mot)

# ---------------------------
# WORDCLOUD
# ---------------------------
nuage = WordCloud(
    width=800,
    height=400,
    background_color="white",
    collocations=False
).generate(" ".join(mots_propres))

# ---------------------------
# AFFICHAGE
# ---------------------------
plt.imshow(nuage, interpolation="bilinear")
plt.axis("off")
plt.title("Words around 'soul'")

# ---------------------------
# SAUVEGARDE
# ---------------------------
os.makedirs("../nuage", exist_ok=True)

plt.savefig("../nuage/wordcloud_soul_en.png", dpi=300, bbox_inches='tight')
print("✓ Nuage sauvegardé dans ../nuage/wordcloud_soul_en.png")

plt.show()



#Commande : python3 wordcloud_en.py