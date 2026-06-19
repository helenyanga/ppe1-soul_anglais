#!/usr/bin/bash
#Code pour le dump en txt.
#Boucle pour obtenir le texte brut (dumps-text) de chaque URLs :
echo "Traitement des pages HTML pour l'obtention du texte brut de chaque URLs..."

N=$1 #N pour numéro de la ligne
line=$2

while read -r line
do
    lynx -dump -nolist "../aspirations/fra-${N}.html" > "../dumps-text/fra-${N}.txt"
    N=$(expr $N + 1)
done < ../urls/fra.txt

echo "Dumps terminées."
