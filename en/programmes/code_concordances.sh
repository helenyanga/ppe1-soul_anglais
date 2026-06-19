#!/usr/bin/bash
#Code pour le concordancier en HTML.
#Boucle qui génère une page HTML comprenant le contexte gauche, le mot cible et le contexte droit pour chaque dump-text :

echo "Génération du concordancier..."

fichier_context=$1
fichier_concordance=$2

if [ $# -ne 2 ]
then
	echo "Le script doit prendre exactement 2 arguments." #Sur la konsole, appeler le programme et ses arguments de la manière suivante : ./code_concordances.sh ../dumps-text ../concordances
	exit 1
fi

for fichier in "$fichier_context"/en-*.txt
do
    nom_fichier=$(basename "$fichier" .txt)
    N=$(echo "$nom_fichier" | sed 's/^en-//')

    fichier_html_concordance="$fichier_concordance/en-${N}.html"

    echo "Traitement des fichiers : $nom_fichier → en-${N}.html"

    echo -e "<!DOCTYPE html>
        <html>
            <head>
                <meta charset=\"UTF-8\">
            </head>
            <body>
                <table>
                    <tr>
                        <th>Contexte gauche</th>
                        <th>Mot cible</th>
                        <th>Contexte droit</th>
                    </tr>" > "$fichier_html_concordance"

    #grep -i '\bsouls\?\b' "$fichier"
    grep -o -i -E '.{0,50}\bsouls?\b.{0,50}' "$fichier" | while IFS= read -r line

    do
        mot=$(echo "$line" | grep -o -i -E '\bsoul?\b' | head -1)

        contexte_gauche=$(echo "$line" | sed -E "s/^(.*)\bsouls?\b.*$/\1/I")

        contexte_droit=$(echo "$line" | sed -E "s/^.*\bsouls?\b(.*)$/\1/I")

        echo -e "  <tr>
                    <td>$contexte_gauche</td>
                    <td>$mot</td>
                    <td>$contexte_droit</td>
                   </tr>" >> "$fichier_html_concordance"

    done

    echo -e "          </table>
                </body>
            </html>" >> "$fichier_html_concordance"

done

echo "Concordanciers terminés."
